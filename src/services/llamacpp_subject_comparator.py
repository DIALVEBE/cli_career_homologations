from __future__ import annotations

import json
import re
import socket
from urllib import request
from urllib.error import URLError

from entities import Subject, SubjectMatch
from .subject_similarity import subject_similarity


class LlamaCppSubjectComparator:
    def __init__(
        self,
        endpoint_url: str,
        model: str,
        timeout_seconds: int = 600,
        max_tokens: int = 320,
    ) -> None:
        self.endpoint_url = endpoint_url
        self.model = model
        self.timeout_seconds = timeout_seconds
        self.max_tokens = max_tokens

    def compare(self, source: Subject, target: Subject, threshold: float) -> SubjectMatch:
        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "Eres un evaluador academico. Compara dos espacios academicos "
                        "para determinar si son homologables. Responde solo JSON valido, "
                        "sin explicaciones y sin razonamiento paso a paso."
                    ),
                },
                {
                    "role": "user",
                    "content": _prompt(source, target, threshold),
                },
            ],
            "temperature": 0.1,
            "max_tokens": self.max_tokens,
            "response_format": {"type": "json_object"},
            "chat_template_kwargs": {"enable_thinking": False},
        }
        response_payload = self._post(payload)
        content = response_payload["choices"][0]["message"]["content"]
        try:
            parsed = _parse_json_object(content)
        except ValueError as error:
            return _fallback_match(source, target, threshold, str(error), content)
        score = _coerce_score(parsed.get("score", 0.0))
        evidence = _string_list(parsed.get("evidence", []))
        risks = _string_list(parsed.get("risks", []))

        return SubjectMatch(
            source_subject=source.name,
            target_subject=target.name,
            score=score,
            homologable=score >= threshold,
            threshold=threshold,
            evidence=evidence + [f"Riesgo: {risk}" for risk in risks],
        )

    def _post(self, payload: dict) -> dict:
        data = json.dumps(payload).encode("utf-8")
        http_request = request.Request(
            self.endpoint_url,
            data=data,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with request.urlopen(http_request, timeout=self.timeout_seconds) as response:
                return json.loads(response.read().decode("utf-8"))
        except socket.timeout as error:
            raise TimeoutError(
                "llama.cpp no respondio a tiempo. Prueba subir --llamacpp-timeout, "
                "bajar --llamacpp-max-tokens, usar --candidate-limit 1, o arrancar "
                "llama-server con --ctx-size 4096 para CPU."
            ) from error
        except URLError as error:
            raise ConnectionError(
                f"No se pudo conectar con llama.cpp en {self.endpoint_url}. "
                "Verifica que llama-server este corriendo."
            ) from error


def _prompt(source: Subject, target: Subject, threshold: float) -> str:
    return f"""
Compara estos dos espacios academicos y estima compatibilidad de homologacion.

Reglas:
- score debe estar entre 0.0 y 1.0.
- homologable si score >= {threshold}.
- No inventes informacion que no este en los textos.
- No uses razonamiento largo ni etiquetas <think>.
- Maximo 2 evidencias y 2 riesgos.
- Responde solo este JSON:
{{
  "score": 0.0,
  "evidence": ["razon breve"],
  "risks": ["riesgo breve"]
}}

Materia origen:
{_subject_context(source)}

Materia destino:
{_subject_context(target)}
""".strip()


def _subject_context(subject: Subject) -> str:
    return "\n".join(
        [
            f"Nombre: {_trim(subject.name, 300)}",
            f"Programa: {_trim(subject.program, 200)}",
            f"Objetivo: {_trim(subject.objective, 700)}",
            f"Competencias y resultados: {_trim(_competency_text(subject), 900)}",
            f"Contenidos: {_trim(_contents_text(subject), 900)}",
        ]
    )


def _competency_text(subject: Subject) -> str:
    chunks: list[str] = []
    for competency in subject.competencies:
        chunks.append(competency.name)
        chunks.extend(competency.learningResults)
    return " ".join(chunks)


def _contents_text(subject: Subject) -> str:
    return " ".join(competency.contents for competency in subject.competencies)


def _trim(value: str, limit: int) -> str:
    if len(value) <= limit:
        return value
    return value[:limit].rsplit(" ", 1)[0]


def _parse_json_object(content: str) -> dict:
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", content, re.DOTALL)
        if not match:
            raise ValueError("llama.cpp response did not contain a JSON object")
        try:
            return json.loads(match.group(0))
        except json.JSONDecodeError as error:
            raise ValueError(f"llama.cpp response contained invalid JSON: {error.msg}") from error


def _coerce_score(value) -> float:
    score = float(value)
    return max(0.0, min(1.0, score))


def _string_list(value) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(item) for item in value if str(item).strip()]


def _fallback_match(
    source: Subject,
    target: Subject,
    threshold: float,
    reason: str,
    content: str,
) -> SubjectMatch:
    score, evidence = subject_similarity(source, target)
    raw_preview = " ".join(content.split())[:180]
    return SubjectMatch(
        source_subject=source.name,
        target_subject=target.name,
        score=score,
        homologable=score >= threshold,
        threshold=threshold,
        evidence=[
            f"Fallback deterministico: respuesta llama.cpp invalida ({reason}).",
            f"Respuesta parcial: {raw_preview}",
            *evidence,
        ],
    )

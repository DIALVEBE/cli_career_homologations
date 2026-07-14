from entities import Competency, HumanActionDimensions, Subject
from services import LlamaCppSubjectComparator


def test_llamacpp_subject_comparator_maps_json_response_to_subject_match():
    comparator = FakeLlamaCppSubjectComparator(
        endpoint_url="http://localhost:8080/v1/chat/completions",
        model="local-model",
        timeout_seconds=300,
        max_tokens=120,
    )

    match = comparator.compare(
        _subject("Programación"),
        _subject("Introducción a la Programación"),
        threshold=0.40,
    )

    assert match.score == 0.72
    assert match.homologable is True
    assert match.evidence == ["Coinciden contenidos base.", "Riesgo: Falta comparar intensidad horaria."]
    assert comparator.payload["max_tokens"] == 120
    assert comparator.payload["chat_template_kwargs"] == {"enable_thinking": False}


def test_llamacpp_subject_comparator_falls_back_when_json_is_truncated():
    comparator = TruncatedJsonLlamaCppSubjectComparator(
        endpoint_url="http://localhost:8080/v1/chat/completions",
        model="local-model",
    )

    match = comparator.compare(
        _subject("Programación"),
        _subject("Introducción a la Programación"),
        threshold=0.40,
    )

    assert match.source_subject == "Programación"
    assert "Fallback deterministico" in match.evidence[0]
    assert "Respuesta parcial" in match.evidence[1]


class FakeLlamaCppSubjectComparator(LlamaCppSubjectComparator):
    payload: dict

    def _post(self, payload: dict) -> dict:
        self.payload = payload
        return {
            "choices": [
                {
                    "message": {
                        "content": (
                            '{"score": 0.72, '
                            '"evidence": ["Coinciden contenidos base."], '
                            '"risks": ["Falta comparar intensidad horaria."]}'
                        )
                    }
                }
            ]
        }


class TruncatedJsonLlamaCppSubjectComparator(LlamaCppSubjectComparator):
    def _post(self, payload: dict) -> dict:
        return {
            "choices": [
                {
                    "message": {
                        "content": (
                            '{"score": 0.51, "evidence": ["Coincide en fundamentos de '
                            'programacion'
                        )
                    }
                }
            ]
        }


def _subject(name: str) -> Subject:
    return Subject(
        name=name,
        program="Programa",
        objective="Resolver problemas con algoritmos.",
        problemicCore="",
        didacticStrategies="",
        competencies=[
            Competency(
                name="Construir algoritmos.",
                humanActionDimensions=HumanActionDimensions(
                    comprehend=True,
                    act=False,
                    do=True,
                    communicate=False,
                    feel=False,
                ),
                learningResults=["Aplica estructuras de control."],
                contents="Variables, ciclos, condicionales.",
                time="",
                evaluationMechanisms="",
                didacticResources="",
            )
        ],
    )

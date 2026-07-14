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

import json
from pathlib import Path

from services import load_subjects_from_processed_json


def test_load_subjects_from_processed_json_filters_by_prefix(tmp_path: Path):
    processed = tmp_path / "syllabus.json"
    processed.write_text(
        json.dumps(
            {
                "subjects": [
                    _subject_payload("PROGRAM_A/subject.xlsx", "Programación"),
                    _subject_payload("PROGRAM_B/subject.xlsx", "Diseño"),
                ],
                "errors": [],
            }
        ),
        encoding="utf-8",
    )

    subjects = load_subjects_from_processed_json(processed, "PROGRAM_A")

    assert len(subjects) == 1
    assert subjects[0].name == "Programación"
    assert subjects[0].competencies[0].learningResults == ["Resultado"]


def _subject_payload(path: str, name: str) -> dict:
    return {
        "path": path,
        "program": "Programa",
        "name": name,
        "objective": "Objetivo",
        "problemic_core": "Núcleo",
        "didactic_strategies": "Estrategias",
        "competencies": [
            {
                "name": "Competencia",
                "learning_results": ["Resultado"],
                "contents": "Contenido",
                "time": "4 semanas",
                "evaluation_mechanisms": "Evaluación",
                "didactic_resources": "Recursos",
                "human_action_dimensions": {
                    "comprehend": True,
                    "act": False,
                    "do": True,
                    "communicate": False,
                    "feel": False,
                },
            }
        ],
    }

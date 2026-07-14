from __future__ import annotations

import json
from pathlib import Path

from entities import Competency, HumanActionDimensions, Subject


def load_subjects_from_processed_json(path: Path, root_prefix: str | None = None) -> list[Subject]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    subjects = payload.get("subjects", [])

    if root_prefix:
        subjects = [
            subject
            for subject in subjects
            if str(subject.get("path", "")).startswith(root_prefix)
        ]

    return [_subject_from_dict(subject) for subject in subjects]


def _subject_from_dict(payload: dict) -> Subject:
    return Subject(
        name=payload.get("name", ""),
        program=payload.get("program", ""),
        objective=payload.get("objective", ""),
        problemicCore=payload.get("problemic_core", ""),
        didacticStrategies=payload.get("didactic_strategies", ""),
        competencies=[
            _competency_from_dict(competency)
            for competency in payload.get("competencies", [])
        ],
    )


def _competency_from_dict(payload: dict) -> Competency:
    dimensions = payload.get("human_action_dimensions", {})
    return Competency(
        name=payload.get("name", ""),
        humanActionDimensions=HumanActionDimensions(
            comprehend=bool(dimensions.get("comprehend", False)),
            act=bool(dimensions.get("act", False)),
            do=bool(dimensions.get("do", False)),
            communicate=bool(dimensions.get("communicate", False)),
            feel=bool(dimensions.get("feel", False)),
        ),
        learningResults=list(payload.get("learning_results", [])),
        contents=payload.get("contents", ""),
        time=payload.get("time", ""),
        evaluationMechanisms=payload.get("evaluation_mechanisms", ""),
        didacticResources=payload.get("didactic_resources", ""),
    )

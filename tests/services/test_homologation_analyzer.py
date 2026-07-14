from entities import Competency, HumanActionDimensions, Subject
from services import analyze_homologation


def test_analyze_homologation_marks_matches_above_threshold():
    source_subjects = [
        _subject(
            "Programación",
            "Desarrollar algoritmos y programas usando estructuras de control.",
            "Algoritmos, variables, condicionales, ciclos y funciones.",
        )
    ]
    target_subjects = [
        _subject(
            "Introducción a la Programación",
            "Resolver problemas mediante algoritmos, estructuras de control y funciones.",
            "Variables, condicionales, ciclos, funciones y pruebas de escritorio.",
        )
    ]

    report = analyze_homologation(source_subjects, target_subjects, threshold=0.40)

    assert report.total_source_subjects == 1
    assert report.homologable_subjects == 1
    assert report.general_percentage == 1.0
    assert report.results[0].best_match is not None
    assert report.results[0].best_match.homologable is True


def test_analyze_homologation_rejects_matches_below_threshold():
    source_subjects = [
        _subject(
            "Programación",
            "Desarrollar algoritmos y programas usando estructuras de control.",
            "Algoritmos, variables, condicionales, ciclos y funciones.",
        )
    ]
    target_subjects = [
        _subject(
            "Cultura Teológica",
            "Analizar fenómenos religiosos y su relación con la cultura.",
            "Religión, cultura, sociedad, teología y humanidades.",
        )
    ]

    report = analyze_homologation(source_subjects, target_subjects, threshold=0.40)

    assert report.homologable_subjects == 0
    assert report.general_percentage == 0.0
    assert report.results[0].best_match is not None
    assert report.results[0].best_match.homologable is False


def _subject(name: str, objective: str, contents: str) -> Subject:
    return Subject(
        name=name,
        program="Programa origen",
        objective=objective,
        problemicCore="",
        didacticStrategies="",
        competencies=[
            Competency(
                name=objective,
                humanActionDimensions=HumanActionDimensions(
                    comprehend=True,
                    act=False,
                    do=True,
                    communicate=False,
                    feel=False,
                ),
                learningResults=[objective],
                contents=contents,
                time="",
                evaluationMechanisms="",
                didacticResources="",
            )
        ],
    )

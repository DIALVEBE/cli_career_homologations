from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from adapters.parsing_syllabus_gateway.xlsx import XLSXParsingSyllabusGateway
from entities import Subject
from services import analyze_homologation, build_inventory, write_csv_report, write_json_report


def main() -> None:
    parser = argparse.ArgumentParser(prog="homologations")
    subparsers = parser.add_subparsers(dest="command", required=True)

    inventory_parser = subparsers.add_parser("inventory", help="Scan syllabus files.")
    inventory_parser.add_argument("root", nargs="?", default="data/raw")
    inventory_parser.add_argument("--output", "-o", type=Path)

    extract_parser = subparsers.add_parser("extract-xlsx", help="Extract readable XLSX syllabus files.")
    extract_parser.add_argument("root", nargs="?", default="data/raw")
    extract_parser.add_argument("--output", "-o", type=Path, default=Path("data/processed/syllabus.json"))

    analyze_parser = subparsers.add_parser("analyze", help="Analyze homologation compatibility.")
    analyze_parser.add_argument("source_root", type=Path)
    analyze_parser.add_argument("target_root", type=Path)
    analyze_parser.add_argument("--threshold", type=float, default=0.40)
    analyze_parser.add_argument("--output-json", type=Path, default=Path("data/reports/homologation_report.json"))
    analyze_parser.add_argument("--output-csv", type=Path, default=Path("data/reports/homologation_report.csv"))

    args = parser.parse_args()

    if args.command == "inventory":
        _run_inventory(Path(args.root), args.output)
    elif args.command == "extract-xlsx":
        _run_extract_xlsx(Path(args.root), args.output)
    elif args.command == "analyze":
        _run_analyze(args.source_root, args.target_root, args.threshold, args.output_json, args.output_csv)


def _run_inventory(root: Path, output: Path | None) -> None:
    inventory = build_inventory(root)
    payload = inventory.to_dict()

    if output:
        output.parent.mkdir(parents=True, exist_ok=True)
        if output.suffix.lower() == ".csv":
            with output.open("w", newline="", encoding="utf-8") as file:
                writer = csv.DictWriter(file, fieldnames=list(inventory.entries[0].to_dict()))
                writer.writeheader()
                writer.writerows(entry.to_dict() for entry in inventory.entries)
        else:
            output.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    print(
        json.dumps(
            {
                "root": payload["root"],
                "total_files": payload["total_files"],
                "supported_files": payload["supported_files"],
                "empty_files": payload["empty_files"],
                "unsupported_files": payload["unsupported_files"],
                "ignored_files": payload["ignored_files"],
            },
            ensure_ascii=False,
            indent=2,
        )
    )


def _run_extract_xlsx(root: Path, output: Path) -> None:
    inventory = build_inventory(root)
    parser = XLSXParsingSyllabusGateway()
    subjects = []
    errors = []

    for entry in inventory.entries:
        if entry.status != "supported":
            continue
        try:
            subject = parser.extract_subject_from_syllabus(Path(entry.path))
        except ValueError as error:
            errors.append({"path": entry.to_dict()["relative_path"], "error": _safe_text(str(error))})
            continue

        subjects.append(
            {
                "path": entry.to_dict()["relative_path"],
                "program": subject.program or entry.program,
                "term": entry.to_dict()["term"],
                "name": subject.name,
                "objective": subject.objective,
                "problemic_core": subject.problemicCore,
                "didactic_strategies": subject.didacticStrategies,
                "competencies": [
                    {
                        "name": competency.name,
                        "learning_results": competency.learningResults,
                        "contents": competency.contents,
                        "time": competency.time,
                        "evaluation_mechanisms": competency.evaluationMechanisms,
                        "didactic_resources": competency.didacticResources,
                        "human_action_dimensions": {
                            "comprehend": competency.humanActionDimensions.comprehend,
                            "act": competency.humanActionDimensions.act,
                            "do": competency.humanActionDimensions.do,
                            "communicate": competency.humanActionDimensions.communicate,
                            "feel": competency.humanActionDimensions.feel,
                        },
                    }
                    for competency in subject.competencies
                ],
            }
        )

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps({"subjects": subjects, "errors": errors}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(json.dumps({"subjects": len(subjects), "errors": len(errors), "output": str(output)}, indent=2))


def _run_analyze(
    source_root: Path,
    target_root: Path,
    threshold: float,
    output_json: Path,
    output_csv: Path,
) -> None:
    source_subjects = _extract_subjects(source_root)
    target_subjects = _extract_subjects(target_root)
    report = analyze_homologation(source_subjects, target_subjects, threshold=threshold)

    write_json_report(report, output_json)
    write_csv_report(report, output_csv)

    print(
        json.dumps(
            {
                "source_subjects": report.total_source_subjects,
                "target_subjects": len(target_subjects),
                "homologable_subjects": report.homologable_subjects,
                "general_percentage": report.general_percentage,
                "threshold": report.threshold,
                "output_json": str(output_json),
                "output_csv": str(output_csv),
            },
            ensure_ascii=False,
            indent=2,
        )
    )


def _extract_subjects(root: Path) -> list[Subject]:
    inventory = build_inventory(root)
    parser = XLSXParsingSyllabusGateway()
    subjects: list[Subject] = []

    for entry in inventory.entries:
        if entry.status != "supported":
            continue
        subjects.append(parser.extract_subject_from_syllabus(Path(entry.path)))

    return subjects


def _safe_text(value: str) -> str:
    return value.encode("utf-8", errors="replace").decode("utf-8")


if __name__ == "__main__":
    main()

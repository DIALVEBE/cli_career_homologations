from __future__ import annotations

import csv
import json
from dataclasses import asdict
from pathlib import Path

from entities import CareerHomologationReport


def write_json_report(report: CareerHomologationReport, output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(asdict(report), ensure_ascii=False, indent=2), encoding="utf-8")


def write_csv_report(report: CareerHomologationReport, output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "source_program",
                "source_subject",
                "target_program",
                "best_target_subject",
                "source_credits",
                "target_credits",
                "score",
                "homologable",
                "threshold",
                "evidence",
            ],
        )
        writer.writeheader()
        for result in report.results:
            match = result.best_match
            writer.writerow(
                {
                    "source_program": report.source_program,
                    "source_subject": result.source_subject,
                    "target_program": report.target_program,
                    "best_target_subject": match.target_subject if match else "",
                    "source_credits": match.source_credits if match else "",
                    "target_credits": match.target_credits if match else "",
                    "score": match.score if match else "",
                    "homologable": match.homologable if match else False,
                    "threshold": report.threshold,
                    "evidence": " | ".join(match.evidence) if match else "",
                }
            )

from pathlib import Path

from services import build_inventory


def test_build_inventory_classifies_files(tmp_path: Path):
    raw = tmp_path / "data" / "raw"
    program = raw / "SYLLABUS_TEST" / "Semestre 1"
    program.mkdir(parents=True)
    supported = program / "subject.xlsx"
    empty = program / "empty.xlsx"
    unsupported = program / "subject.ods"
    ignored = program / "desktop.ini"

    supported.write_bytes(b"not empty")
    empty.write_bytes(b"")
    unsupported.write_bytes(b"not empty")
    ignored.write_bytes(b"not empty")

    inventory = build_inventory(raw)

    assert inventory.total_files == 4
    assert inventory.supported_files == 1
    assert inventory.empty_files == 1
    assert inventory.unsupported_files == 1
    assert inventory.ignored_files == 1
    assert inventory.entries[0].program == "SYLLABUS_TEST"
    assert inventory.entries[0].term == "Semestre 1"

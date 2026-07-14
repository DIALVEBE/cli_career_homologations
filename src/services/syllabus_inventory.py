from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path

SUPPORTED_EXTENSIONS = {".xlsx"}
KNOWN_UNSUPPORTED_EXTENSIONS = {".xlsb", ".ods"}
IGNORED_FILENAMES = {"desktop.ini"}


@dataclass(frozen=True)
class InventoryEntry:
    path: str
    relative_path: str
    program: str
    term: str | None
    extension: str
    size_bytes: int
    status: str
    reason: str | None = None

    def to_dict(self) -> dict[str, object]:
        payload = asdict(self)
        payload["path"] = _safe_text(self.path)
        payload["relative_path"] = _safe_text(self.relative_path)
        payload["program"] = _safe_text(self.program)
        if self.term is not None:
            payload["term"] = _safe_text(self.term)
        return payload


@dataclass(frozen=True)
class InventorySummary:
    root: str
    total_files: int
    supported_files: int
    empty_files: int
    unsupported_files: int
    ignored_files: int
    entries: list[InventoryEntry]

    def to_dict(self) -> dict[str, object]:
        return {
            "root": self.root,
            "total_files": self.total_files,
            "supported_files": self.supported_files,
            "empty_files": self.empty_files,
            "unsupported_files": self.unsupported_files,
            "ignored_files": self.ignored_files,
            "entries": [entry.to_dict() for entry in self.entries],
        }


def build_inventory(root: Path) -> InventorySummary:
    root = root.resolve()
    entries = [_build_entry(root, path) for path in sorted(root.rglob("*")) if path.is_file()]

    return InventorySummary(
        root=str(root),
        total_files=len(entries),
        supported_files=sum(entry.status == "supported" for entry in entries),
        empty_files=sum(entry.status == "empty" for entry in entries),
        unsupported_files=sum(entry.status == "unsupported" for entry in entries),
        ignored_files=sum(entry.status == "ignored" for entry in entries),
        entries=entries,
    )


def _build_entry(root: Path, path: Path) -> InventoryEntry:
    relative = path.resolve().relative_to(root)
    parts = relative.parts
    extension = path.suffix.lower()
    size_bytes = path.stat().st_size

    if path.name.lower() in IGNORED_FILENAMES:
        status = "ignored"
        reason = "ignored filename"
    elif size_bytes == 0:
        status = "empty"
        reason = "empty file"
    elif extension in SUPPORTED_EXTENSIONS:
        status = "supported"
        reason = None
    elif extension in KNOWN_UNSUPPORTED_EXTENSIONS:
        status = "unsupported"
        reason = f"{extension} support is not implemented yet"
    else:
        status = "unsupported"
        reason = "unknown file extension"

    return InventoryEntry(
        path=str(path.resolve()),
        relative_path=str(relative),
        program=_infer_program(parts),
        term=_infer_term(parts),
        extension=extension,
        size_bytes=size_bytes,
        status=status,
        reason=reason,
    )


def _infer_program(parts: tuple[str, ...]) -> str:
    if not parts:
        return "UNKNOWN"
    return parts[0]


def _infer_term(parts: tuple[str, ...]) -> str | None:
    for part in parts[1:-1]:
        normalized = part.lower()
        if "semestre" in normalized or "optativa" in normalized:
            return part
    return None


def _safe_text(value: str) -> str:
    return value.encode("utf-8", errors="replace").decode("utf-8")

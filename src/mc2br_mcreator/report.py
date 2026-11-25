"""Collect what was converted, approximated or skipped, and write it out."""

from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class Report:
    converted: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    unsupported: list[str] = field(default_factory=list)

    def ok(self, kind: str, name: str) -> None:
        self.converted.append(f"{kind} `{name}`")

    def warn(self, kind: str, name: str, message: str) -> None:
        self.warnings.append(f"{kind} `{name}`: {message}")

    def unmapped(self, kind: str, name: str, field_name: str) -> None:
        self.warn(kind, name, f"field `{field_name}` has no Bedrock mapping yet (skipped)")

    def skip(self, kind: str, name: str, reason: str) -> None:
        self.unsupported.append(f"{kind} `{name}`: {reason}")

    def to_markdown(self) -> str:
        def section(title: str, rows: list[str]) -> str:
            body = "\n".join(f"- {r}" for r in rows) if rows else "_None_"
            return f"## {title} ({len(rows)})\n\n{body}\n"

        return "\n".join([
            "# Conversion report\n",
            section("Converted", self.converted),
            section("Warnings", self.warnings),
            section("Not converted", self.unsupported),
        ])

    def write(self, path: Path) -> None:
        path.write_text(self.to_markdown(), encoding="utf-8")

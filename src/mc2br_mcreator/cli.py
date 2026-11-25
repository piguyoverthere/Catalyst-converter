"""Command line entry point: `mc2br <workspace> -o <out>`."""

from pathlib import Path

import click

from .emitters import emit_mod
from .package import make_mcaddon
from .parsers import parse_workspace
from .report import Report
from .workspace import load_workspace


def convert(workspace: Path, out: Path) -> tuple[Path, Report]:
    """Run the whole pipeline: load -> parse -> emit -> package -> report."""
    report = Report()
    ws = load_workspace(workspace)
    mod = parse_workspace(ws, report)
    bp, rp = emit_mod(mod, out, report)
    addon = make_mcaddon([bp, rp], out / f"{mod.namespace}.mcaddon")
    report.write(out / "report.md")
    return addon, report


@click.command()
@click.argument("workspace", type=click.Path(exists=True, file_okay=False, path_type=Path))
@click.option("-o", "--out", default="out", show_default=True,
              type=click.Path(file_okay=False, path_type=Path), help="Output folder")
def main(workspace: Path, out: Path) -> None:
    """Convert an MCreator WORKSPACE folder into a Bedrock .mcaddon."""
    addon, report = convert(workspace, out)
    click.echo(f"Converted: {len(report.converted)}  Warnings: {len(report.warnings)}  "
               f"Not converted: {len(report.unsupported)}")
    click.echo(f"Add-on: {addon}")
    click.echo(f"Report: {out / 'report.md'}")


if __name__ == "__main__":
    main()

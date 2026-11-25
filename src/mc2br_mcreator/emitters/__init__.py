"""Write a Mod (IR) out as a Bedrock behavior pack and resource pack."""

import shutil
from pathlib import Path

from ..ir import Mod
from ..report import Report
from .item import emit_items
from .manifest import bp_manifest, rp_manifest
from .util import write_json


def emit_mod(mod: Mod, out: Path, report: Report) -> tuple[Path, Path]:
    """Create out/<ns>_BP and out/<ns>_RP. Returns their paths."""
    bp = out / f"{mod.namespace}_BP"
    rp = out / f"{mod.namespace}_RP"
    for folder in (bp, rp):
        if folder.exists():
            shutil.rmtree(folder)   # start clean so deleted items don't linger

    write_json(bp / "manifest.json", bp_manifest(mod))
    write_json(rp / "manifest.json", rp_manifest(mod))
    emit_items(mod, bp, rp, report)
    return bp, rp

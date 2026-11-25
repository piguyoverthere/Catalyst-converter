"""Zip the behavior and resource packs into one .mcaddon file."""

import zipfile
from pathlib import Path


def make_mcaddon(packs: list[Path], dest: Path) -> Path:
    dest.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(dest, "w", zipfile.ZIP_DEFLATED) as zf:
        for pack in packs:
            for f in sorted(pack.rglob("*")):
                if f.is_file():
                    # Keep the pack folder name inside the zip: <ns>_BP/manifest.json
                    zf.write(f, f.relative_to(pack.parent).as_posix())
    return dest

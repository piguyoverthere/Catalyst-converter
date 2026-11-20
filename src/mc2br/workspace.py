"""find and load the files in an workspace."""

import json
import re
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Element:
    name: str          # file name without ".mod.json", e.g. "RubyItem"
    type: str          # MCreator element type, e.g. "item"
    definition: dict   # the element's settings
    path: Path


@dataclass
class Workspace:
    root: Path
    mod_id: str
    mod_name: str
    version: tuple[int, int, int]

    def elements(self):
        """Yield every mod element in the workspace's elements/ folder."""
        for f in sorted((self.root / "elements").glob("*.mod.json")):
            data = json.loads(f.read_text(encoding="utf-8"))
            yield Element(
                name=f.name.removesuffix(".mod.json"),
                type=data.get("_type", "unknown"),
                definition=data.get("definition", {}),
                path=f,
            )

    def find_texture(self, texture_name: str | None, kind: str = "item") -> Path | None:
        """Locate a texture PNG by its MCreator name (e.g. "ruby")."""
        if not texture_name:
            return None
        candidates = [
            self.root / "src/main/resources/assets" / self.mod_id / "textures" / kind / f"{texture_name}.png",
            self.root / "src/main/resources/assets" / self.mod_id / "textures" / f"{kind}s" / f"{texture_name}.png",
        ]
        for c in candidates:
            if c.exists():
                return c
        # Fall back to searching anywhere in the workspace.
        return next(self.root.rglob(f"{texture_name}.png"), None)


def _parse_version(text: str) -> tuple[int, int, int]:
    nums = [int(n) for n in re.findall(r"\d+", text or "")][:3]
    return tuple((nums + [1, 0, 0][len(nums):])[:3]) if nums else (1, 0, 0)


def load_workspace(root: Path) -> Workspace:
    """Read the .mcreator file for the mod id, name and version."""
    root = Path(root)
    settings: dict = {}
    mcreator_files = list(root.glob("*.mcreator"))
    if mcreator_files:
        data = json.loads(mcreator_files[0].read_text(encoding="utf-8"))
        settings = data.get("workspaceSettings", {})
    mod_id = settings.get("modid") or re.sub(r"[^a-z0-9_]", "_", root.name.lower())
    return Workspace(
        root=root,
        mod_id=mod_id,
        mod_name=settings.get("modName") or root.name,
        version=_parse_version(settings.get("version", "")),
    )

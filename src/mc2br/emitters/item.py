"""IR Item -> Bedrock item files.

For each item this writes:
  BP/items/<id>.json              the item definition and its components
  RP/textures/items/<id>.png      the texture, copied from the workspace
  RP/textures/item_texture.json   the atlas that links icon names to textures
"""

import shutil
from pathlib import Path

from ..ir import Item, Mod
from ..report import Report
from .util import write_json

ITEM_FORMAT_VERSION = "1.21.40"


def item_json(mod: Mod, item: Item) -> dict:
    components = {
        "minecraft:display_name": {"value": item.display_name},
        **item.components,
    }
    if item.texture is not None:
        components["minecraft:icon"] = {"textures": {"default": f"{mod.namespace}_{item.id}"}}
    return {
        "format_version": ITEM_FORMAT_VERSION,
        "minecraft:item": {
            "description": {
                "identifier": f"{mod.namespace}:{item.id}",
                "menu_category": {"category": "items"},
            },
            "components": components,
        },
    }


def emit_items(mod: Mod, bp: Path, rp: Path, report: Report) -> None:
    atlas: dict = {}
    for item in mod.items:
        write_json(bp / "items" / f"{item.id}.json", item_json(mod, item))
        if item.texture is not None:
            dest = rp / "textures" / "items" / f"{item.id}.png"
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(item.texture, dest)
            atlas[f"{mod.namespace}_{item.id}"] = {"textures": f"textures/items/{item.id}"}
        report.ok("item", f"{mod.namespace}:{item.id}")

    if atlas:
        write_json(rp / "textures" / "item_texture.json", {
            "resource_pack_name": mod.namespace,
            "texture_name": "atlas.items",
            "texture_data": atlas,
        })

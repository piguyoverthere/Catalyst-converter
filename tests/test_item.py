import json
import zipfile
from pathlib import Path

from mc2br.cli import convert
from mc2br.mapping import apply_mapping
from mc2br.parsers.item import to_identifier

FIXTURE = Path(__file__).parent / "fixtures" / "simple_mod"


def test_identifier_is_snake_case():
    assert to_identifier("RubyItem") == "ruby_item"
    assert to_identifier("Ruby Gem!") == "ruby_gem_"


def test_mapping_wraps_clamps_and_skips():
    mapping = {
        "fields": {
            "stackSize": {"component": "minecraft:max_stack_size", "max": 64},
            "damageCount": {"component": "minecraft:durability",
                            "wrap": "max_durability", "skip_if": 0},
        },
        "handled": ["name"],
    }
    components, unmapped = apply_mapping(
        {"name": "x", "stackSize": 99, "damageCount": 250, "mystery": 1}, mapping)
    assert components == {
        "minecraft:max_stack_size": 64,
        "minecraft:durability": {"max_durability": 250},
    }
    assert unmapped == ["mystery"]


def test_convert_fixture(tmp_path):
    addon, report = convert(FIXTURE, tmp_path)

    item = json.loads((tmp_path / "simple_mod_BP/items/ruby_item.json").read_text())
    body = item["minecraft:item"]
    assert body["description"]["identifier"] == "simple_mod:ruby_item"
    comps = body["components"]
    assert comps["minecraft:display_name"] == {"value": "Ruby"}
    assert comps["minecraft:max_stack_size"] == 64
    assert comps["minecraft:glint"] is True
    assert "minecraft:durability" not in comps          # damageCount 0 is skipped
    assert comps["minecraft:icon"] == {"textures": {"default": "simple_mod_ruby_item"}}

    assert (tmp_path / "simple_mod_RP/textures/items/ruby_item.png").exists()

    # Unknown fields and unsupported element types end up in the report.
    assert any("rarity" in w for w in report.warnings)
    assert any("RubySword" in u for u in report.unsupported)

    # BP and RP manifests depend on each other.
    bp = json.loads((tmp_path / "simple_mod_BP/manifest.json").read_text())
    rp = json.loads((tmp_path / "simple_mod_RP/manifest.json").read_text())
    assert bp["dependencies"][0]["uuid"] == rp["header"]["uuid"]
    assert rp["dependencies"][0]["uuid"] == bp["header"]["uuid"]

    with zipfile.ZipFile(addon) as zf:
        names = zf.namelist()
    assert "simple_mod_BP/manifest.json" in names
    assert "simple_mod_RP/textures/items/ruby_item.png" in names

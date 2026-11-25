"""Load the YAML replacement keys and apply them to MCreator data."""

from functools import cache
from pathlib import Path

import yaml

MAPPINGS_DIR = Path(__file__).parent / "mappings"


@cache
def load_mapping(name: str) -> dict:
    """Load mappings/<name>.yaml (cached, so each file is read once)."""
    with open(MAPPINGS_DIR / f"{name}.yaml", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def apply_mapping(definition: dict, mapping: dict) -> tuple[dict, list[str]]:
    """Turn MCreator fields into Bedrock components using a mapping.

    Returns (components, unmapped_field_names).
    """
    rules = mapping.get("fields", {})
    known = set(mapping.get("handled", [])) | set(mapping.get("ignored", []))
    components: dict = {}
    unmapped: list[str] = []

    for key, value in definition.items():
        rule = rules.get(key)
        if rule is None:
            if key not in known:
                unmapped.append(key)
            continue
        if "skip_if" in rule and value == rule["skip_if"]:
            continue
        if "max" in rule and isinstance(value, (int, float)):
            value = min(value, rule["max"])
        if "value" in rule:
            value = rule["value"]
        if "wrap" in rule:
            value = {rule["wrap"]: value, **rule.get("extra", {})}
        components[rule["component"]] = value

    return components, unmapped

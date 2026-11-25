"""MCreator "item" element -> IR Item."""

import re

from ..ir import Item
from ..mapping import apply_mapping, load_mapping
from ..report import Report
from ..workspace import Element, Workspace


def to_identifier(name: str) -> str:
    """"RubyItem" -> "ruby_item" (Bedrock ids are lowercase snake_case)."""
    snake = re.sub(r"(?<=[a-z0-9])(?=[A-Z])", "_", name)
    return re.sub(r"[^a-z0-9_]", "_", snake.lower())


def texture_name(raw) -> str | None:
    """MCreator stores textures as a plain string or as {"texture": "..."}."""
    if isinstance(raw, dict):
        raw = raw.get("texture") or raw.get("name")
    return raw or None


def parse_item(element: Element, ws: Workspace, report: Report) -> Item:
    d = element.definition
    components, unmapped = apply_mapping(d, load_mapping("items"))
    for field_name in unmapped:
        report.unmapped("item", element.name, field_name)

    tex_name = texture_name(d.get("texture"))
    texture = ws.find_texture(tex_name, "item")
    if tex_name and texture is None:
        report.warn("item", element.name, f"texture `{tex_name}` not found in workspace")

    return Item(
        id=to_identifier(element.name),
        display_name=d.get("name") or element.name,
        texture=texture,
        components=components,
    )

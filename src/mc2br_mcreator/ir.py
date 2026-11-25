"""Intermediate representation (IR).

Parsers turn MCreator data into these classes, and emitters turn these classes
into Bedrock files. Keeping this layer platform-neutral means a parser never
needs to know about Bedrock, and an emitter never needs to know about MCreator.
"""

from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class Item:
    id: str                                   # e.g. "ruby" (no namespace)
    display_name: str                         # e.g. "Ruby"
    texture: Path | None = None               # PNG file inside the MCreator workspace
    components: dict = field(default_factory=dict)  # Bedrock components from the mapping


@dataclass
class Mod:
    namespace: str                            # MCreator mod id, becomes the Bedrock namespace
    name: str                                 # human-readable mod name
    version: tuple[int, int, int] = (1, 0, 0)
    items: list[Item] = field(default_factory=list)

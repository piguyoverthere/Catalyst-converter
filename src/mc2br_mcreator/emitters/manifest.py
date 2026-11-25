"""Build manifest.json for the behavior pack (BP) and resource pack (RP)."""

import uuid

from ..ir import Mod

MIN_ENGINE_VERSION = [1, 21, 40]

# Fixed namespace so the same mod always gets the same UUIDs. That lets Bedrock
# treat a re-converted add-on as an update instead of a second copy.
_NS = uuid.UUID("6f1c2d3e-4b5a-4c6d-8e7f-9a0b1c2d3e4f")


def pack_uuid(mod: Mod, role: str) -> str:
    return str(uuid.uuid5(_NS, f"{mod.namespace}:{role}"))


def _manifest(mod: Mod, kind: str, module_type: str, depends_on: str) -> dict:
    version = list(mod.version)
    return {
        "format_version": 2,
        "header": {
            "name": f"{mod.name} {kind}",
            "description": "Converted from MCreator by mc2br",
            "uuid": pack_uuid(mod, f"{kind}-header"),
            "version": version,
            "min_engine_version": MIN_ENGINE_VERSION,
        },
        "modules": [
            {"type": module_type, "uuid": pack_uuid(mod, f"{kind}-module"), "version": version}
        ],
        "dependencies": [{"uuid": depends_on, "version": version}],
    }


def bp_manifest(mod: Mod) -> dict:
    return _manifest(mod, "BP", "data", pack_uuid(mod, "RP-header"))


def rp_manifest(mod: Mod) -> dict:
    return _manifest(mod, "RP", "resources", pack_uuid(mod, "BP-header"))

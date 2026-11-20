"""Parser registry: MCreator element type -> parser function.

To support a new element type, write parsers/<type>.py and add it here.
"""

from ..ir import Mod
from ..report import Report
from ..workspace import Workspace
from .item import parse_item

PARSERS = {
    "item": ("items", parse_item),
}


def parse_workspace(ws: Workspace, report: Report) -> Mod:
    mod = Mod(namespace=ws.mod_id, name=ws.mod_name, version=ws.version)
    for element in ws.elements():
        entry = PARSERS.get(element.type)
        if entry is None:
            report.skip(element.type, element.name, "element type not supported yet")
            continue
        list_name, parser = entry
        getattr(mod, list_name).append(parser(element, ws, report))
    return mod

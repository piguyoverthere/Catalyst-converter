# Catalyst Converter (mc2br)

__\[work in progress\]__
__\[\#\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\]__

Converts NeoForge workspaces into Minecraft Bedrock add-ons (`.mcaddon`). Also has support for MCreator workspaces

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

## Usage

```bash
mc2br path/to/workspace -o out
```

Output in `out/`:

- `<modid>_BP/`, `<modid>_RP/`: the behavior and resource packs
- `<modid>.mcaddon`: both packs zipped; double-click to import into Minecraft
- `report.md`: what was converted, what was skipped, and why

## MCreator edition

It reads MCreator's own element files (`elements/*.mod.json`) instead of the
generated Java, turns them into a platform-neutral intermediate representation,
and writes a Bedrock behavior pack and resource pack.

### Supported so far

| MCreator element | Status |
|---|---|
| Item | Name, texture, stack size, durability, enchantability, glint |
| Everything else | Listed in the report as "not converted" |

## Project layout

```
src/mc2br/
  take-input.py    what you actually run in the terminal
  catalyst-base/   contains recodings for elements for java parity and customizability
    behavior-pack/...
    resource-pack/...
  mcreator/
    workspace.py   finds and reads MCreator files
    ir.py          platform-neutral data classes
    mapping.py     applies the YAML replacement keys
    mappings/...   the replacement keys (MCreator field -> Bedrock component)
    parsers/...    MCreator element -> IR, one file per element type
    emitters/...   IR -> Bedrock JSON files
    package.py     zips packs into .mcaddon
    report.py      conversion report
    cli.py         the `mc2br` command
  neoforge/
    identify.py    simplifies workspace into JSON and identifies mod element types
  ollama/
    ollama.py      AI fallback for unknown mod elements, requires a beefy computer and --use-ollama in take-input.py
    training-data/...
```

## Tests

```bash
pytest
```


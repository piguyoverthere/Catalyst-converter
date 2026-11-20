# Catalyst Converter (mc2br)

Converts MCreator (NeoForge) workspaces into Minecraft Bedrock add-ons (`.mcaddon`).

It reads MCreator's own element files (`elements/*.mod.json`) instead of the
generated Java, turns them into a platform-neutral intermediate representation,
and writes a Bedrock behavior pack and resource pack.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

## Usage

```bash
mc2br path/to/MCreatorWorkspace -o out
```

Output in `out/`:

- `<modid>_BP/`, `<modid>_RP/`: the behavior and resource packs
- `<modid>.mcaddon`: both packs zipped; double-click to import into Minecraft
- `report.md`: what was converted, what was skipped, and why

## Supported so far

| MCreator element | Status |
|---|---|
| Item | Name, texture, stack size, durability, enchantability, glint |
| Everything else | Listed in the report as "not converted" |

## Project layout

```
src/mc2br/
  workspace.py   finds and reads MCreator files
  ir.py          platform-neutral data classes
  mapping.py     applies the YAML replacement keys
  mappings/      the replacement keys (MCreator field -> Bedrock component)
  parsers/       MCreator element -> IR, one file per element type
  emitters/      IR -> Bedrock JSON files
  package.py     zips packs into .mcaddon
  report.py      conversion report
  cli.py         the `mc2br` command
```

## Tests

```bash
pytest
```

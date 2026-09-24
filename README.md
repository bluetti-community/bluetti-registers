# bluetti-registers

Register maps for BLUETTI power stations, covering both the Bluetooth app
protocol (`bluetooth/`) and Modbus TCP (`modbus-tcp/`). One JSON file per
device, plus a combined JSON per protocol attached to every release.

Currently: 27 devices over Bluetooth, 8 over Modbus TCP.

Want to add or fix a register, including from real hardware you own? See
[CONTRIBUTING.md](CONTRIBUTING.md) — no coding experience required to help.

## Credits

This repository is a fork of
[Patrick762/bluetti-registers](https://github.com/Patrick762/bluetti-registers),
created and maintained by [Patrick762](https://github.com/Patrick762), who
built the original register tables, the CSV-to-JSON pipeline and the JSON
Schemas that this repository still runs on. The Bluetooth register data is
essentially his work.

The fork exists to let several people with different hardware iterate quickly
on the Modbus TCP side; it is not a fork in opposition. The upstream repository
is still actively developed and worth following. Original work is MIT-licensed
and the copyright notice is unchanged — see [LICENSE](LICENSE).

> **Note on version tags.** `0.0.20` is the last tag shared with upstream.
> Later `0.0.x` tags exist in both repositories with different content, so pin
> releases by repository URL, not by version number alone.
>
> The generated files differ too: upstream builds a single `devices.json`,
> this repository builds one file per protocol, in a different shape. They are
> not interchangeable.

## Consuming the data

Every [release](../../releases) carries two files, `bluetooth.json` and
`modbus-tcp.json`, each holding every device of that protocol. Fetch one by
tag, never from `main`, which can be mid-change:

```
https://github.com/bluetti-community/bluetti-registers/releases/download/<tag>/modbus-tcp.json
```

The per-device files are not on the release; they live in the tree, and are
pinned the same way. The Python library
[bluetti-modbus](https://github.com/bluetti-community/bluetti-modbus) is the
largest consumer of the Modbus TCP data and imports it exactly as above.

The GitHub Pages site publishes the **JSON Schemas** from `schemas/`, not the
register data. Every device file names one in its `$schema` key, which is what
`validate.py` and an editor's live validation resolve.

`examples/` contains a short worked example of importing a generated file from
another project (currently Node.js/TypeScript).

## Naming convention for field names

1. Type (PV/AC/DC/Grid/Device/Battery) (short: pv/ac/dc/g/d/b)

2. Phase/String/Battery number if available

3. in/out (short: i/o) or destination

4. power/voltage/current/energy/frequency/temperature (short: p/v/c/e/f/t)

5. **total** / **avg** (if total over all phases/strings or average over all
   cells)

## Repository layout

- `bluetooth/` and `modbus-tcp/` — one CSV per protocol (`bluetooth.csv`,
  `modbus-tcp.csv`), plus one JSON file per device.
- `schemas/` — JSON Schema files describing the generated JSON's shape,
  published as a static site via GitHub Pages.
- `examples/` — short examples showing how to consume a generated JSON file
  from another project.
- `fields.py` — the shared field catalogue: name, type, unit, scale and
  metadata for every field the CSVs can reference.
- `generate-from-csv.py`, `generate.py`, `validate.py`, `helpers.py` — the
  pipeline: per-device files, the combined per-protocol files, validation, and
  the shared paths and schema URL.

## Workflow

1. Add registers to the relevant CSV (`bluetooth/bluetooth.csv` or
   `modbus-tcp/modbus-tcp.csv`), adding the field to `fields.py` first if it's
   new.
2. Generate the per-device JSON files with `generate-from-csv.py`.
3. Validate with `validate.py`.
4. Commit both the CSV and the regenerated JSON, and open a pull request —
   validation runs on every PR.

`generate.py` builds the combined per-protocol files (`out/bluetooth.json`,
`out/modbus-tcp.json`) that are attached to releases. You don't normally need
to run it by hand; CI does it on tag.

> **Exception:** `modbus-tcp/smeter.json` is maintained by hand and has no row
> in `modbus-tcp.csv`. Edit that file directly and don't regenerate it from the
> CSV, or it will be lost.

## Where the data comes from

Fields carry a `contributors` list recording who established them. Sources
differ in confidence and it's worth knowing which is which:

- BLUETTI's official Cassandra Protocol register table, which covers most of
  the Balco260/Balco500/EP2000 Modbus map.
- Readings confirmed against real hardware. Where these contradict the official
  table, hardware wins and the commit message says so.
- Reverse engineering of the Bluetooth app protocol, which is where the
  `bluetooth/` data originates.

Pre-release tags (`ac500-beta-*`, `balco500-beta-*`) exist so owners of a given
device can test a register map before it lands in a stable release.

⚠️ **If you plan to probe registers yourself, read the warning in
[CONTRIBUTING.md](CONTRIBUTING.md) first.** At least one device has had its
socket pool exhausted by rapid successive TCP connections on port 502,
requiring a factory reset. Out-of-range addresses may reset the connection
instead of returning a Modbus exception. Pace any scanning well below what a
normal scanner would do.

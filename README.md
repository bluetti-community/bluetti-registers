# bluetti-registers

A JSON file containing all known Bluetti registers, for both the Bluetooth
app protocol (`bluetooth/`) and Modbus TCP (`modbus-tcp/`).

Just import registers using the JSON file of a release. The JSON Schemas
describing their shape (see `schemas/`) are also published as a browsable
site via GitHub Pages (`.github/workflows/static.yml`).

## Naming convention for field names

1. Type (PV/AC/DC/Grid/Device/Battery) (short: pv/ac/dc/g/d/b)

2. Phase/String/Battery number if available

3. in/out (short: i/o) or destination

4. power/voltage/current/energy/frequency/temperature (short: p/v/c/e/f/t)

5. **total** / **avg** (if total over all phases/strings or average over all cells)

## Repository layout

- `bluetooth/` and `modbus-tcp/` - one CSV per protocol (`bluetooth.csv`,
  `modbus-tcp.csv`), plus one generated JSON file per device.
- `schemas/` - JSON Schema files describing the generated JSON's shape,
  published as a static site via GitHub Pages.
- `examples/` - short examples showing how to consume a generated JSON file
  from another project (currently: Node.js/TypeScript).

## Workflow

1. Add registers to the relevant CSV (`bluetooth/bluetooth.csv` or
   `modbus-tcp/modbus-tcp.csv`)
2. Generate JSON files using `generate-from-csv.py`
3. Validate JSON files using `validate.py`
4. Git commit and push

The full JSON files (one per protocol, covering every device) can be built
using `generate.py`.

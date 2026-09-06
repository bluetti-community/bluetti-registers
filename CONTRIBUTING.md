# Contributing

This repository is the source of truth for every register definition used across the
bluetti-community projects (`bluetti-modbus` generates its device classes from here;
`hassio-bluetti-modbus` vendors that in turn). There is no static per-model datasheet baked in
anywhere downstream - every field here was confirmed by someone comparing a real device's raw
Modbus/Bluetooth values against BLUETTI's own documentation and/or the Bluetti app. A fix here
propagates to every project that consumes it.

**Not a developer, or don't know Python?** The hardest part of contributing here is almost never
writing the JSON/CSV - it's gathering real-device evidence that a field's address, width, sign, or
scale is right. See [bluetti-modbus's HARDWARE_TESTING.md][hardware-testing] for a no-coding
guide to testing your own device, including prompts you can hand directly to an AI assistant. Come
back here once you have real numbers to report.

## Repository layout

See the [README](README.md) for the full layout and naming convention. In short:
`bluetooth/bluetooth.csv` and `modbus-tcp/modbus-tcp.csv` are the actual source data - one row per
device, one column per field name, each cell holding that field's register address for that
device (blank = the device doesn't have it). `fields.py` defines what each field *name* means
(content type, unit, scale, writability) - shared across every device that has a column with that
name.

## Adding or fixing a field

1. Edit the relevant CSV (`bluetooth/bluetooth.csv` or `modbus-tcp/modbus-tcp.csv`):
   - New field: add a column, fill in the address for every device that has it, leave others
     blank.
   - Fixing an address: edit the cell for the specific device row.
   - Add your GitHub handle (`@yourname`) to that device's `contributors` cell if it isn't already
     there - `validate.py` requires at least one contributor per device, and this is how real
     verification work gets credited. Multiple contributors are **space**-separated (not comma -
     `generate-from-csv.py` splits each CSV line on `,` first, then splits the contributors cell
     on ` `, so a comma inside it would be parsed as a new column).
2. If the field's *type* (content, unit, scale, range, or writability) needs to change, that's in
   `fields.py`, not the CSV - the CSV only carries addresses. Most fields are handled by name in
   one place; if the same field name needs to behave differently on one specific device (a
   narrower writable range, a different content type), `create_field`/`create_special_fields`
   both accept the device name and support scoping a `case` to it - see the existing
   `if device == "Balco260":` blocks in `fields.py` for the pattern. Don't widen a device-specific
   fix to every device sharing that field name unless you have evidence it applies there too.
3. Regenerate the JSON files:
   ```
   python3 generate-from-csv.py
   ```
4. Validate:
   ```
   python3 validate.py
   ```
5. Commit the CSV change together with the regenerated JSON file(s) - both belong in the same
   commit, since the JSON is a generated artifact of the CSV, not independent state.

## What a good fix includes

Reference real evidence in the field/commit, the way this project's own history does it - a raw
register scan, a comparison against BLUETTI's official register list, a mathematical cross-check
between related fields, or (for Bluetooth) a packet capture. "Confirmed by BLUETTI support" or a
link to the issue where someone tested it is exactly the kind of provenance worth keeping, either
as a short code comment in `fields.py` or in the PR description - future contributors (human or
AI) rely on it to know a field's behavior is verified rather than guessed.

## Submitting a change

Open a pull request against `main`. Keep it focused - one field/device fix per PR is easier to
verify and revert than a bundle of unrelated changes. CI (`build.yml`) runs `validate.py` on every
PR; a tagged release (which downstream projects like `bluetti-modbus` pin to) is cut by a
maintainer once changes on `main` are ready to ship.

[hardware-testing]: https://github.com/bluetti-community/bluetti-modbus/blob/main/HARDWARE_TESTING.md

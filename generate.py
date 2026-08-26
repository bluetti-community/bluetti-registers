import os
import json
from jsonschema import validate

from helpers import (
    getDevicesModbusTcp,
    getDevicesBluetooth,
    load_schema,
)

if not os.path.exists("out"):
    os.makedirs("out")

print("Loading devices list schema")

schema, registry = load_schema("all-devices.json")

print("Getting device files")

# region Bluetooth

result = []

# Load device files
for f in getDevicesBluetooth():
    print(f"Loading device definition {f}")

    with open(f, "r") as f:
        data = json.load(f)
        del data["$schema"]
        result.append(data)

    print("added to result")

print("Validating output")

validate(result, schema=schema, registry=registry)

print("Writing result to file")

with open("./out/bluetooth.json", "w") as f:
    f.write(json.dumps(result))

# region Modbus TCP

device_files = getDevicesModbusTcp()

result = []

for f in device_files:
    print(f"Loading device definition {f}")

    with open(f, "r") as f:
        data = json.load(f)
        del data["$schema"]
        result.append(data)

    print("added to result")

print("Validating output")

validate(result, schema=schema, registry=registry)

print("Writing result to file")

with open("./out/modbus-tcp.json", "w") as f:
    f.write(json.dumps(result))

print("Done")

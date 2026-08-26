import json
from jsonschema import validate

from helpers import getDevicesBluetooth, getDevicesModbusTcp, load_schema

print("Loading device schema")

schema, registry = load_schema("device.json")

print("Getting device files")

device_files = getDevicesBluetooth()

for f in device_files:
    print(f"Loading device definition {f}")

    with open(f) as f:
        data = json.load(f)

    print("Validating")

    validate(data, schema=schema, registry=registry)

    if len(data["contributors"]) == 0:
        raise Exception(f'Contributors for device {data["name"]} missing')

    print("Device validation complete")

device_files = getDevicesModbusTcp()

for f in device_files:
    print(f"Loading device definition {f}")

    with open(f) as f:
        data = json.load(f)

    print("Validating")

    validate(data, schema=schema, registry=registry)

    print("Device validation complete")

print("Done")

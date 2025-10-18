#!/usr/bin/env python3
import subprocess
import json

version = (
    subprocess.check_output("midclt call system.version", shell=True).rstrip().decode()
)
product = (
    subprocess.check_output("midclt call system.product_type", shell=True)
    .rstrip()
    .decode()
)
[product_type, version] = version.split("-", maxsplit=1)
if int(version.split(".")[0]) <= 25 and int(version.split(".")[1]) < 10:
    update_available = json.loads(
        subprocess.check_output("midclt call update.check_available", shell=True)
    )
    pending_update = (
        None
        if update_available["status"] != "UNAVAILABLE"
        else update_available["status"]
    )
else:
    update_available = json.loads(
        subprocess.check_output("midclt call update.status", shell=True)
    )
    pending_update = (
        "None"
        if "new_version" not in update_available
        else update_available["new_version"]
    )
update_status = 1 if not pending_update else 0
print(f'{update_status} "{product_type} Version" version={version}|update={pending_update}')
print(f'0 "Product" - {product}')

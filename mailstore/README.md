# CheckMK Mailstore

> Simple Localcheck-Returns w/o any further Integration 
> https://docs.checkmk.com/latest/en/localchecks.html

- Version - Check Current Version against possible Download from Mailstore-Site
- Licenses - Get License-Count/Usage
- Profiles - Retrieve Profile-Count and Check last Run-Result

## Installation

- Put content in e.g. `/opt/mailstore_check/`
- Create a script in `/usr/lib/check_mk_agent/local/3600`

```
cat << EOF >/usr/lib/check_mk_agent/local/3600/mailstore
#!/bin/sh
python3 /opt/mailstore_check/mailstore.py
EOF
chmod +x /usr/lib/check_mk_agent/local/3600/mailstore
```
> Every hour should be enough...
> https://docs.checkmk.com/latest/en/localchecks.html#cache

- Install Python-Library if missing:
  - `apt-get install python3-requests`

After first run of `mailstore.py` a default Configuration will be created.


`mgmt.py` from https://help.mailstore.com/en/server/Python_API_Wrapper_Tutorial

# vpn-config-diff-tool

Diff two VPN config files and list what changed: CHANGED when a key is in both files with a different value, ADDED when it is only in the new file, REMOVED when it is only in the old file — differences listed alphabetically by key, with a summary. Config lines are "key value" (or "key=value"); blank lines and "#" comments are ignored.

Sample input is included (sample-old.conf and sample-new.conf).

## How to run

```sh
python3 main.py sample-old.conf sample-new.conf
```

## Example output

```
ADDED auth-user-pass: 
CHANGED cipher: AES-256-GCM -> AES-128-GCM
CHANGED remote: vpn1.company.local 1194 -> vpn2.company.local 1194
CHANGED route: 10.0.1.0 255.255.255.0 -> 10.0.5.0 255.255.255.0
4 difference(s): 3 changed, 1 added, 0 removed.
```

Standard library only. Run the tests with `python3 -m unittest discover`.

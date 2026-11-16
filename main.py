"""Diff two VPN config files and list what changed.

Usage: python3 main.py old.conf new.conf
Config lines are "key value" (or "key=value"); blank lines and
lines starting with "#" are ignored. The key is the first word on
the line, the rest is the value; a key with no value counts as a
flag (value "").
- CHANGED: the key is in both files with a different value.
- ADDED: the key is only in the new file.
- REMOVED: the key is only in the old file.
Differences are listed alphabetically by key, then a summary.
"""
import argparse, sys

def parse(text):
    settings = {}
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" in line and " " not in line.split("=", 1)[0]:
            key, value = line.split("=", 1)
            settings[key.strip()] = value.strip()
        else:
            parts = line.split(None, 1)
            settings[parts[0]] = parts[1].strip() if len(parts) > 1 else ""
    return settings

def diff(old, new):
    out = []
    for key in sorted(set(old) | set(new)):
        if key in old and key in new:
            if old[key] != new[key]:
                out.append(("CHANGED", key, old[key], new[key]))
        elif key in new:
            out.append(("ADDED", key, "", new[key]))
        else:
            out.append(("REMOVED", key, old[key], ""))
    return out

def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("old")
    parser.add_argument("new")
    args = parser.parse_args(argv)
    with open(args.old, encoding="utf-8") as f:
        old = parse(f.read())
    with open(args.new, encoding="utf-8") as f:
        new = parse(f.read())
    results = diff(old, new)
    for kind, key, old_value, new_value in results:
        if kind == "CHANGED":
            print(f"CHANGED {key}: {old_value} -> {new_value}")
        elif kind == "ADDED":
            print(f"ADDED {key}: {new_value}")
        else:
            print(f"REMOVED {key}: {old_value}")
    kinds = [r[0] for r in results]
    print(f"{len(results)} difference(s): {kinds.count('CHANGED')} changed, "
          f"{kinds.count('ADDED')} added, {kinds.count('REMOVED')} removed.")
    return 0

if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Compare server.json with the live server's serverInfo before publishing. No tool calls or API credentials."""

import importlib.util
import json
import sys
import urllib.error
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIELDS = ("version", "title", "description", "websiteUrl", "icons")


def load_discover():
    spec = importlib.util.spec_from_file_location("discover", ROOT / "examples" / "discover.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def mismatches(record, server_info):
    return [field for field in FIELDS if record.get(field) != server_info.get(field)]


def main(discover_module=None):
    record = json.loads((ROOT / "server.json").read_text(encoding="utf-8"))
    module = discover_module or load_discover()
    # Check the endpoint the record advertises, not the example's default.
    module.ENDPOINT = record["remotes"][0]["url"]
    try:
        server_info = module.discover()["serverInfo"]
    except (urllib.error.URLError, ValueError, TimeoutError) as error:
        print(f"Discovery failed: {error}", file=sys.stderr)
        return 1
    bad = mismatches(record, server_info)
    for field in bad:
        print(f"{field}: server.json has {record.get(field)!r}, the live server has {server_info.get(field)!r}",
              file=sys.stderr)
    if not bad:
        print(f"server.json matches {module.ENDPOINT} at version {record['version']}")
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Domain availability check for name-wizard.

Calls the public Revved domain status API and prints results in a stable
format the slash command can consume directly. No third-party dependencies.

Usage:
    check_domains.py foo.com bar.io baz.app
    check_domains.py foo.com,bar.io,baz.app
    echo "foo.com bar.io" | check_domains.py -

Output (one line per domain):
    foo.com: AVAILABLE
    bar.io: taken
    baz.app: AVAILABLE
"""
from __future__ import annotations

import json
import sys
import urllib.error
import urllib.parse
import urllib.request

API_URL = "https://domains.revved.com/v1/domainStatus"
BATCH_SIZE = 25
TIMEOUT_SECONDS = 15


def parse_args(argv: list[str]) -> list[str]:
    if not argv:
        return []
    if argv == ["-"]:
        argv = sys.stdin.read().split()
    flattened: list[str] = []
    for arg in argv:
        for piece in arg.replace(",", " ").split():
            piece = piece.strip().lower()
            if piece and "." in piece:
                flattened.append(piece)
    seen: set[str] = set()
    deduped: list[str] = []
    for d in flattened:
        if d not in seen:
            seen.add(d)
            deduped.append(d)
    return deduped


def check_batch(batch: list[str]) -> list[tuple[str, str]]:
    # The Revved API treats %2C-encoded commas as a single literal token and
    # falls back to a default domain. Keep the comma as a real character.
    domains_param = urllib.parse.quote(",".join(batch), safe=",")
    url = f"{API_URL}?domains={domains_param}"
    req = urllib.request.Request(url, headers={"Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=TIMEOUT_SECONDS) as resp:
        payload = json.loads(resp.read().decode("utf-8"))
    results: list[tuple[str, str]] = []
    for entry in payload.get("status", []):
        name = entry.get("name", "")
        status = "AVAILABLE" if entry.get("available") else "taken"
        if name:
            results.append((name, status))
    return results


def main(argv: list[str]) -> int:
    domains = parse_args(argv)
    if not domains:
        print(
            "Error: pass one or more full domains (each must include a TLD).\n"
            "Example: check_domains.py example.com foo.io",
            file=sys.stderr,
        )
        return 2

    all_results: list[tuple[str, str]] = []
    for i in range(0, len(domains), BATCH_SIZE):
        batch = domains[i : i + BATCH_SIZE]
        try:
            all_results.extend(check_batch(batch))
        except urllib.error.HTTPError as e:
            print(f"HTTP error from Revved API: {e.code} {e.reason}", file=sys.stderr)
            return 1
        except urllib.error.URLError as e:
            print(f"Network error contacting Revved API: {e.reason}", file=sys.stderr)
            return 1
        except (json.JSONDecodeError, ValueError) as e:
            print(f"Malformed response from Revved API: {e}", file=sys.stderr)
            return 1

    returned = {name for name, _ in all_results}
    missing = [d for d in domains if d not in returned]
    for name, status in all_results:
        print(f"{name}: {status}")
    for name in missing:
        print(f"{name}: unknown")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

from __future__ import annotations

import argparse
import json
import sys

from wiki_core import compile_missing_sources


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(
        description="Scan raw/ for uncompiled originals and compile missing source pages."
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Write compiled source pages, update wiki/index.md, and append wiki/log.md.",
    )
    parser.add_argument(
        "--domain",
        help="Optional default domain page id to attach to compiled drafts.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        help="Optional maximum number of pending raw files to process.",
    )
    args = parser.parse_args()

    result = compile_missing_sources(
        domain=args.domain,
        apply=args.apply,
        limit=args.limit,
    )
    json.dump(result, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

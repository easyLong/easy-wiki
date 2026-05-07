from __future__ import annotations

import argparse
import json
import sys
import time

from wiki_core import maintain_sources


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(
        description="Automatically compile new raw originals and report source promotion closure."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview maintenance without writing compiled source drafts.",
    )
    parser.add_argument(
        "--domain",
        help="Optional default domain page id to attach to newly compiled drafts.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        help="Optional maximum number of pending raw files to compile per run.",
    )
    parser.add_argument(
        "--watch",
        action="store_true",
        help="Keep scanning raw/ and compiling new files until stopped.",
    )
    parser.add_argument(
        "--interval",
        type=int,
        default=10,
        help="Seconds between watch scans. Default: 10.",
    )
    args = parser.parse_args()

    apply = not args.dry_run
    while True:
        result = maintain_sources(
            domain=args.domain,
            apply=apply,
            limit=args.limit,
        )
        json.dump(result, sys.stdout, ensure_ascii=False, indent=2)
        sys.stdout.write("\n")
        sys.stdout.flush()
        if not args.watch:
            return 0
        time.sleep(max(args.interval, 1))


if __name__ == "__main__":
    raise SystemExit(main())

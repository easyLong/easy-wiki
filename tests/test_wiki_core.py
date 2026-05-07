from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path


SERVICE_DIR = Path(__file__).resolve().parents[1] / "services" / "wiki-service"
if str(SERVICE_DIR) not in sys.path:
    sys.path.insert(0, str(SERVICE_DIR))

import wiki_core


class WikiCoreTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        (self.root / "raw").mkdir(parents=True)
        (self.root / "wiki" / "sources").mkdir(parents=True)
        (self.root / "wiki" / "concepts").mkdir(parents=True)
        self._write(
            "wiki/index.md",
            """---
type: index
title: index
---

# Index

## Sources

""",
        )
        self._write(
            "wiki/log.md",
            """---
type: log
title: log
---

# Log
""",
        )
        self._write(
            "wiki/concepts/example-concept.md",
            """---
type: concept
title: Example Concept
---

# Example Concept

## Definition

Example concept body.

## Links

- [[index]]
""",
        )

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def _write(self, relpath: str, text: str) -> None:
        path = self.root / relpath
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text.rstrip() + "\n", encoding="utf-8", newline="\n")

    def test_parse_raw_source_document_strips_metadata_and_preface(self) -> None:
        document = wiki_core.parse_raw_source_document(
            """# Example Source

Source URL: https://example.com/source
Expert: Example Person
Publisher: Example Publisher

Winter 2024

Example Source

The actual article body starts here.
Another paragraph continues the body.
"""
        )
        self.assertEqual(document.title, "Example Source")
        self.assertEqual(document.metadata["source_url"], "https://example.com/source")
        self.assertTrue(document.body.startswith("The actual article body starts here."))
        self.assertNotIn("Source URL:", document.body)
        self.assertNotIn("Winter 2024", document.body)

    def test_compile_source_dry_run_returns_lifecycle_and_clean_summary(self) -> None:
        self._write(
            "raw/example-source.md",
            """# Example Source

Source URL: https://example.com/source
Expert: Example Person
Role: Director
Publisher: Example Publisher

Winter 2024

Example Source

The article body explains why preparation matters because it improves execution.
Directors should plan enough to protect the strongest moment in the scene.
""",
        )

        result = wiki_core.compile_source("raw/example-source.md", apply=False, root=self.root)

        self.assertEqual(result["lifecycle"]["status"], "compiled-draft")
        self.assertEqual(result["lifecycle"]["review_status"], "pending-review")
        self.assertEqual(result["lifecycle"]["promotion_status"], "not-promoted")
        self.assertEqual(result["lifecycle"]["compile_version"], wiki_core.SOURCE_COMPILE_VERSION)
        self.assertNotIn("Source URL:", result["summary"])
        self.assertTrue(result["summary"].startswith("The article body explains"))
        self.assertIn("preparation matters because it improves execution.", result["claims"][0])

    def test_compile_source_apply_writes_tracking_fields_and_health_flags(self) -> None:
        self._write(
            "raw/example-source.md",
            """# Example Source

Source URL: https://example.com/source
Expert: Example Person

The article body explains why preparation matters because it improves execution.
Directors should plan enough to protect the strongest moment in the scene.
""",
        )

        result = wiki_core.compile_source("raw/example-source.md", apply=True, root=self.root)
        self.assertTrue(result["written"])

        page = wiki_core.read_page_file(self.root / "wiki" / "sources" / "example-source.md", self.root)
        self.assertEqual(page.frontmatter["status"], "compiled-draft")
        self.assertEqual(page.frontmatter["review_status"], "pending-review")
        self.assertEqual(page.frontmatter["promotion_status"], "not-promoted")
        self.assertEqual(page.frontmatter["compile_version"], wiki_core.SOURCE_COMPILE_VERSION)
        self.assertIn("## Compile Status", page.body)
        self.assertIn("Review status: pending-review", page.body)

        health = wiki_core.health_check(self.root)
        self.assertEqual(health["compiled_drafts_pending_review"], ["example-source"])
        self.assertEqual(health["compiled_drafts_missing_tracking"], [])

    def test_compile_missing_sources_dry_run_uses_would_write_counts(self) -> None:
        self._write("raw/first.md", "# First\n\nBody because it matters.\n")
        self._write("raw/second.md", "# Second\n\nBody because it matters.\n")

        result = wiki_core.compile_missing_sources(apply=False, root=self.root)

        self.assertEqual(result["mode"], "dry-run")
        self.assertEqual(result["pending_count"], 2)
        self.assertEqual(result["written_count"], 0)
        self.assertEqual(result["would_write_count"], 2)
        self.assertEqual(result["skipped_count"], 0)
        self.assertEqual(sorted(result["would_write_source_ids"]), ["first", "second"])

    def test_health_check_flags_compiled_drafts_missing_tracking(self) -> None:
        self._write(
            "wiki/sources/broken-draft.md",
            """---
type: source
title: Broken Draft
status: compiled-draft
raw_original_path: raw/broken.md
tags: [source, compiled-draft]
---

# Broken Draft

## Summary

Needs review.

## Sources

- `raw/broken.md`
""",
        )

        health = wiki_core.health_check(self.root)

        self.assertEqual(health["compiled_drafts_pending_review"], ["broken-draft"])
        self.assertEqual(health["compiled_drafts_missing_tracking"], ["broken-draft"])


if __name__ == "__main__":
    unittest.main()

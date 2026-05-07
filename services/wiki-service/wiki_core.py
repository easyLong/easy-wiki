from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any


WIKILINK_RE = re.compile(r"\[\[([^\]|#]+)(?:[#|][^\]]*)?\]\]")


@dataclass(frozen=True)
class Page:
    id: str
    path: Path
    relpath: str
    frontmatter: dict[str, Any]
    body: str

    @property
    def title(self) -> str:
        value = self.frontmatter.get("title")
        return str(value) if value else self.id

    @property
    def type(self) -> str:
        value = self.frontmatter.get("type")
        return str(value) if value else "unknown"

    @property
    def tags(self) -> list[str]:
        value = self.frontmatter.get("tags", [])
        if isinstance(value, list):
            return [str(item) for item in value]
        if isinstance(value, str):
            return [value]
        return []


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def wiki_root(root: Path | None = None) -> Path:
    return (root or repo_root()) / "wiki"


def parse_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    if not text.startswith("---\n"):
        return {}, text

    end = text.find("\n---\n", 4)
    if end == -1:
        return {}, text

    raw = text[4:end]
    body = text[end + 5 :]
    data: dict[str, Any] = {}

    for line in raw.splitlines():
        if not line.strip() or ":" not in line:
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()
        if value.startswith("[") and value.endswith("]"):
            items = [item.strip().strip("\"'") for item in value[1:-1].split(",")]
            data[key] = [item for item in items if item]
        else:
            data[key] = value.strip("\"'")

    return data, body


def read_page_file(path: Path, root: Path | None = None) -> Page:
    base = root or repo_root()
    text = path.read_text(encoding="utf-8")
    frontmatter, body = parse_frontmatter(text)
    return Page(
        id=path.stem,
        path=path,
        relpath=path.relative_to(base).as_posix(),
        frontmatter=frontmatter,
        body=body,
    )


def list_pages(root: Path | None = None) -> list[Page]:
    base = root or repo_root()
    pages = []
    for path in sorted(wiki_root(base).rglob("*.md")):
        pages.append(read_page_file(path, base))
    return pages


def page_catalog(root: Path | None = None) -> dict[str, Page]:
    catalog: dict[str, Page] = {}
    for page in list_pages(root):
        catalog[page.id] = page
    return catalog


def get_page(page_id: str, root: Path | None = None) -> Page | None:
    return page_catalog(root).get(page_id)


def page_links(page: Page) -> list[str]:
    text = "\n".join([_frontmatter_text(page.frontmatter), page.body])
    seen: set[str] = set()
    links: list[str] = []
    for match in WIKILINK_RE.finditer(text):
        target = match.group(1).strip()
        if target and target not in seen:
            seen.add(target)
            links.append(target)
    return links


def backlinks(page_id: str, root: Path | None = None) -> list[str]:
    result: list[str] = []
    for page in list_pages(root):
        if page_id in page_links(page):
            result.append(page.id)
    return result


def search_pages(query: str, limit: int = 10, root: Path | None = None) -> list[dict[str, Any]]:
    terms = [term.lower() for term in query.split() if term.strip()]
    if not terms:
        return []

    results: list[dict[str, Any]] = []
    for page in list_pages(root):
        haystack = " ".join(
            [
                page.id,
                page.title,
                page.type,
                " ".join(page.tags),
                page.body,
            ]
        ).lower()
        score = sum(haystack.count(term) for term in terms)
        if score:
            results.append({"score": score, **page_record(page)})

    results.sort(key=lambda item: item["score"], reverse=True)
    return results[:limit]


def lint(root: Path | None = None) -> dict[str, Any]:
    pages = list_pages(root)
    ids: dict[str, int] = {}
    for page in pages:
        ids[page.id] = ids.get(page.id, 0) + 1

    valid_ids = set(ids)
    broken: list[dict[str, str]] = []
    missing_frontmatter: list[str] = []

    for page in pages:
        if not page.frontmatter:
            missing_frontmatter.append(page.id)
        for target in page_links(page):
            if target not in valid_ids:
                broken.append({"from": page.id, "to": target})

    duplicates = sorted([page_id for page_id, count in ids.items() if count > 1])

    return {
        "page_count": len(pages),
        "duplicate_ids": duplicates,
        "broken_links": broken,
        "missing_frontmatter": missing_frontmatter,
    }


def page_record(page: Page) -> dict[str, Any]:
    return {
        "id": page.id,
        "path": page.relpath,
        "type": page.type,
        "title": page.title,
        "tags": page.tags,
        "links": page_links(page),
    }


def page_detail(page: Page, root: Path | None = None) -> dict[str, Any]:
    return {
        **page_record(page),
        "frontmatter": page.frontmatter,
        "content": page.body,
        "backlinks": backlinks(page.id, root),
    }


def _frontmatter_text(frontmatter: dict[str, Any]) -> str:
    return "\n".join(f"{key}: {value}" for key, value in frontmatter.items())

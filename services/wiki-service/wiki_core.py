from __future__ import annotations

import re
from collections import Counter
from dataclasses import dataclass
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any


WIKILINK_RE = re.compile(r"\[\[([^\]|#]+)(?:[#|][^\]]*)?\]\]")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$", re.MULTILINE)
WORD_RE = re.compile(r"[A-Za-z][A-Za-z0-9-]{2,}|[\u4e00-\u9fff]{2,}")
ENGLISH_CLAIM_MARKER_RE = re.compile(r"\b(?:should|must|can|not|because|therefore)\b", re.IGNORECASE)
SOURCE_COMPILE_VERSION = "source-compile-v4"
SOURCE_PROMOTION_TARGET_TYPES = {
    "concept",
    "comparison",
    "domain",
    "expert",
    "template",
    "workflow",
}
RAW_SOURCE_METADATA_KEYS = {
    "source url": "source_url",
    "url": "source_url",
    "original url": "source_url",
    "expert": "expert",
    "role": "role",
    "publisher": "publisher",
    "published": "published",
    "date": "published",
    "author": "author",
    "by": "author",
    "来源": "source_url",
    "原文链接": "source_url",
    "专家": "expert",
    "角色": "role",
    "发布方": "publisher",
    "出版方": "publisher",
    "发布时间": "published",
    "作者": "author",
}


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


@dataclass(frozen=True)
class RawSourceDocument:
    title: str | None
    metadata: dict[str, str]
    body: str


@dataclass(frozen=True)
class SourceLifecycle:
    status: str
    review_status: str
    promotion_status: str
    compiled_at: str
    compile_version: str


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def wiki_root(root: Path | None = None) -> Path:
    return (root or repo_root()) / "wiki"


def raw_root(root: Path | None = None) -> Path:
    return (root or repo_root()) / "raw"


def parse_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    normalized = text.lstrip("\ufeff").replace("\r\n", "\n").replace("\r", "\n")
    if not normalized.startswith("---\n"):
        return {}, normalized
    end = normalized.find("\n---\n", 4)
    if end == -1:
        return {}, normalized

    raw = normalized[4:end]
    body = normalized[end + 5 :]
    data: dict[str, Any] = {}
    lines = raw.splitlines()
    index = 0
    while index < len(lines):
        line = lines[index]
        if not line.strip() or ":" not in line or line.startswith(" "):
            index += 1
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()
        if value == "":
            items: list[str] = []
            index += 1
            while index < len(lines):
                item_match = re.match(r"\s*-\s+(.+?)\s*$", lines[index])
                if not item_match:
                    break
                items.append(item_match.group(1).strip().strip("\"'"))
                index += 1
            data[key] = items if items else ""
            continue
        if value.startswith("[") and value.endswith("]"):
            items = [item.strip().strip("\"'") for item in value[1:-1].split(",")]
            data[key] = [item for item in items if item]
        else:
            data[key] = value.strip("\"'")
        index += 1
    return data, body


def read_page_file(path: Path, root: Path | None = None) -> Page:
    base = root or repo_root()
    text = path.read_text(encoding="utf-8")
    frontmatter, body = parse_frontmatter(text)
    return Page(
        id=path.stem,
        path=path,
        relpath=_relpath_from_base(path, base),
        frontmatter=frontmatter,
        body=body,
    )


def list_pages(root: Path | None = None) -> list[Page]:
    base = root or repo_root()
    return [read_page_file(path, base) for path in sorted(wiki_root(base).rglob("*.md"))]


def page_catalog(root: Path | None = None) -> dict[str, Page]:
    return {page.id: page for page in list_pages(root)}


def get_page(page_id: str, root: Path | None = None) -> Page | None:
    return page_catalog(root).get(page_id)


def page_links(page: Page) -> list[str]:
    text = "\n".join([_frontmatter_text(page.frontmatter), page.body])
    seen: set[str] = set()
    result: list[str] = []
    for match in WIKILINK_RE.finditer(text):
        target = match.group(1).strip()
        if target and target not in seen:
            seen.add(target)
            result.append(target)
    return result


def backlinks(page_id: str, root: Path | None = None) -> list[str]:
    return [page.id for page in list_pages(root) if page_id in page_links(page)]


def search_pages(query: str, limit: int = 10, root: Path | None = None) -> list[dict[str, Any]]:
    terms = [term.lower() for term in query.split() if term.strip()]
    if not terms:
        return []
    results: list[dict[str, Any]] = []
    for page in list_pages(root):
        haystack = " ".join([page.id, page.title, page.type, " ".join(page.tags), page.body]).lower()
        score = sum(haystack.count(term) for term in terms)
        if score:
            results.append({"score": score, **page_record(page)})
    return sorted(results, key=lambda item: item["score"], reverse=True)[:limit]


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
    return {
        "page_count": len(pages),
        "duplicate_ids": sorted(page_id for page_id, count in ids.items() if count > 1),
        "broken_links": broken,
        "missing_frontmatter": missing_frontmatter,
    }


def health_check(root: Path | None = None) -> dict[str, Any]:
    base = root or repo_root()
    pages = list_pages(base)
    catalog = {page.id: page for page in pages}
    index_page = catalog.get("index")
    index_links = set(page_links(index_page)) if index_page else set()
    usage = source_usage(base)
    draft_tracking = _compiled_draft_tracking(pages)
    return {
        **lint(base),
        "missing_index_entries": sorted(
            page.id
            for page in pages
            if page.type not in {"index", "log", "template"} and page.id not in index_links
        ),
        "orphan_pages": sorted(
            page.id
            for page in pages
            if page.id != "index" and page.type != "log" and not backlinks(page.id, base)
        ),
        "missing_required_sections": _missing_required_sections(pages),
        "raw_files_missing_source_page": usage["raw_files_missing_source_page"],
        "source_pages_missing_raw_file": usage["source_pages_missing_raw_file"],
        "source_pages_without_usage": usage["source_pages_without_usage"],
        "source_pages_without_durable_usage": usage["source_pages_without_durable_usage"],
        "source_pages_pending_review": usage["source_pages_pending_review"],
        "source_pages_not_promoted": usage["source_pages_not_promoted"],
        "durable_pages_without_source_context": usage["durable_pages_without_source_context"],
        "source_usage": usage["sources"],
        "source_promotion_candidates": promotion_candidates(base)["candidates"],
        "compiled_drafts_pending_review": draft_tracking["pending_review"],
        "compiled_drafts_missing_tracking": draft_tracking["missing_tracking"],
    }


def source_usage(root: Path | None = None) -> dict[str, Any]:
    base = root or repo_root()
    raw_relpaths = [
        _relpath_from_base(path, base)
        for path in sorted(raw_root(base).glob("*"))
        if path.is_file()
    ]
    pages = list_pages(base)
    catalog = {page.id: page for page in pages}
    source_pages = [page for page in pages if page.type == "source" or page.relpath.startswith("wiki/sources/")]
    raw_to_sources: dict[str, list[str]] = {relpath: [] for relpath in raw_relpaths}
    missing_raw: list[dict[str, str]] = []
    without_usage: list[str] = []
    without_durable_usage: list[str] = []
    pending_review: list[str] = []
    not_promoted: list[str] = []
    source_records: list[dict[str, Any]] = []
    source_ids = {page.id for page in source_pages}
    durable_source_targets: dict[str, list[str]] = {}

    for page in pages:
        if page.type not in SOURCE_PROMOTION_TARGET_TYPES:
            continue
        source_links = sorted(link for link in page_links(page) if link in source_ids)
        durable_source_targets[page.id] = source_links

    for source in source_pages:
        raw_paths = source_raw_paths(source)
        for raw_path in raw_paths:
            if raw_path in raw_to_sources:
                raw_to_sources[raw_path].append(source.id)
            else:
                missing_raw.append({"source": source.id, "raw_path": raw_path})
        outbound = [link for link in page_links(source) if link in catalog and link != source.id]
        durable_outbound = [
            link
            for link in outbound
            if catalog[link].type in SOURCE_PROMOTION_TARGET_TYPES
        ]
        inbound = backlinks(source.id, base)
        meaningful_inbound = [
            page_id
            for page_id in inbound
            if catalog.get(page_id) and catalog[page_id].type not in {"index", "log", "source"}
        ]
        durable_backlinks = [
            page_id
            for page_id in inbound
            if catalog.get(page_id) and catalog[page_id].type in SOURCE_PROMOTION_TARGET_TYPES
        ]
        feeds_pages = sorted(set(outbound + meaningful_inbound))
        durable_usage_pages = sorted(set(durable_backlinks))
        if not feeds_pages:
            without_usage.append(source.id)
        if not durable_usage_pages:
            without_durable_usage.append(source.id)
        if source.frontmatter.get("review_status") == "pending-review":
            pending_review.append(source.id)
        if source.frontmatter.get("promotion_status") in {"not-promoted", "", None}:
            not_promoted.append(source.id)
        source_records.append(
            {
                "id": source.id,
                "title": source.title,
                "raw_paths": raw_paths,
                "status": source.frontmatter.get("status"),
                "review_status": source.frontmatter.get("review_status"),
                "promotion_status": source.frontmatter.get("promotion_status"),
                "compile_version": source.frontmatter.get("compile_version"),
                "outbound_links": outbound,
                "durable_outbound_links": durable_outbound,
                "backlinks": inbound,
                "meaningful_backlinks": meaningful_inbound,
                "durable_backlinks": durable_backlinks,
                "feeds_pages": feeds_pages,
                "durable_usage_pages": durable_usage_pages,
                "closure_status": "used" if durable_usage_pages else "needs-promotion",
            }
        )

    durable_without_source_context = [
        page_id
        for page_id, source_links in durable_source_targets.items()
        if not source_links
    ]

    return {
        "raw_files": raw_relpaths,
        "raw_files_missing_source_page": sorted(
            relpath for relpath, source_ids in raw_to_sources.items() if not source_ids
        ),
        "source_pages_missing_raw_file": missing_raw,
        "source_pages_without_usage": sorted(without_usage),
        "source_pages_without_durable_usage": sorted(without_durable_usage),
        "source_pages_pending_review": sorted(pending_review),
        "source_pages_not_promoted": sorted(not_promoted),
        "durable_pages_without_source_context": sorted(durable_without_source_context),
        "closure_counts": {
            "raw_files": len(raw_relpaths),
            "raw_files_missing_source_page": sum(1 for source_ids in raw_to_sources.values() if not source_ids),
            "source_pages": len(source_pages),
            "source_pages_without_durable_usage": len(without_durable_usage),
            "source_pages_pending_review": len(pending_review),
            "source_pages_not_promoted": len(not_promoted),
            "durable_pages_without_source_context": len(durable_without_source_context),
        },
        "sources": sorted(source_records, key=lambda item: item["id"]),
    }


def promotion_candidates(root: Path | None = None) -> dict[str, Any]:
    base = root or repo_root()
    pages = list_pages(base)
    catalog = {page.id: page for page in pages}
    source_pages = [page for page in pages if page.type == "source" or page.relpath.startswith("wiki/sources/")]
    candidates: list[dict[str, Any]] = []

    for source in source_pages:
        outbound = [link for link in page_links(source) if link in catalog]
        durable_outbound = [
            link
            for link in outbound
            if catalog[link].type in SOURCE_PROMOTION_TARGET_TYPES
        ]
        meaningful_backlinks = [
            page_id
            for page_id in backlinks(source.id, base)
            if catalog.get(page_id) and catalog[page_id].type in SOURCE_PROMOTION_TARGET_TYPES
        ]
        durable_usage_pages = sorted(set(meaningful_backlinks))
        review_status = str(source.frontmatter.get("review_status") or "unknown")
        promotion_status = str(source.frontmatter.get("promotion_status") or "unknown")
        needs_review = review_status in {"unknown", "pending-review"}
        needs_promotion = promotion_status in {"unknown", "not-promoted"}
        lacks_usage = not durable_usage_pages

        if not (needs_review or needs_promotion or lacks_usage):
            continue

        search_text = " ".join(
            [
                source.title,
                " ".join(str(item) for item in source.frontmatter.values()),
                " ".join(_keywords(source.body, limit=8)),
            ]
        )
        benchmark_targets = [
            item
            for item in _benchmark_candidates(search_text, base)
            if item["id"] != source.id
        ]
        target_ids = _ordered_unique([*durable_outbound, *meaningful_backlinks, *[item["id"] for item in benchmark_targets]])
        reasons: list[str] = []
        if needs_review:
            reasons.append("source draft still needs human review")
        if needs_promotion:
            reasons.append("promotion_status is not promoted")
        if lacks_usage:
            reasons.append("no durable page currently uses this source")

        candidates.append(
            {
                "source_id": source.id,
                "title": source.title,
                "raw_paths": source_raw_paths(source),
                "review_status": review_status,
                "promotion_status": promotion_status,
                "durable_usage_pages": durable_usage_pages,
                "suggested_targets": [
                    {
                        "id": page_id,
                        "title": catalog[page_id].title,
                        "type": catalog[page_id].type,
                    }
                    for page_id in target_ids[:8]
                    if page_id in catalog and catalog[page_id].type in SOURCE_PROMOTION_TARGET_TYPES
                ],
                "benchmark_candidates": benchmark_targets[:8],
                "reason": "; ".join(reasons),
                "priority": (10 if lacks_usage else 0) + (5 if needs_promotion else 0) + (3 if needs_review else 0),
            }
        )

    candidates.sort(key=lambda item: (-item["priority"], item["source_id"]))
    return {
        "candidate_count": len(candidates),
        "candidates": candidates,
    }


def source_raw_paths(page: Page) -> list[str]:
    paths: list[str] = []
    single = page.frontmatter.get("raw_original_path")
    if single:
        paths.append(str(single))
    multiple = page.frontmatter.get("raw_original_paths")
    if isinstance(multiple, list):
        paths.extend(str(item) for item in multiple if item)
    elif isinstance(multiple, str) and multiple:
        paths.append(multiple)
    return sorted(set(paths))


def compile_source(
    source_path: str,
    *,
    title: str | None = None,
    domain: str | None = None,
    apply: bool = False,
    root: Path | None = None,
) -> dict[str, Any]:
    base = root or repo_root()
    raw_path = _resolve_raw_path(source_path, base)
    text = raw_path.read_text(encoding="utf-8")
    raw_document = parse_raw_source_document(text)
    content_text = raw_document.body or text
    lifecycle = _build_source_lifecycle()
    source_id = raw_path.stem
    page_title = title or raw_document.title or _extract_title(text) or source_id.replace("-", " ").title()
    source_page_path = wiki_root(base) / "sources" / f"{source_id}.md"
    existing_page = read_page_file(source_page_path, base) if source_page_path.exists() else None
    headings = _extract_headings(content_text)
    summary = _summary_from_text(content_text)
    claims = _claims_from_text(content_text)
    keywords = _keywords(content_text, limit=10)
    benchmark_candidates = _benchmark_candidates(" ".join([page_title, *keywords]), base)
    suggested_links = [item["id"] for item in benchmark_candidates[:8]]
    condensed_takeaways = _condensed_takeaways(summary, claims)
    challenge_notes = _challenge_notes(
        metadata=raw_document.metadata,
        claims=claims,
        headings=headings,
    )
    benchmark_notes = _benchmark_notes(benchmark_candidates)
    compile_promotion_candidates = _compile_promotion_candidates(
        domain=domain,
        benchmark_candidates=benchmark_candidates,
        keywords=keywords,
    )
    written = False
    log_entry = None

    if apply and existing_page is None:
        source_page_path.parent.mkdir(parents=True, exist_ok=True)
        raw_relpath = _relpath_from_base(raw_path, base)
        frontmatter = {
            "type": "source",
            "title": page_title,
            "raw_original_path": raw_relpath,
            "date_added": date.today().isoformat(),
            "status": lifecycle.status,
            "review_status": lifecycle.review_status,
            "promotion_status": lifecycle.promotion_status,
            "compiled_at": lifecycle.compiled_at,
            "compile_version": lifecycle.compile_version,
            "tags": ["source", "compiled-draft"],
        }
        for key in ("source_url", "publisher", "published", "expert", "role", "author"):
            value = raw_document.metadata.get(key)
            if value:
                frontmatter[key] = value
        if domain:
            frontmatter["domain"] = domain
        _write_markdown_page(
            source_page_path,
            frontmatter,
            _source_page_body(
                source_id=source_id,
                title=page_title,
                raw_relpath=raw_relpath,
                domain=domain,
                summary=summary,
                metadata=raw_document.metadata,
                lifecycle=lifecycle,
                headings=headings,
                claims=claims,
                condensed_takeaways=condensed_takeaways,
                challenge_notes=challenge_notes,
                benchmark_notes=benchmark_notes,
                benchmark_candidates=benchmark_candidates,
                promotion_candidates=compile_promotion_candidates,
                suggested_links=suggested_links,
            ),
        )
        ensure_index_source_entry(source_id, page_title, base)
        log_entry = append_log(
            "ingest",
            f"Compiled raw source `{raw_relpath}` into [[{source_id}]] draft.",
            base,
        )
        written = True

    return {
        "source_id": source_id,
        "title": page_title,
        "raw_path": _relpath_from_base(raw_path, base),
        "source_page": _relpath_from_base(source_page_path, base),
        "existing_source_page": existing_page.id if existing_page else None,
        "written": written,
        "log_entry": log_entry,
        "lifecycle": {
            "status": lifecycle.status,
            "review_status": lifecycle.review_status,
            "promotion_status": lifecycle.promotion_status,
            "compiled_at": lifecycle.compiled_at,
            "compile_version": lifecycle.compile_version,
        },
        "summary": summary,
        "raw_metadata": raw_document.metadata,
        "headings": headings,
        "claims": claims,
        "condensed_takeaways": condensed_takeaways,
        "challenge_notes": challenge_notes,
        "benchmark_notes": benchmark_notes,
        "keywords": keywords,
        "benchmark_candidates": benchmark_candidates,
        "promotion_candidates": compile_promotion_candidates,
        "suggested_links": suggested_links,
        "next_actions": [
            "Review the compiled draft for factual accuracy.",
            "Use condensed takeaways, challenge notes, and benchmark targets before promoting claims.",
            "Update relevant concept, expert, domain, workflow, or template pages with explicit source links.",
            "Run /healthcheck after promotion to confirm source usage and link health.",
        ],
    }


def compile_missing_sources(
    *,
    domain: str | None = None,
    apply: bool = False,
    limit: int | None = None,
    root: Path | None = None,
) -> dict[str, Any]:
    base = root or repo_root()
    usage = source_usage(base)
    pending = usage["raw_files_missing_source_page"]
    if limit is not None:
        pending = pending[:limit]

    results = [
        compile_source(raw_path, domain=domain, apply=apply, root=base)
        for raw_path in pending
    ]
    written = [item["source_id"] for item in results if item["written"]]
    would_write = [item["source_id"] for item in results if not apply and item["existing_source_page"] is None]
    skipped = [item["source_id"] for item in results if apply and not item["written"]]

    return {
        "apply": apply,
        "mode": "apply" if apply else "dry-run",
        "domain": domain,
        "pending_count": len(pending),
        "written_count": len(written),
        "would_write_count": len(would_write),
        "skipped_count": len(skipped),
        "pending_raw_files": pending,
        "written_source_ids": written,
        "would_write_source_ids": would_write,
        "skipped_source_ids": skipped,
        "results": results,
    }


def maintain_sources(
    *,
    domain: str | None = None,
    apply: bool = True,
    limit: int | None = None,
    root: Path | None = None,
) -> dict[str, Any]:
    base = root or repo_root()
    compile_result = compile_missing_sources(
        domain=domain,
        apply=apply,
        limit=limit,
        root=base,
    )
    usage = source_usage(base)
    promotion_report = promotion_candidates(base)
    health = health_check(base)
    return {
        "apply": apply,
        "mode": "apply" if apply else "dry-run",
        "domain": domain,
        "compile": compile_result,
        "closure_counts": usage["closure_counts"],
        "promotion_candidate_count": promotion_report["candidate_count"],
        "promotion_candidates": promotion_report["candidates"],
        "health_summary": {
            "broken_links_count": len(health["broken_links"]),
            "missing_index_entries_count": len(health["missing_index_entries"]),
            "orphan_pages_count": len(health["orphan_pages"]),
            "missing_required_sections_count": len(health["missing_required_sections"]),
            "raw_files_missing_source_page_count": len(health["raw_files_missing_source_page"]),
            "source_pages_without_durable_usage_count": len(health["source_pages_without_durable_usage"]),
            "source_pages_pending_review_count": len(health["source_pages_pending_review"]),
            "source_pages_not_promoted_count": len(health["source_pages_not_promoted"]),
        },
        "next_actions": _maintain_next_actions(compile_result, promotion_report, health),
    }


def create_project(
    slug: str,
    *,
    title: str | None = None,
    domain: str = "ai-short-drama-domain-overview",
    apply: bool = True,
    root: Path | None = None,
) -> dict[str, Any]:
    base = root or repo_root()
    safe_slug = slugify(slug)
    if not safe_slug:
        raise ValueError("Project slug is required.")
    project_title = title or safe_slug.replace("-", " ").title()
    project_dir = wiki_root(base) / "projects" / safe_slug
    files = {
        f"{safe_slug}-project-overview.md": _project_overview_body(safe_slug, project_title, domain),
        f"{safe_slug}-brief.md": _project_brief_body(project_title),
        f"{safe_slug}-action-plan.md": _project_action_plan_body(project_title),
        f"{safe_slug}-decisions.md": _project_decisions_body(project_title),
        f"{safe_slug}-working-notes.md": _project_working_notes_body(project_title),
        f"{safe_slug}-review.md": _project_review_body(project_title),
        f"{safe_slug}-postmortem.md": _project_postmortem_body(project_title),
    }
    created: list[str] = []
    skipped: list[str] = []
    if apply:
        project_dir.mkdir(parents=True, exist_ok=True)
        for filename, body in files.items():
            path = project_dir / filename
            if path.exists():
                skipped.append(_relpath_from_base(path, base))
                continue
            frontmatter = {
                "type": "project",
                "title": project_title if filename.endswith("project-overview.md") else filename[:-3],
                "project": safe_slug,
                "domain": domain,
                "status": "active",
                "created": date.today().isoformat(),
                "updated": date.today().isoformat(),
                "tags": ["project"],
            }
            _write_markdown_page(path, frontmatter, body)
            created.append(_relpath_from_base(path, base))
        ensure_project_index_entry(safe_slug, project_title, base)
        append_log("project", f"Created project [[{safe_slug}-project-overview|{project_title}]].", base)
    return {
        "slug": safe_slug,
        "title": project_title,
        "domain": domain,
        "project_dir": _relpath_from_base(project_dir, base),
        "created": created,
        "skipped": skipped,
        "planned_files": sorted(files),
    }


def append_log(category: str, message: str, root: Path | None = None) -> str:
    base = root or repo_root()
    path = wiki_root(base) / "log.md"
    entry = f"\n## [{date.today().isoformat()}] {category}\n\n{message}\n"
    with path.open("a", encoding="utf-8", newline="\n") as handle:
        handle.write(entry)
    return entry.strip()


def ensure_index_source_entry(source_id: str, title: str, root: Path | None = None) -> None:
    base = root or repo_root()
    path = wiki_root(base) / "index.md"
    text = path.read_text(encoding="utf-8")
    if f"[[{source_id}" in text:
        return
    entry = f"- [[{source_id}|{title}]] - Compiled source draft.\n"
    path.write_text(_insert_under_heading(text, "## Sources", entry), encoding="utf-8", newline="\n")


def ensure_project_index_entry(slug: str, title: str, root: Path | None = None) -> None:
    base = root or repo_root()
    path = wiki_root(base) / "projects" / "project-index.md"
    text = path.read_text(encoding="utf-8")
    if f"[[{slug}-project-overview" in text:
        return
    entry = f"- [[{slug}-project-overview|{title}]] - Active project.\n"
    if "No active projects yet." in text:
        text = text.replace("No active projects yet.", entry.rstrip())
    else:
        text = _insert_under_heading(text, "## Active Projects", entry)
    path.write_text(text, encoding="utf-8", newline="\n")


def page_record(page: Page) -> dict[str, Any]:
    return {
        "id": page.id,
        "path": page.relpath,
        "type": page.type,
        "title": page.title,
        "tags": page.tags,
        "domain": page.frontmatter.get("domain"),
        "project": page.frontmatter.get("project"),
        "updated": page.frontmatter.get("updated"),
        "links": page_links(page),
    }


def page_detail(page: Page, root: Path | None = None) -> dict[str, Any]:
    return {**page_record(page), "frontmatter": page.frontmatter, "content": page.body, "backlinks": backlinks(page.id, root)}


def slugify(value: str) -> str:
    lowered = value.strip().lower()
    lowered = re.sub(r"[^a-z0-9\u4e00-\u9fff]+", "-", lowered)
    return re.sub(r"-+", "-", lowered).strip("-")


def _frontmatter_text(frontmatter: dict[str, Any]) -> str:
    return "\n".join(f"{key}: {value}" for key, value in frontmatter.items())


def _frontmatter_block(frontmatter: dict[str, Any]) -> str:
    lines = ["---"]
    for key, value in frontmatter.items():
        if isinstance(value, list):
            lines.append(f"{key}: [{', '.join(str(item) for item in value)}]")
        else:
            lines.append(f"{key}: {value}")
    lines.append("---")
    return "\n".join(lines)


def _write_markdown_page(path: Path, frontmatter: dict[str, Any], body: str) -> None:
    path.write_text(f"{_frontmatter_block(frontmatter)}\n\n{body.rstrip()}\n", encoding="utf-8", newline="\n")


def _resolve_raw_path(source_path: str, root: Path) -> Path:
    candidate = (root / source_path).resolve() if not Path(source_path).is_absolute() else Path(source_path).resolve()
    raw = raw_root(root).resolve()
    try:
        candidate.relative_to(raw)
    except ValueError as exc:
        raise ValueError("source_path must point to a file under raw/") from exc
    if not candidate.exists() or not candidate.is_file():
        raise FileNotFoundError(source_path)
    return candidate


def _relpath_from_base(path: Path, base: Path) -> str:
    return path.resolve().relative_to(base.resolve()).as_posix()


def _extract_title(text: str) -> str | None:
    match = re.search(r"^#\s+(.+?)\s*$", text, re.MULTILINE)
    return match.group(1).strip() if match else None


def _build_source_lifecycle(now: datetime | None = None) -> SourceLifecycle:
    current = now or datetime.now(timezone.utc)
    return SourceLifecycle(
        status="compiled-draft",
        review_status="pending-review",
        promotion_status="not-promoted",
        compiled_at=current.replace(microsecond=0).isoformat(),
        compile_version=SOURCE_COMPILE_VERSION,
    )


def parse_raw_source_document(text: str) -> RawSourceDocument:
    normalized = text.lstrip("\ufeff").replace("\r\n", "\n").replace("\r", "\n")
    lines = normalized.split("\n")
    index = 0

    while index < len(lines) and not lines[index].strip():
        index += 1

    title = None
    if index < len(lines):
        title_match = re.match(r"^#\s+(.+?)\s*$", lines[index])
        if title_match:
            title = title_match.group(1).strip()
            index += 1

    while index < len(lines) and not lines[index].strip():
        index += 1

    metadata: dict[str, str] = {}
    while index < len(lines):
        stripped = lines[index].strip()
        if not stripped:
            if metadata:
                index += 1
                break
            index += 1
            continue
        parsed = _parse_raw_source_metadata_line(stripped)
        if parsed is None:
            break
        key, value = parsed
        metadata[key] = value
        index += 1

    while index < len(lines) and not lines[index].strip():
        index += 1

    body = _strip_raw_body_preface(lines[index:], title)
    if not body:
        body = normalized.strip()
    return RawSourceDocument(title=title, metadata=metadata, body=body)


def _parse_raw_source_metadata_line(line: str) -> tuple[str, str] | None:
    if ":" not in line:
        return None
    raw_key, raw_value = line.split(":", 1)
    key = re.sub(r"\s+", " ", raw_key).strip().lower()
    value = raw_value.strip()
    if not value:
        return None
    canonical = RAW_SOURCE_METADATA_KEYS.get(key)
    if not canonical:
        return None
    return canonical, value


def _strip_raw_body_preface(lines: list[str], title: str | None) -> str:
    index = 0
    while index < len(lines):
        cleaned = _clean_line(lines[index])
        if not cleaned:
            index += 1
            continue
        if title and cleaned.casefold() == title.casefold():
            index += 1
            continue
        if re.fullmatch(r"(spring|summer|fall|winter)\s+\d{4}", cleaned, re.IGNORECASE):
            index += 1
            continue
        break
    return "\n".join(lines[index:]).strip()


def _extract_headings(text: str, limit: int = 20) -> list[str]:
    headings: list[str] = []
    for match in HEADING_RE.finditer(text):
        title = match.group(2).strip()
        if title and title not in headings:
            headings.append(title)
        if len(headings) >= limit:
            break
    return headings


def _summary_from_text(text: str, limit: int = 900) -> str:
    paragraphs = [
        _clean_line(line)
        for line in text.splitlines()
        if _clean_line(line)
        and not _is_ignorable_source_line(line)
        and not line.lstrip().startswith("#")
        and not line.lstrip().startswith("![")
    ]
    summary = " ".join(paragraphs[:8])
    return summary[: limit - 3].rstrip() + "..." if len(summary) > limit else summary


def _claims_from_text(text: str, limit: int = 10) -> list[str]:
    chinese_markers = [
        "\u9700\u8981",
        "\u5e94\u8be5",
        "\u5fc5\u987b",
        "\u53ef\u4ee5",
        "\u4e0d\u662f",
        "\u56e0\u4e3a",
        "\u6240\u4ee5",
        "\u5173\u952e",
        "\u6838\u5fc3",
    ]
    candidates: list[str] = []
    for raw_line in text.splitlines():
        line = _clean_line(raw_line).lstrip("-0123456789. ")
        if len(line) < 12 or line.startswith("![") or _is_ignorable_source_line(raw_line):
            continue
        if ENGLISH_CLAIM_MARKER_RE.search(line) or any(marker in line for marker in chinese_markers):
            candidates.append(line)
        if len(candidates) >= limit:
            break
    return candidates


def _condensed_takeaways(summary: str, claims: list[str], limit: int = 3) -> list[str]:
    candidates = [claim for claim in claims if claim]
    if len(candidates) < limit:
        candidates.extend(_sentences_from_text(summary))
    takeaways: list[str] = []
    for candidate in candidates:
        cleaned = _truncate(_clean_line(candidate), 180)
        if cleaned and cleaned not in takeaways:
            takeaways.append(cleaned)
        if len(takeaways) >= limit:
            break
    return takeaways


def _challenge_notes(
    *,
    metadata: dict[str, str],
    claims: list[str],
    headings: list[str],
) -> list[str]:
    notes: list[str] = []
    if not metadata.get("source_url"):
        notes.append("Reliability: no source_url metadata was detected; verify provenance before promotion.")
    if not metadata.get("published"):
        notes.append("Freshness: no published date was detected; check whether claims depend on timing.")
    if claims:
        notes.append(f"Assumption check: verify evidence for `{_truncate(claims[0], 120)}`.")
    else:
        notes.append("Claim check: no strong claims were extracted automatically; review the source manually.")
    if headings:
        notes.append(f"Boundary check: extracted structure starts from `{_truncate(headings[0], 80)}`; confirm the source scope.")
    notes.append("Counterexample check: identify where this advice would fail before updating durable pages.")
    return notes


def _benchmark_notes(benchmark_candidates: list[dict[str, Any]]) -> list[str]:
    if not benchmark_candidates:
        return ["No existing durable benchmark target was found; consider creating a concept, workflow, or expert page only if the idea will be reused."]
    notes: list[str] = []
    for item in benchmark_candidates[:3]:
        notes.append(
            f"Compare against [[{item['id']}]] ({item['type']}) and promote only the reusable delta."
        )
    return notes


def _compile_promotion_candidates(
    *,
    domain: str | None,
    benchmark_candidates: list[dict[str, Any]],
    keywords: list[str],
) -> list[dict[str, Any]]:
    candidates: list[dict[str, Any]] = []
    if domain:
        candidates.append(
            {
                "target_id": domain,
                "target_type": "domain",
                "reason": "Source was compiled with this domain binding.",
            }
        )
    for item in benchmark_candidates[:6]:
        candidates.append(
            {
                "target_id": item["id"],
                "target_type": item["type"],
                "reason": f"Search overlap score {item['score']} from title/keyword matching.",
            }
        )
    if not candidates and keywords:
        candidates.append(
            {
                "target_id": None,
                "target_type": "concept",
                "reason": f"Consider a reusable concept page around `{keywords[0]}` if this idea appears in multiple sources.",
            }
        )
    return candidates


def _keywords(text: str, limit: int = 12) -> list[str]:
    stopwords = {
        "the", "and", "that", "with", "for", "this", "from", "into", "your", "wiki", "raw", "source", "article",
        "you", "was", "were", "are", "have", "has", "had", "they", "them", "their", "there", "what", "when",
        "where", "who", "why", "how", "about", "like", "just", "been", "being", "then", "than", "also", "very",
        "much", "more", "most", "some", "such", "only", "would", "could", "should", "into", "after", "before",
        "over", "under", "because", "through", "while", "film", "films", "movie", "movies", "work", "really",
        "but", "did", "does", "doing", "done", "get", "gets", "got", "going", "went", "come", "came", "make",
        "made", "making", "say", "says", "said", "one", "two", "three", "all", "any", "each", "every", "our",
        "their", "its", "his", "her", "hers", "him", "she", "he", "we", "us", "than", "then", "can", "not",
    }
    counter: Counter[str] = Counter()
    filtered_lines = [line for line in text.splitlines() if not _is_ignorable_source_line(line)]
    for match in WORD_RE.finditer("\n".join(filtered_lines)):
        word = match.group(0).lower()
        if word not in stopwords:
            counter[word] += 1
    return [word for word, _count in counter.most_common(limit)]


def _sentences_from_text(text: str) -> list[str]:
    parts = re.split(r"(?<=[.!?。！？])\s+", text)
    return [_clean_line(part) for part in parts if _clean_line(part)]


def _truncate(text: str, limit: int) -> str:
    cleaned = _clean_line(text)
    if len(cleaned) <= limit:
        return cleaned
    return cleaned[: limit - 3].rstrip() + "..."


def _ordered_unique(values: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        if value and value not in seen:
            seen.add(value)
            result.append(value)
    return result


def _is_ignorable_source_line(line: str) -> bool:
    cleaned = _clean_line(line)
    if not cleaned:
        return True
    if _parse_raw_source_metadata_line(cleaned) is not None:
        return True
    lowered = cleaned.lower()
    noise_markers = (
        "lead photo",
        "all images courtesy",
        "photo by ",
        "photographed by ",
    )
    return any(marker in lowered for marker in noise_markers)


def _benchmark_candidates(query: str, root: Path) -> list[dict[str, Any]]:
    return [
        {"id": item["id"], "title": item["title"], "type": item["type"], "score": item["score"]}
        for item in search_pages(query, limit=12, root=root)
        if item["type"] not in {"source", "log", "index"}
    ][:8]


def _source_page_body(
    *,
    source_id: str,
    title: str,
    raw_relpath: str,
    domain: str | None,
    summary: str,
    metadata: dict[str, str],
    lifecycle: SourceLifecycle,
    headings: list[str],
    claims: list[str],
    condensed_takeaways: list[str],
    challenge_notes: list[str],
    benchmark_notes: list[str],
    benchmark_candidates: list[dict[str, Any]],
    promotion_candidates: list[dict[str, Any]],
    suggested_links: list[str],
) -> str:
    domain_line = f"- Domain: [[{domain}]]\n" if domain else ""
    metadata_lines = _source_metadata_lines(metadata)
    lifecycle_lines = _source_lifecycle_lines(lifecycle)
    takeaway_lines = "\n".join(f"- {takeaway}" for takeaway in condensed_takeaways) or "- No takeaways extracted automatically."
    heading_lines = "\n".join(f"- {heading}" for heading in headings) or "- No headings detected."
    claim_lines = "\n".join(f"- {claim}" for claim in claims) or "- No concrete claims detected automatically."
    challenge_lines = "\n".join(f"- {note}" for note in challenge_notes) or "- No challenge notes generated."
    benchmark_note_lines = "\n".join(f"- {note}" for note in benchmark_notes) or "- No benchmark notes generated."
    candidate_lines = "\n".join(f"- [[{item['id']}]] ({item['type']}, score {item['score']})" for item in benchmark_candidates) or "- No benchmark candidates found."
    promotion_lines = _promotion_candidate_lines(promotion_candidates)
    link_lines = "\n".join(f"- [[{page_id}]]" for page_id in suggested_links) or "- No links suggested."
    return f"""# {title}

## Summary

{summary}

## Compile Status

- Source id: `{source_id}`
- Raw original: `{raw_relpath}`
{domain_line}
{lifecycle_lines}

## Source Metadata

{metadata_lines}

## Condensed Takeaways

{takeaway_lines}

## Condensed Structure

{heading_lines}

## Extracted Claims

{claim_lines}

## Challenge Notes

{challenge_lines}

## Benchmark / Transfer

{benchmark_note_lines}

## Benchmark Candidates

{candidate_lines}

## Promotion Candidates

{promotion_lines}

## Compile Actions

- Review this source page manually.
- Promote durable ideas into concepts, experts, domains, workflows, or templates.
- Add explicit source links on every promoted page.
- If this source contradicts another source, mark the conflict on the durable page.

## Links

{link_lines}

## Sources

- `{raw_relpath}`
"""


def _source_lifecycle_lines(lifecycle: SourceLifecycle) -> str:
    return "\n".join(
        [
            f"- Status: {lifecycle.status}",
            f"- Review status: {lifecycle.review_status}",
            f"- Promotion status: {lifecycle.promotion_status}",
            f"- Compiled at: {lifecycle.compiled_at}",
            f"- Compile version: {lifecycle.compile_version}",
        ]
    )


def _source_metadata_lines(metadata: dict[str, str]) -> str:
    if not metadata:
        return "- No structured metadata detected."
    ordered_keys = ("source_url", "publisher", "published", "author", "expert", "role")
    labels = {
        "source_url": "Source URL",
        "publisher": "Publisher",
        "published": "Published",
        "author": "Author",
        "expert": "Expert",
        "role": "Role",
    }
    lines: list[str] = []
    for key in ordered_keys:
        value = metadata.get(key)
        if value:
            lines.append(f"- {labels[key]}: {value}")
    return "\n".join(lines) if lines else "- No structured metadata detected."


def _maintain_next_actions(
    compile_result: dict[str, Any],
    promotion_report: dict[str, Any],
    health: dict[str, Any],
) -> list[str]:
    actions: list[str] = []
    if compile_result["written_count"]:
        actions.append("Review and promote the newly compiled source drafts into durable pages.")
    if promotion_report["candidate_count"]:
        actions.append("Use promotion_candidates to update concepts, experts, domains, workflows, or templates.")
    if health["broken_links"]:
        actions.append("Fix broken wikilinks before relying on search or backlinks.")
    if health["missing_index_entries"]:
        actions.append("Add missing durable pages to wiki/index.md.")
    if not actions:
        actions.append("No source maintenance action is currently required.")
    return actions


def _promotion_candidate_lines(candidates: list[dict[str, Any]]) -> str:
    if not candidates:
        return "- No promotion candidates generated."
    lines: list[str] = []
    for item in candidates:
        target_id = item.get("target_id")
        target_type = item.get("target_type", "page")
        reason = item.get("reason", "Candidate target.")
        if target_id:
            lines.append(f"- [[{target_id}]] ({target_type}) - {reason}")
        else:
            lines.append(f"- New {target_type} page - {reason}")
    return "\n".join(lines)


def _compiled_draft_tracking(pages: list[Page]) -> dict[str, list[str]]:
    pending_review: list[str] = []
    missing_tracking: list[str] = []
    required_fields = ("review_status", "promotion_status", "compiled_at", "compile_version")
    for page in pages:
        if page.type != "source":
            continue
        if page.frontmatter.get("status") != "compiled-draft":
            continue
        pending_review.append(page.id)
        if any(not page.frontmatter.get(field) for field in required_fields):
            missing_tracking.append(page.id)
    return {
        "pending_review": sorted(pending_review),
        "missing_tracking": sorted(missing_tracking),
    }


def _missing_required_sections(pages: list[Page]) -> list[dict[str, str]]:
    required = {
        "source": {
            "summary": ["## Summary", "## 摘要"],
            "sources": ["## Sources", "## 来源"],
        },
        "expert": {
            "role": ["## Role", "## 角色"],
            "research inputs": ["## Research Inputs", "## 研究输入"],
        },
        "concept": {
            "definition": ["## Definition", "## 定义"],
            "links": ["## Links", "## 链接"],
        },
        "workflow": {
            "links": ["## Links", "## 链接"],
        },
    }
    missing: list[dict[str, str]] = []
    for page in pages:
        for section_name, alternatives in required.get(page.type, {}).items():
            if not any(section in page.body for section in alternatives):
                missing.append({"page": page.id, "missing": " / ".join(alternatives)})
    return missing


def _insert_under_heading(text: str, heading: str, entry: str) -> str:
    lines = text.splitlines(keepends=True)
    for index, line in enumerate(lines):
        if line.strip() == heading:
            insert_at = index + 1
            while insert_at < len(lines) and lines[insert_at].strip() == "":
                insert_at += 1
            lines.insert(insert_at, entry)
            return "".join(lines)
    return text.rstrip() + "\n\n" + heading + "\n\n" + entry


def _clean_line(line: str) -> str:
    return re.sub(r"\s+", " ", line.replace("\u00a0", " ")).strip()


def _project_overview_body(slug: str, title: str, domain: str) -> str:
    return f"""# {title}

## Purpose

Define the concrete outcome for this project.

## Domain

- Domain: [[{domain}]]

## Success Criteria

- The project has a clear brief.
- The required expert pages are selected before execution.
- Decisions and working notes are captured during execution.
- A postmortem feeds lessons back into durable wiki pages.

## Active Expert Roles

- Add only the expert pages this project needs.

## Project Files

- Brief: [[{slug}-brief]]
- Action plan: [[{slug}-action-plan]]
- Decisions: [[{slug}-decisions]]
- Working notes: [[{slug}-working-notes]]
- Review: [[{slug}-review]]
- Postmortem: [[{slug}-postmortem]]

## Current Status

Project created. Brief not finalized.

## Links

- [[project-index]]
- [[project-start-workflow]]
"""


def _project_brief_body(title: str) -> str:
    return f"""# {title} Brief

## Context

Why are we doing this now?

## Goal

What concrete outcome should exist at the end?

## Audience / User

Who is this for?

## Constraints

- Time:
- Budget:
- Tools:
- Platform:
- Quality bar:

## Inputs

- Existing sources:
- Reference materials:
- User preferences:

## Non-Goals

- ...

## Open Questions

- ...
"""


def _project_action_plan_body(title: str) -> str:
    return f"""# {title} Action Plan

## Steps

1. Finalize brief.
2. Select expert pages.
3. Create working artifacts.
4. Review against selected experts.
5. Write postmortem.
6. Promote durable lessons back into the wiki.

## Current Next Action

- Finalize the brief.
"""


def _project_decisions_body(title: str) -> str:
    return f"""# {title} Decisions

## Decisions

- No project decisions recorded yet.
"""


def _project_working_notes_body(title: str) -> str:
    return f"""# {title} Working Notes

## Notes

- No working notes recorded yet.
"""


def _project_review_body(title: str) -> str:
    return f"""# {title} Review

## Review

- No review completed yet.
"""


def _project_postmortem_body(title: str) -> str:
    return f"""# {title} Postmortem

## What Worked

- ...

## What Failed

- ...

## Lessons To Promote

- ...

## Pages To Update

- ...
"""

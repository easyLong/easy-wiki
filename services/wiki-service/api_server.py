from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, unquote, urlparse

from wiki_core import (
    append_log,
    compile_missing_sources,
    compile_source,
    create_project,
    get_page,
    health_check,
    lint,
    list_pages,
    page_detail,
    page_links,
    page_record,
    backlinks,
    search_pages,
    source_usage,
)


class WikiRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        path = parsed.path.rstrip("/") or "/"
        query = parse_qs(parsed.query)

        if path == "/health":
            self._json({"status": "ok"})
            return

        if path == "/pages":
            self._list_pages(query)
            return

        if path == "/search":
            q = query.get("q", [""])[0]
            limit = int(query.get("limit", ["10"])[0])
            self._json({"query": q, "results": search_pages(q, limit=limit)})
            return

        if path == "/lint":
            self._json(lint())
            return

        if path == "/healthcheck":
            self._json(health_check())
            return

        if path == "/sources/usage":
            self._json(source_usage())
            return

        if path.startswith("/pages/") and path.endswith("/links"):
            page_id = unquote(path.removeprefix("/pages/").removesuffix("/links").strip("/"))
            page = get_page(page_id)
            if not page:
                self._not_found(page_id)
                return
            self._json(
                {
                    "id": page.id,
                    "links": page_links(page),
                    "backlinks": backlinks(page.id),
                }
            )
            return

        if path.startswith("/pages/"):
            page_id = unquote(path.removeprefix("/pages/"))
            page = get_page(page_id)
            if not page:
                self._not_found(page_id)
                return
            self._json(page_detail(page))
            return

        self._json({"error": "unknown endpoint"}, status=404)

    def do_POST(self) -> None:
        parsed = urlparse(self.path)
        path = parsed.path.rstrip("/") or "/"
        payload = self._read_json()

        try:
            if path in {"/compile-source", "/ingest"}:
                source_path = str(payload.get("source_path", ""))
                if not source_path:
                    self._json({"error": "source_path is required"}, status=400)
                    return
                result = compile_source(
                    source_path,
                    title=payload.get("title"),
                    domain=payload.get("domain"),
                    apply=bool(payload.get("apply", True)),
                )
                self._json(result, status=201 if result["written"] else 200)
                return

            if path in {"/compile-missing-sources", "/scan-raw"}:
                limit_value = payload.get("limit")
                limit = int(limit_value) if limit_value is not None else None
                result = compile_missing_sources(
                    domain=payload.get("domain"),
                    apply=bool(payload.get("apply", True)),
                    limit=limit,
                )
                status = 201 if result["written_count"] else 200
                self._json(result, status=status)
                return

            if path == "/projects":
                slug = str(payload.get("slug", ""))
                if not slug:
                    self._json({"error": "slug is required"}, status=400)
                    return
                result = create_project(
                    slug,
                    title=payload.get("title"),
                    domain=payload.get("domain", "ai-short-drama-domain-overview"),
                    apply=bool(payload.get("apply", True)),
                )
                self._json(result, status=201)
                return

            if path == "/log":
                category = str(payload.get("category", "note"))
                message = str(payload.get("message", ""))
                if not message:
                    self._json({"error": "message is required"}, status=400)
                    return
                entry = append_log(category, message)
                self._json({"written": True, "entry": entry}, status=201)
                return
        except FileNotFoundError as exc:
            self._json({"error": "file not found", "detail": str(exc)}, status=404)
            return
        except ValueError as exc:
            self._json({"error": "invalid request", "detail": str(exc)}, status=400)
            return

        self._json({"error": "unknown endpoint"}, status=404)

    def log_message(self, format: str, *args: object) -> None:
        return

    def _list_pages(self, query: dict[str, list[str]]) -> None:
        page_type = query.get("type", [None])[0]
        tag = query.get("tag", [None])[0]
        domain = query.get("domain", [None])[0]
        project = query.get("project", [None])[0]
        records = []
        for page in list_pages():
            if page_type and page.type != page_type:
                continue
            if tag and tag not in page.tags:
                continue
            if domain and page.frontmatter.get("domain") != domain:
                continue
            if project and page.frontmatter.get("project") != project:
                continue
            records.append(page_record(page))
        self._json({"pages": records})

    def _not_found(self, page_id: str) -> None:
        self._json({"error": "page not found", "id": page_id}, status=404)

    def _read_json(self) -> dict[str, object]:
        length = int(self.headers.get("Content-Length", "0"))
        if length == 0:
            return {}
        body = self.rfile.read(length).decode("utf-8")
        try:
            payload = json.loads(body)
        except json.JSONDecodeError:
            return {}
        return payload if isinstance(payload, dict) else {}

    def _json(self, payload: object, status: int = 200) -> None:
        body = json.dumps(payload, ensure_ascii=False, indent=2).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def main() -> None:
    server = ThreadingHTTPServer(("127.0.0.1", 8765), WikiRequestHandler)
    print("Wiki service listening on http://127.0.0.1:8765")
    server.serve_forever()


if __name__ == "__main__":
    main()

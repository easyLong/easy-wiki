from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, unquote, urlparse

from wiki_core import (
    get_page,
    lint,
    list_pages,
    page_detail,
    page_links,
    page_record,
    backlinks,
    search_pages,
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

    def log_message(self, format: str, *args: object) -> None:
        return

    def _list_pages(self, query: dict[str, list[str]]) -> None:
        page_type = query.get("type", [None])[0]
        tag = query.get("tag", [None])[0]
        records = []
        for page in list_pages():
            if page_type and page.type != page_type:
                continue
            if tag and tag not in page.tags:
                continue
            records.append(page_record(page))
        self._json({"pages": records})

    def _not_found(self, page_id: str) -> None:
        self._json({"error": "page not found", "id": page_id}, status=404)

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

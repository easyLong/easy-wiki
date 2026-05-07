from __future__ import annotations

import json
import sys
import traceback
from typing import Any

from wiki_core import (
    append_log,
    backlinks,
    compile_missing_sources,
    compile_source,
    create_project,
    get_page,
    health_check,
    lint,
    list_pages,
    maintain_sources,
    page_detail,
    page_links,
    page_record,
    promotion_candidates,
    search_pages,
    source_usage,
)


JSONRPC_VERSION = "2.0"
SUPPORTED_PROTOCOL_VERSIONS = (
    "2025-11-05",
    "2025-06-18",
    "2025-03-26",
)
SERVER_INFO = {
    "name": "easy-wiki",
    "title": "Easy Wiki MCP Server",
    "version": "0.1.0",
}


class McpError(Exception):
    def __init__(self, code: int, message: str, data: Any | None = None) -> None:
        super().__init__(message)
        self.code = code
        self.message = message
        self.data = data


def _tool_definitions() -> list[dict[str, Any]]:
    return [
        {
            "name": "wiki_list_pages",
            "title": "List Wiki Pages",
            "description": "List wiki pages with optional filters for type, tag, domain, and project.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "type": {"type": "string"},
                    "tag": {"type": "string"},
                    "domain": {"type": "string"},
                    "project": {"type": "string"},
                },
                "additionalProperties": False,
            },
        },
        {
            "name": "wiki_read_page",
            "title": "Read Wiki Page",
            "description": "Read a page by id, including frontmatter, content, links, and backlinks.",
            "inputSchema": {
                "type": "object",
                "properties": {"id": {"type": "string"}},
                "required": ["id"],
                "additionalProperties": False,
            },
        },
        {
            "name": "wiki_search",
            "title": "Search Wiki Pages",
            "description": "Search wiki pages by query text.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "query": {"type": "string"},
                    "limit": {"type": "integer", "minimum": 1},
                },
                "required": ["query"],
                "additionalProperties": False,
            },
        },
        {
            "name": "wiki_get_links",
            "title": "Get Wiki Links",
            "description": "Return outbound links and backlinks for a page id.",
            "inputSchema": {
                "type": "object",
                "properties": {"id": {"type": "string"}},
                "required": ["id"],
                "additionalProperties": False,
            },
        },
        {
            "name": "wiki_lint",
            "title": "Lint Wiki",
            "description": "Run the wiki link and metadata lint checks.",
            "inputSchema": {
                "type": "object",
                "properties": {},
                "additionalProperties": False,
            },
        },
        {
            "name": "wiki_healthcheck",
            "title": "Wiki Healthcheck",
            "description": "Run the stronger weekly wiki health report.",
            "inputSchema": {
                "type": "object",
                "properties": {},
                "additionalProperties": False,
            },
        },
        {
            "name": "wiki_source_usage",
            "title": "Source Usage",
            "description": "Inspect raw/source coverage and durable usage.",
            "inputSchema": {
                "type": "object",
                "properties": {},
                "additionalProperties": False,
            },
        },
        {
            "name": "wiki_promotion_candidates",
            "title": "Source Promotion Candidates",
            "description": "List source drafts that need review, promotion, or durable usage.",
            "inputSchema": {
                "type": "object",
                "properties": {},
                "additionalProperties": False,
            },
        },
        {
            "name": "wiki_append_log",
            "title": "Append Wiki Log",
            "description": "Append an entry to wiki/log.md.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "category": {"type": "string"},
                    "message": {"type": "string"},
                },
                "required": ["message"],
                "additionalProperties": False,
            },
        },
        {
            "name": "wiki_create_project",
            "title": "Create Wiki Project",
            "description": "Create a new project folder from templates.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "slug": {"type": "string"},
                    "title": {"type": "string"},
                    "domain": {"type": "string"},
                    "apply": {"type": "boolean"},
                },
                "required": ["slug"],
                "additionalProperties": False,
            },
        },
        {
            "name": "wiki_compile_source",
            "title": "Compile Raw Source",
            "description": "Compile a raw original into a source-page draft.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "source_path": {"type": "string"},
                    "title": {"type": "string"},
                    "domain": {"type": "string"},
                    "apply": {"type": "boolean"},
                },
                "required": ["source_path"],
                "additionalProperties": False,
            },
        },
        {
            "name": "wiki_compile_missing_sources",
            "title": "Compile Missing Sources",
            "description": "Scan raw/ for files without source pages and compile them in batch.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "domain": {"type": "string"},
                    "apply": {"type": "boolean"},
                    "limit": {"type": "integer", "minimum": 1},
                },
                "additionalProperties": False,
            },
        },
        {
            "name": "wiki_maintain_sources",
            "title": "Maintain Sources",
            "description": "Compile new raw files and report review, promotion, and source closure status.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "domain": {"type": "string"},
                    "apply": {"type": "boolean"},
                    "limit": {"type": "integer", "minimum": 1},
                },
                "additionalProperties": False,
            },
        },
        {
            "name": "wiki_ingest_source",
            "title": "Ingest Raw Source",
            "description": "Alias for compiling a raw source into a source-page draft.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "source_path": {"type": "string"},
                    "title": {"type": "string"},
                    "domain": {"type": "string"},
                    "apply": {"type": "boolean"},
                },
                "required": ["source_path"],
                "additionalProperties": False,
            },
        },
    ]


def _require_string(args: dict[str, Any], key: str) -> str:
    value = args.get(key)
    if not isinstance(value, str) or not value.strip():
        raise McpError(-32602, f"`{key}` must be a non-empty string.")
    return value


def _optional_string(args: dict[str, Any], key: str) -> str | None:
    value = args.get(key)
    if value is None:
        return None
    if not isinstance(value, str):
        raise McpError(-32602, f"`{key}` must be a string.")
    return value


def _optional_int(args: dict[str, Any], key: str, default: int) -> int:
    value = args.get(key, default)
    if not isinstance(value, int):
        raise McpError(-32602, f"`{key}` must be an integer.")
    return value


def _optional_bool(args: dict[str, Any], key: str, default: bool) -> bool:
    value = args.get(key, default)
    if not isinstance(value, bool):
        raise McpError(-32602, f"`{key}` must be a boolean.")
    return value


def _filter_pages(args: dict[str, Any]) -> list[dict[str, Any]]:
    page_type = _optional_string(args, "type")
    tag = _optional_string(args, "tag")
    domain = _optional_string(args, "domain")
    project = _optional_string(args, "project")
    records: list[dict[str, Any]] = []
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
    return records


def _call_tool(name: str, args: dict[str, Any]) -> Any:
    if name == "wiki_list_pages":
        return {"pages": _filter_pages(args)}

    if name == "wiki_read_page":
        page_id = _require_string(args, "id")
        page = get_page(page_id)
        if not page:
            raise McpError(-32602, f"Page `{page_id}` was not found.")
        return page_detail(page)

    if name == "wiki_search":
        query = _require_string(args, "query")
        limit = _optional_int(args, "limit", 10)
        return {"query": query, "results": search_pages(query, limit=limit)}

    if name == "wiki_get_links":
        page_id = _require_string(args, "id")
        page = get_page(page_id)
        if not page:
            raise McpError(-32602, f"Page `{page_id}` was not found.")
        return {"id": page.id, "links": page_links(page), "backlinks": backlinks(page.id)}

    if name == "wiki_lint":
        return lint()

    if name == "wiki_healthcheck":
        return health_check()

    if name == "wiki_source_usage":
        return source_usage()

    if name == "wiki_promotion_candidates":
        return promotion_candidates()

    if name == "wiki_append_log":
        category = _optional_string(args, "category") or "note"
        message = _require_string(args, "message")
        entry = append_log(category, message)
        return {"written": True, "entry": entry}

    if name == "wiki_create_project":
        slug = _require_string(args, "slug")
        title = _optional_string(args, "title")
        domain = _optional_string(args, "domain") or "ai-short-drama-domain-overview"
        apply = _optional_bool(args, "apply", True)
        return create_project(slug, title=title, domain=domain, apply=apply)

    if name == "wiki_compile_missing_sources":
        domain = _optional_string(args, "domain")
        apply = _optional_bool(args, "apply", True)
        limit = None if "limit" not in args else _optional_int(args, "limit", 1)
        return compile_missing_sources(domain=domain, apply=apply, limit=limit)

    if name == "wiki_maintain_sources":
        domain = _optional_string(args, "domain")
        apply = _optional_bool(args, "apply", True)
        limit = None if "limit" not in args else _optional_int(args, "limit", 1)
        return maintain_sources(domain=domain, apply=apply, limit=limit)

    if name in {"wiki_compile_source", "wiki_ingest_source"}:
        source_path = _require_string(args, "source_path")
        title = _optional_string(args, "title")
        domain = _optional_string(args, "domain")
        apply = _optional_bool(args, "apply", True)
        return compile_source(source_path, title=title, domain=domain, apply=apply)

    raise McpError(-32601, f"Unknown tool `{name}`.")


def _tool_result(payload: Any) -> dict[str, Any]:
    text = json.dumps(payload, ensure_ascii=False, indent=2)
    return {
        "content": [{"type": "text", "text": text}],
        "structuredContent": payload,
    }


class McpServer:
    def __init__(self) -> None:
        self._initialized = False

    def serve(self) -> int:
        for raw_line in sys.stdin:
            line = raw_line.strip()
            if not line:
                continue
            responses = self._handle_line(line)
            for response in responses:
                self._write_message(response)
        return 0

    def _handle_line(self, line: str) -> list[dict[str, Any]]:
        try:
            payload = json.loads(line)
        except json.JSONDecodeError as exc:
            return [self._error_response(None, -32700, f"Invalid JSON: {exc.msg}")]

        if isinstance(payload, list):
            responses: list[dict[str, Any]] = []
            for item in payload:
                response = self._handle_message(item)
                if response is not None:
                    responses.append(response)
            return responses

        response = self._handle_message(payload)
        return [response] if response is not None else []

    def _handle_message(self, message: Any) -> dict[str, Any] | None:
        if not isinstance(message, dict):
            return self._error_response(None, -32600, "Request must be a JSON object.")

        if message.get("jsonrpc") != JSONRPC_VERSION:
            return self._error_response(message.get("id"), -32600, "Only JSON-RPC 2.0 is supported.")

        method = message.get("method")
        if not isinstance(method, str):
            return self._error_response(message.get("id"), -32600, "Request is missing a string method.")

        is_notification = "id" not in message
        params = message.get("params", {})
        if params is None:
            params = {}
        if not isinstance(params, dict):
            return self._error_response(message.get("id"), -32602, "Params must be an object.")

        try:
            if method == "initialize":
                return self._result_response(message.get("id"), self._handle_initialize(params))

            if method == "notifications/initialized":
                self._initialized = True
                return None

            if method == "ping":
                return None if is_notification else self._result_response(message.get("id"), {})

            if not self._initialized:
                raise McpError(-32002, "Server not initialized.")

            if method == "tools/list":
                return self._result_response(message.get("id"), {"tools": _tool_definitions()})

            if method == "tools/call":
                tool_name = params.get("name")
                arguments = params.get("arguments", {})
                if not isinstance(tool_name, str) or not tool_name:
                    raise McpError(-32602, "`name` must be a non-empty string.")
                if arguments is None:
                    arguments = {}
                if not isinstance(arguments, dict):
                    raise McpError(-32602, "`arguments` must be an object.")
                payload = _call_tool(tool_name, arguments)
                return self._result_response(message.get("id"), _tool_result(payload))

            if is_notification:
                return None
            raise McpError(-32601, f"Method `{method}` is not supported.")
        except McpError as exc:
            if is_notification:
                return None
            return self._error_response(message.get("id"), exc.code, exc.message, exc.data)
        except Exception as exc:  # pragma: no cover - safety path
            if is_notification:
                return None
            return self._error_response(
                message.get("id"),
                -32603,
                f"Internal error: {exc}",
                {"traceback": traceback.format_exc()},
            )

    def _handle_initialize(self, params: dict[str, Any]) -> dict[str, Any]:
        client_version = params.get("protocolVersion")
        if isinstance(client_version, str) and client_version in SUPPORTED_PROTOCOL_VERSIONS:
            protocol_version = client_version
        else:
            protocol_version = SUPPORTED_PROTOCOL_VERSIONS[0]
        return {
            "protocolVersion": protocol_version,
            "capabilities": {"tools": {"listChanged": False}},
            "serverInfo": SERVER_INFO,
        }

    def _result_response(self, request_id: Any, result: Any) -> dict[str, Any]:
        return {"jsonrpc": JSONRPC_VERSION, "id": request_id, "result": result}

    def _error_response(self, request_id: Any, code: int, message: str, data: Any | None = None) -> dict[str, Any]:
        error: dict[str, Any] = {"code": code, "message": message}
        if data is not None:
            error["data"] = data
        return {"jsonrpc": JSONRPC_VERSION, "id": request_id, "error": error}

    def _write_message(self, message: dict[str, Any]) -> None:
        sys.stdout.write(json.dumps(message, ensure_ascii=False) + "\n")
        sys.stdout.flush()


def main() -> int:
    if hasattr(sys.stdin, "reconfigure"):
        sys.stdin.reconfigure(encoding="utf-8")
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")
    server = McpServer()
    return server.serve()


if __name__ == "__main__":
    raise SystemExit(main())

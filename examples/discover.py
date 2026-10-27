#!/usr/bin/env python3
"""Anonymous Geonode MCP discovery. No tool calls or API credentials."""

import argparse
import json
import sys
import urllib.error
import urllib.request

ENDPOINT = "https://mcp.geonode.com/mcp"
PROTOCOL_VERSION = "2025-03-26"
ALLOWED_METHODS = {"initialize", "notifications/initialized", "tools/list"}


def read_result(response, request_id):
    """Read JSON or SSE until the matching JSON-RPC response arrives."""
    if "text/event-stream" not in response.headers.get("Content-Type", ""):
        messages = [json.loads(response.read().decode("utf-8"))]
    else:
        messages = sse_messages(response)
    for message in messages:
        if message.get("id") != request_id:
            continue
        if "error" in message:
            error = message["error"]
            raise ValueError(f"MCP error {error.get('code')}: {error.get('message')}")
        if "result" not in message:
            raise ValueError("MCP response has no result")
        return message["result"]
    raise ValueError("No matching MCP response received")


def sse_messages(response):
    data = []
    for raw_line in response:
        line = raw_line.decode("utf-8").rstrip("\r\n")
        if not line:
            if data:
                yield json.loads("\n".join(data))
                data = []
        elif line.startswith("data:"):
            data.append(line[5:].removeprefix(" "))
    if data:
        yield json.loads("\n".join(data))


def post(message, headers, opener):
    if message["method"] not in ALLOWED_METHODS:
        raise ValueError("This discovery example does not invoke tools")
    request = urllib.request.Request(
        ENDPOINT,
        data=json.dumps(message).encode("utf-8"),
        headers=headers,
        method="POST",
    )
    return opener(request, timeout=30)


def discover(opener=urllib.request.urlopen):
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream",
    }
    with post(
        {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": PROTOCOL_VERSION,
                "capabilities": {},
                "clientInfo": {"name": "geonode-discovery-example", "version": "0.1.0"},
            },
        },
        headers,
        opener,
    ) as response:
        initialized = read_result(response, 1)
        session_id = response.headers.get("Mcp-Session-Id")
    negotiated = initialized.get("protocolVersion")
    if negotiated != PROTOCOL_VERSION:
        raise ValueError(f"Unsupported negotiated protocol version: {negotiated}")
    headers["MCP-Protocol-Version"] = negotiated
    if session_id:
        headers["Mcp-Session-Id"] = session_id
    with post(
        {"jsonrpc": "2.0", "method": "notifications/initialized"}, headers, opener
    ):
        pass
    tools = []
    cursor = None
    for page in range(20):
        request_id = page + 2
        message = {"jsonrpc": "2.0", "id": request_id, "method": "tools/list"}
        if cursor:
            message["params"] = {"cursor": cursor}
        with post(message, headers, opener) as response:
            result = read_result(response, request_id)
        tools.extend(result.get("tools", []))
        cursor = result.get("nextCursor")
        if not cursor:
            return {
                "endpoint": ENDPOINT,
                "protocolVersion": negotiated,
                "serverInfo": initialized.get("serverInfo", {}),
                "tools": tools,
                "toolsInvoked": 0,
            }
    raise ValueError("Tool discovery exceeded 20 pages; inspect the server response")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--connect", action="store_true", help="Send anonymous discovery requests to Geonode"
    )
    args = parser.parse_args(argv)
    if not args.connect:
        print(f"Endpoint: {ENDPOINT}")
        print("Methods: initialize, notifications/initialized, tools/list")
        print("No network requests made. Add --connect to discover tools; no tool is invoked.")
        return 0
    try:
        print(json.dumps(discover(), indent=2))
    except (urllib.error.URLError, ValueError, TimeoutError) as error:
        print(f"Discovery failed: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

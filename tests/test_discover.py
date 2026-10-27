import importlib.util
import io
import json
from pathlib import Path
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location(
    "discover", Path(__file__).resolve().parents[1] / "examples" / "discover.py"
)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class Response(io.BytesIO):
    def __init__(self, value, *, sse=False, headers=None):
        data = json.dumps(value)
        super().__init__((f": keepalive\nevent: message\ndata: {data}\n\n" if sse else data).encode())
        self.headers = {"Content-Type": "text/event-stream" if sse else "application/json"}
        self.headers.update(headers or {})


class DiscoveryTests(unittest.TestCase):
    def test_discovery_negotiates_session_and_paginates_without_calling_tools(self):
        requests = []
        responses = [
            Response({"jsonrpc": "2.0", "id": 1, "result": {
                "protocolVersion": "2025-03-26", "serverInfo": {"name": "fixture"}
            }}, sse=True, headers={"Mcp-Session-Id": "test-session"}),
            Response({}),
            Response({"id": 2, "result": {"tools": [{"name": "extract"}], "nextCursor": "page2"}}),
            Response({"id": 3, "result": {"tools": [{"name": "other"}]}}, sse=True),
        ]

        def opener(request, timeout):
            self.assertEqual(timeout, 30)
            self.assertEqual(request.full_url, module.ENDPOINT)
            requests.append(request)
            return responses.pop(0)

        result = module.discover(opener)
        messages = [json.loads(request.data) for request in requests]
        self.assertEqual([m["method"] for m in messages], [
            "initialize", "notifications/initialized", "tools/list", "tools/list"
        ])
        self.assertEqual(messages[-1]["params"], {"cursor": "page2"})
        self.assertEqual(requests[1].get_header("Mcp-session-id"), "test-session")
        self.assertEqual(requests[1].get_header("Mcp-protocol-version"), "2025-03-26")
        self.assertTrue(all(request.get_header("X-api-key") is None for request in requests))
        self.assertEqual([tool["name"] for tool in result["tools"]], ["extract", "other"])
        self.assertEqual(result["toolsInvoked"], 0)

    def test_default_command_does_not_connect(self):
        with patch.object(module, "discover", side_effect=AssertionError("Network forbidden")):
            with patch("sys.stdout", new_callable=io.StringIO):
                self.assertEqual(module.main([]), 0)

    def test_tool_calls_are_rejected_before_network(self):
        with self.assertRaisesRegex(ValueError, "does not invoke tools"):
            module.post({"method": "tools/call"}, {}, lambda *_: self.fail("Network forbidden"))

    def test_rpc_error_is_reported(self):
        with self.assertRaisesRegex(ValueError, "MCP error -32600"):
            module.read_result(Response({"id": 1, "error": {"code": -32600, "message": "Bad request"}}), 1)

    def test_mismatched_response_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "No matching"):
            module.read_result(Response({"id": 99, "result": {}}), 1)

    def test_unknown_protocol_does_not_continue(self):
        calls = []

        def opener(request, timeout):
            calls.append(request)
            return Response({"id": 1, "result": {"protocolVersion": "unknown"}})

        with self.assertRaisesRegex(ValueError, "Unsupported negotiated"):
            module.discover(opener)
        self.assertEqual(len(calls), 1)


if __name__ == "__main__":
    unittest.main()

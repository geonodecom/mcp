# Anonymous discovery example

`examples/discover.py` uses Python's standard library. Run it without flags to inspect the request plan, or add `--connect` to make metadata requests to the fixed Geonode endpoint.

The example requests MCP protocol `2025-03-26`, the version observed in the existing 2026-10-21 metadata check. It stops if the server negotiates a different version rather than claiming support for an untested protocol revision.

The exchange is:

1. `initialize`, with an empty capability set and a descriptive client name.
2. `notifications/initialized`, preserving a server-issued session ID when present.
3. `tools/list`, following pagination cursors up to a bounded 20 pages.

HTTP requests accept both JSON and SSE. For SSE, the reader stops after the matching JSON-RPC response, so it need not wait for a long-lived stream to close. Requests have a 30-second timeout. The output includes tool definitions and input schemas, plus `toolsInvoked: 0`.

This is a small inspection example, not a general MCP client library. It intentionally has no tool-execution method, credential handling, automatic retries, subscription support or local-server mode. The tests use in-memory fixtures and perform no network requests.

An earlier metadata check observed the anonymous tool `extract`; this new script was validated offline during repository preparation and has not itself been run against production. Neither check establishes authenticated scraping success or installation in an assistant.

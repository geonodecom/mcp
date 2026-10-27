# Connecting an MCP client

Use the remote Streamable HTTP endpoint `https://mcp.geonode.com/mcp`. The earlier address, `https://scraper.geonode.io/mcp`, serves the same server and keeps working. Your client must support remote HTTP MCP; clients that only support local stdio servers need a separately evaluated bridge. This repository does not ship one.

For a client-specific walkthrough, start at the [Geonode MCP overview](https://docs.geonode.com/docs/scraper-api/guides/mcp/00_overview). Use the client's current official documentation for where it stores server configuration and credentials.

## Authentication

Discovery can run anonymously. Only `extract` is exposed without a key, and the anonymous request schema and limits apply. For account access, use the exact header `X-Api-Key`, configured using your client's secure credential mechanism. Do not substitute a Bearer token or put the key into the server URL.

The [prerequisites guide](https://docs.geonode.com/docs/scraper-api/guides/mcp/01_before-you-start) and [keyless guide](https://docs.geonode.com/docs/scraper-api/guides/mcp/01_use-without-an-api-key) describe current requirements. Plan-backed calls use account allowance and limits.

## Validate the right result

- A reachable endpoint proves network connectivity.
- Successful initialization and `tools/list` prove protocol discovery.
- A tool execution response proves that a particular invocation returned; inspect its error state and content before claiming extraction succeeded.
- An assistant's summary should be grounded in that returned content and identify the source URL.

## Troubleshooting

| Symptom | Check |
| --- | --- |
| HTTP 406 or unsupported response | Client must accept `application/json` and `text/event-stream`. |
| Only `extract` appears | Confirm that the client sends `X-Api-Key`, then refresh its tool list. |
| Authentication failure | Confirm the active dashboard key and credential binding without printing the key. |
| Session/protocol error | Reinitialize; preserve any returned `Mcp-Session-Id` and the negotiated protocol version. |
| Rate limit | Respect the response and documented limits; do not loop immediate retries. |
| Unexpected tool arguments | Read the current tool's `inputSchema`. MCP tool names and envelopes differ from the CLI and Python toolkit. |

Do not retry billable job submissions blindly after a timeout. A transport failure does not prove that the server did not accept the request.

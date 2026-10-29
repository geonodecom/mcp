# Source and release boundary

This repository is documentation and client-side examples for the existing hosted Geonode MCP endpoint. The production server is implemented separately in the private Scraper API backend. Backend code, credentials, deployment configuration and server history are not included here.

The public MCP registry identity is `com.geonode/mcp`, published from this repository's `server.json`. It replaces `io.geonode/scraper`, which the registry now marks as deprecated with a pointer here; that endpoint keeps working for existing installs. Registry publication and hosted deployment continue through their existing processes; no new release workflow, package registry entry or server artifact is created by this repository.

## Registry version

The running server is the one source of the version. The backend's `MCP_VERSION` is what `initialize` reports, and `server.json` carries the same string. Both move together for each release that changes the tools, their descriptions or the profile fields (title, description, website, icons), not for every deploy. Registry versions are immutable, so any change to `server.json` needs a new version.

To release: deploy the server, set the same version and fields here, then run `python scripts/check_live.py`. It reads the live `serverInfo` from the endpoint in `remotes` and fails unless the version, title, description, website and icons match. Publish only after it passes.

The example's client version is an identifier for diagnostic requests, not a server or package release. A future bridge or distributable server would need its own design, tests, dependency boundary and release decision.

Guidance is based on the Geonode MCP documentation, the existing anonymous metadata evidence checked 2026-10-21, and the public API schema. Brand artwork and MIT license are reused from Geonode-owned project materials. New example code is included under that license. No third-party implementation was copied.

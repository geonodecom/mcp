# Source and release boundary

This repository is documentation and client-side examples for the existing hosted Geonode MCP endpoint. The production server is implemented separately in the private Scraper API backend. Backend code, credentials, deployment configuration and server history are not included here.

The public MCP registry identity is `com.geonode/mcp`, published from this repository's `server.json`. It replaces `io.geonode/scraper`, which stays listed so existing installs keep working. Registry publication and hosted deployment continue through their existing processes; no new release workflow, package registry entry or server artifact is created by this repository.

The example's client version is an identifier for diagnostic requests, not a server or package release. A future bridge or distributable server would need its own design, tests, dependency boundary and release decision.

Guidance is based on the Geonode MCP documentation, the existing anonymous metadata evidence checked 2026-10-21, and the public API schema. Brand artwork and MIT license are reused from Geonode-owned project materials. New example code is included under that license. No third-party implementation was copied.

## Signup offer release check

The README uses the product-owner-approved launch copy, “Sign up to get 10,000 free credits” (21 October 2026). Before public release, verify that the live signup flow and account credit allocation match this offer. This copy update does not configure billing or issue credits.

## Cross-link deployment handoff

The README and package homepage link to the live [integrations hub](https://geonode.com/integrations). The intended detail destination is `https://geonode.com/integrations/mcp`; it is a deployment target, not a verified public page. After that detail page is deployed and checked, replace the hub fallback in README/package metadata with the detail URL and retain an API documentation link.

Source metadata targets `https://github.com/geonodecom/mcp`; the repository remains private until its separate release decision. These local metadata edits do not alter an existing PyPI/npm listing. Carry them into the authoritative publishing source at the coordinated next release, then verify the registry's rendered README, source/issue links and homepage. Keep existing package names, versions and import identifiers unchanged during preparation.

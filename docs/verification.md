# Verification

Checked locally on 2026-10-21 with Python 3.13.2. Six standard-library unit tests passed: JSON/SSE discovery with session headers and pagination, no-network default invocation, rejecting tool calls, JSON-RPC errors, mismatched IDs and unsupported protocol negotiation. Python compilation passed and the default script invocation printed its plan without networking.

These tests use in-memory fixtures. The new script has not been run against production. Existing earlier anonymous metadata evidence is described separately in the discovery guide; no authenticated scraping, client installation, package release or backend deployment is claimed.

SVGs parse successfully; local Markdown links resolve. A bounded credential-pattern scan found no private-key headers or long literal credential assignments. It does not replace a security audit.

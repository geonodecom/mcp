# Geonode MCP Server: workflow recipes and output guide

[Repository overview](../README.md) · [Geonode documentation](https://docs.geonode.com/docs/scraper-api/guides/mcp/00_overview)

## Example: extract a page and answer with sources

1. Configure the hosted endpoint in a client that supports remote Streamable HTTP MCP, then refresh its tools.
2. Start with the extract tool available through anonymous discovery, or configure X-Api-Key through the client's secure credentials for account access.
3. Ask the assistant to extract https://example.com as Markdown, summarize the returned page, and include its source URL.
4. Inspect the actual tool response for an error before trusting the summary. Discovery alone does not prove that extraction completed.

**Expected result:** The tool supplies page content and the assistant writes the answer. This repository supplies setup guides and a discovery example, not a model or a self-hosted scraping backend.

## Choose the right connection

Use MCP when your assistant discovers and calls tools through the Model Context Protocol. Use the Python or TypeScript SDK when your application owns the request flow, or the CLI for shell scripts.

Use the native Make.com, Zapier or self-hosted n8n connector when building scenarios or workflows in those platforms. Their available operations and access requirements differ from the MCP tool list.

Anonymous access exposes limited extraction. For authenticated access, discover the actual tool schemas in your connected client instead of copying tool names or arguments from a framework toolkit.

Source-reviewed recipes; authenticated workflow execution has not been tested in this review.

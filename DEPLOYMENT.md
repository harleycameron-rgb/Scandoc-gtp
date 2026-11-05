# SCANDOC deployment readiness

## Current status
The repository is publicly readable, but the MCP endpoint is NOT publicly deployed or connected to the ChatGPT plugin directory.

## Required before public hosting
1. Implement and test OAuth or another ChatGPT-compatible user authorization flow, including correct resource metadata and token validation.
2. Apply per-user and per-IP rate limits, bounded request bodies, request timeouts and resource limits.
3. Add structured audit events without logging private payloads.
4. Run integration tests against the actual remote MCP endpoint, including unauthorized and malformed requests.
5. Review dependency licenses, choose a project license, and complete security review.
6. Configure a production host that supports MCP Streamable HTTP. Dockerfile is suitable for a container host; a long-running `python server.py` process must not be assumed to work on Vercel Functions.
7. Connect the endpoint in ChatGPT and complete applicable publication/review steps.

Do not publish a server URL until the endpoint has been tested and authenticated.

"""MCP Streamable HTTP server using the official MCP Python SDK."""
from mcp.server.fastmcp import FastMCP
from engine import root_scour, velocity_splat, double_snapshot, receipt, verify_receipt, octopus_mode

mcp = FastMCP('SCANDOC', stateless_http=True, json_response=True, host='0.0.0.0', port=8000)

@mcp.tool()
def scandoc_root_scour(before: dict, after: dict) -> dict:
    """Compare two explicit feature maps; no claim of identity or authenticity."""
    return root_scour(before,after)

@mcp.tool()
def scandoc_velocity_splat(before: list[float], after: list[float], dt: float=1.0) -> dict:
    """Finite-difference displacement on aligned vectors, not measured physical velocity."""
    return velocity_splat(before,after,dt)

@mcp.tool()
def scandoc_double_snapshot(before: dict, after: dict) -> dict:
    """Compare two structured snapshots with SHA-512 commitments, without trusted timestamps."""
    return double_snapshot(before,after)

@mcp.tool()
def scandoc_sentinel_receipt(payload: dict) -> dict:
    """Generate a deterministic SHA-512 content commitment, not a provenance attestation."""
    return receipt(payload)

@mcp.tool()
def scandoc_verify_receipt(payload: dict, digest: str) -> dict:
    """Verify a SHA-512 commitment against a JSON payload."""
    return verify_receipt(payload,digest)

@mcp.tool()
def scandoc_octopus_mode(faces: dict, tick: int, genesis_digest: str|None=None) -> dict:
    """Build a CLOSED-GATE state with six named faces and two temporal arms."""
    return octopus_mode(faces,tick,genesis_digest)

if __name__=='__main__':
    mcp.run(transport='streamable-http')

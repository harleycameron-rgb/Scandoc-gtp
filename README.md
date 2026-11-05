# SCANDOC ChatGPT MCP Plugin v0.1

Public research preview for Waxtablet / SCANDOC. Implements structured Root Scour, numeric Velocity Splat, Double Snapshot, SHA-512 Sentinel commitments and closed-gate Octopus Mode.

**Status:** research prototype; not deployed as a hosted ChatGPT connector. Do not expose the demo HTTP server to the public internet without authentication, rate limiting and input controls.

## Local setup

```sh
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
python server.py
```

The local MCP Streamable HTTP endpoint is `http://localhost:8000/mcp`.

## Scope

Root Scour compares declared JSON fields, not images. Velocity Splat computes finite differences, not measured motion. Double Snapshot compares structured JSON records. Sentinel SHA-512 commitments establish content equality, not provenance or trusted timestamps. Octopus Mode retains a CLOSED gate and makes no persistent writes. No scientific validation is claimed.

## Tools

`scandoc_root_scour`, `scandoc_velocity_splat`, `scandoc_double_snapshot`, `scandoc_sentinel_receipt`, `scandoc_verify_receipt`, `scandoc_octopus_mode`.

See `engine.py`, `server.py`, and `tests/test_engine.py`. This release is shared for review; licensing terms have not yet been selected.

# Python CLI/Daemon Preferences

This reference captures preferred stack and standards for Python CLI+daemon delivery.

# Modern Python CLI + Daemon Stack

## Use this skill when

- You are defining architecture or standards for `meshctl`/`meshd` or `spawnctl`/`spawnd`.
- You need contract-first Python implementation with systemd-native operations.
- You want OSS-aligned defaults while preserving a Rust convergence path.

## Positioning

- Python is the thin-client and orchestration layer.
- Core daemon runtime and critical adapters converge to Rust.

## Tool composition

- CLI framework: `typer` (primary), `click` (substrate for edge/custom parameters).
- Terminal UX: `rich`, `rich.traceback`, `RichHandler`.
- Contracts: `pydantic v2`, `TypeAdapter[...]`, `model_json_schema()`.
- Config/path model: `xdg-base-dirs`, `dataconfy`, `pyyaml`, optional `tomllib` and JSON payloads.
- Env config strategy: explicit env mapping or `pydantic-settings`.
- Logging: JSONL audit logger + Rich operator logger.
- Execution safety: `subprocess` argv lists, persisted stdout/stderr artifacts, idempotency/correlation IDs.
- systemd integration: `sdnotify`, explicit restart/timeouts, hardening defaults, optional `dbus-next`, optional controlled `systemd-run` wrappers.
- Testing: `pytest`, `click.testing.CliRunner`, `hypothesis`, optional schema snapshot tests.
- Packaging: `pyproject.toml` (PEP 621), console entry points for `meshctl`/`meshd` and `spawnctl`/`spawnd`, operator install via `pipx`.
- Quality gates: `ruff`, `pyright` or `mypy`, `pre-commit`, CI blocks on lint/type/test/schema failures.

## Contract policy

- Canonical runtime contracts are Pydantic v2 models.
- Baseline model set includes `event_envelope_v1`, `action_request_v1`, `action_result_v1`, and profile/config models.
- Schema/version policy is additive and backward-compatible for minor versions.
- Fail fast on invalid critical config; no silent fallback.

## CLI generation policy (OAPI/Proto)

- Do not fully generate operator CLIs from OpenAPI/proto.
- Generate typed clients/stubs from contracts for request/response types and transport clients.
- Keep CLI hand-authored for command UX, policy gates/prompts, multi-step orchestration, and operator output.

## Reference layering

- `core`: pure logic, contracts, state transitions, routing/execution decisions.
- `adapters`: imperative shell for CLI, systemd, and IO (jsonl, yaml/toml, filesystem, subprocess).
- Keep CLI/daemon codepaths separated (`*_ctl` vs `*_d`).

## Defaults

- Treat audit JSONL as operational source of truth.
- Version every externally consumed contract.
- Add deprecation shims only with a removal milestone.
- Do not re-embed daemon-core behavior in Python after Rust parity is reached.

## Implementation checklist

1. Confirm Python thin-layer boundary and Rust convergence target.
2. Define Pydantic contracts and export JSON Schema.
3. Implement XDG-aware config loading with `dataconfy`, then validate with Pydantic.
4. Wire dual logging channels (JSONL audit + Rich operator).
5. Add systemd readiness and service hardening defaults.
6. Add tests (`pytest`, `CliRunner`, `hypothesis`) and CI quality gates.
7. Generate typed clients from OpenAPI/proto and keep CLI UX hand-authored.

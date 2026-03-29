---
name: implement
description: "Use this skill to execute approved bounded batches through gated delivery: consume the request contract, emit canonical response artifacts, and keep apply behind explicit promotion gates."
compatibility: "Requires an approved plan or equivalent execution contract. Uses dry-run by default; apply requires explicit approval and passing evidence gate."
allowed-tools: "Bash(scripts/validate_implement_packet.py:*) Bash(scripts/generate_implement_packet.py:*) Read"
metadata:
  author: _404
  version: "1.0"
---

# Implement

Use this skill after planning, when execution must be traceable, gated, and reversible.

## Trigger

- User asks to execute an approved bounded batch.
- `PLAN/request.instance.json`, `PLAN/request.validation.json`, and `PLAN/contract.bindings.json` exist.

## Output contract

Generate implementation artifacts under `$wt/IMPLEMENT/*`.
`wt` is the source-repo integration worktree. If loop control is active, `ledger_wt` is separate and is used later for review manifests and bundle materialization.

Required files:
- `$wt/IMPLEMENT/IMPLEMENT.md`
- `$wt/IMPLEMENT/packet.meta.json`
- `$wt/IMPLEMENT/response.instance.json`
- `$wt/IMPLEMENT/response.manifest.json`
- `$wt/IMPLEMENT/response.validation.json`

Within `IMPLEMENT.md`, produce sections in this exact order:

1. `artifact_paths`
2. `execution_context`
3. `scope_lock`
4. `issue_map`
5. `work_queue`
6. `evidence_required`
7. `gates`
8. `execution`
9. `results`
10. `rollback`
11. `closeout_decision`

## Rules

- `apply` is disallowed unless `closeout_decision` is `APPROVED` and evidence gate is `PASS`.
- `response.instance.json` must validate against `schemas/review_response.schema.json`.
- `response.manifest.json` must validate against `schemas/response.schema.json`.
- Response manifest bundle contents must not include `response.manifest.json`.
- Prefer file artifacts under `$wt/IMPLEMENT/*`; avoid terminal-only output.

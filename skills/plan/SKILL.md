---
name: plan
description: Use this skill when the user asks for plan-first execution. Produce a bounded-batch, git-flow-aware plan before any code/runtime changes, with explicit gates, promotion intent, and rollback.
compatibility: Requires repository and service inspection commands; no runtime mutation until explicit user approval.
allowed-tools: Bash(scripts/generate_plan_packet.py:*) Bash(scripts/validate_plan_packet.py:*) Bash(gh:*) Read
metadata:
  author: _404
  version: "2.0"
---

# Plan

Use this skill for plan-first requests where execution must be preceded by explicit analysis, bounded batch definition, and promotion gating.

## Trigger

- User asks for `plan`, `analysis`, `blueprint`, `run the standard plan`, or equivalent.
- Contract-first git flow is in effect.
- The main prompt remains unchanged; workflow authority lives outside the prompt.

## Output file contract

Generate planning artifacts under `$wt/PLAN/*` (where `wt` is the source-repo integration worktree provided by loop/init).
When loop control is active, `ledger_wt` may also be supplied for downstream review materialization, but planning artifacts themselves still live under `$wt/PLAN/*`.

Required files:
- `$wt/PLAN/README.md`
- `$wt/PLAN/packet.meta.json`
- `$wt/PLAN/request.instance.json`
- `$wt/PLAN/request.validation.json`
- `$wt/PLAN/contract.bindings.json`
- `$wt/PLAN/batch.manifest.json`
- `$wt/PLAN/integration_gate.plan.json`
- `$wt/PLAN/promotion.plan.json`

Within `README.md`, produce sections in this exact order:

1. `artifact_paths`
2. `bounded_batch`
3. `contract_context`
4. `problem_set`
5. `scope`
6. `assets_required`
7. `assets_impacted`
8. `dependency_matrix`
9. `integration_worktree_plan`
10. `gate_plan`
11. `promotion_plan`
12. `rollback_plan`
13. `decision`
14. `implement`
15. `success_criteria`

## Execution Shape

1. `assets/sequence_dag.md`
2. `assets/workflow.json`
3. `assets/interface.json`
4. `assets/README.plan.template.md`
5. `references/*.md`

## Rules

- Collect evidence before dependency/gap claims.
- Keep assumptions explicit and testable.
- Prefer file artifacts under `$wt/PLAN/*`; avoid terminal-only output.
- `request.instance.json` must validate against `schemas/request.schema.json`.
- `contract.bindings.json` must validate against `schemas/contract_bindings.schema.json`.
- `batch.manifest.json` must validate against `schemas/batch_manifest.schema.json`.
- `integration_gate.plan.json` must validate against `schemas/integration_gate_plan.schema.json`.
- `promotion.plan.json` must validate against `schemas/promotion_plan.schema.json`.
- In `dependency_matrix`, include proof refs and mark evidence as `observed` or `inferred`.
- Include pass/fail gate and rollback for the bounded batch.
- End with explicit `decision` section: `APPROVED`, `REJECTED`, or `NEEDS_INFO` + rationale.
- `implement` must reference `control/git-flow/implement/README.md` and include execution mode (`dry-run|apply`).

## Scripts

- `scripts/generate_plan_packet.py --objective "..." [--failure "..."] [--contract-root "."] [--wt "$WT"] [--bounded-batch-id "..."] [--target-layer shell|implementation|contract] [--target-branch main] [--mode full|body] [--out "$wt/PLAN/README.md"] [--force]`
- `scripts/validate_plan_packet.py [PATH] [--wt "$WT"] [--contract-root "."] [--mode scaffold|ready]`

## References

- `references/contract_layer.md`
- `references/decision_semantics.md`
- `references/template_generation.md`
- `references/plan_packet_validation.md`
- `control/git-flow/plan/README.md`

---
name: json-tool
description: "Use this skill for contract-first JSON operations: normalize or validate JSON artifacts, derive downstream JSON with jq/jaq, evaluate invariant facts, prepare policy inputs, and render human-facing outputs from schema-bound contracts."
compatibility: "Best for JSON-first workflows with canonical JSON Schema contracts. Uses worker_packets as the packet-contract authority and treats CUE/CEL/OPA/MiniJinja as layered support, not co-equal authorities."
metadata:
  author: _404
  version: "0.1"
---

# JSON Tool

Use this skill when the task is primarily JSON contract work rather than ad hoc prose processing.

## Trigger

- Define or revise JSON contracts, envelopes, traces, signals, or packet schemas.
- Normalize machine-generated JSON/JSONL into canonical internal types.
- Derive downstream JSON artifacts with deterministic transforms.
- Prepare validation facts or policy inputs over already-shaped objects.
- Render Markdown or payload outputs from accepted JSON artifacts.

## Rules

- `JSON Schema` is the canonical accepted-artifact authority.
- `CUE` is optional and upstream only: use it for incomplete-state unification or interlingua work when required.
- `jq` is the default wrangling engine; use `jaq` only when Rust embedding is required.
- `CEL` computes local invariants and `validation_facts`; it does not replace `jq` or `OPA/Rego`.
- `OPA/Rego` decides authorization over valid state plus facts; do not duplicate low-level object checks in policy.
- `MiniJinja` renders outputs only; it must not become the contract or policy authority.
- Canonical worker packet contracts and packet instances live in `/home/_404/src/worker_packets`.

## Execution Shape

1. `assets/interface.json`
2. `assets/workflow.json`
3. `assets/sequence_dag.md`
4. `assets/operator_surface.json`
5. `assets/telemetry_artifacts.json`
6. `assets/telemetry_pipeline.json`
7. `references/stack.md`
8. `references/worker_packets.md`
9. `references/telemetry_profile.md`
10. `scripts/validate_json_contract.py`

## Output guidance

Choose the minimal operator path that matches the task:
- unstructured ingress: `extract -> unify -> validate -> derive -> check -> authorize -> render`
- structured ingress: `unify|validate -> derive -> check -> authorize -> render`

Prefer JSON outputs first. Render Markdown only after the JSON artifacts and validation reports are stable.

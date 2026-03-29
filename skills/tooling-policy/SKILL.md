---
name: tooling-policy
description: "Use this skill when deciding tool authority, promotion boundaries, or which official tool/skill must own a workflow step. Keeps proposal_register as the promotion gate, specify-proposal as proposal ingress, json-tool as the authoritative JSON actuator, and worker_packets as runtime packet authority."
compatibility: "Policy/meta-skill only. Use to resolve authority drift, ad hoc tool usage, promotion-path ambiguity, or conflicts between discussions, proposal packets, and canonical repos."
metadata:
  author: _404
  version: "0.1"
---

# Tooling Policy

Use this skill when a task touches authority boundaries between discussion packets, proposal packets, official skills, canonical contract repos, and runtime consumers.

## Trigger

- A workflow step could be owned by more than one tool or repo.
- A user asks which tool should own execution, validation, promotion, or rendering.
- A discussion artifact is at risk of being treated as authoritative.
- A new contract family or runtime surface is being introduced.

## Rules

- `proposal_register` is the only promotion gate for new contract families.
- `specify-proposal` is the ingress/meta-skill for proposal normalization and gating.
- Whenever a workflow crosses a JSON boundary, `json-tool` is the authoritative actuator unless a narrower canonical wrapper already exists.
- `worker_packets` owns canonical worker packet contracts, telemetry contracts, fixtures, transforms, and packet instances.
- `discussions/*` are non-authoritative working docs and evidence packets.
- `spawn` owns runtime execution, worker dispatch, and system-impacting lifecycle control after proposal gating passes.
- Do not introduce ad hoc direct tool usage where an approved wrapper or official skill already exists.

## Decision tests

1. Does this change define or alter a contract family?
- Route through `specify-proposal` and `proposal_register`.

2. Does this step transform, validate, derive, check, authorize, or render JSON?
- Route through `json-tool`.

3. Does this step operate on worker packets, telemetry packets, fixtures, or pilot instances?
- Route through `worker_packets`.

4. Does this step change live runtime behavior, authority, or host reach?
- Route through `spawn`, but only after proposal gating.

5. Is this only evidence, draft prose, raw telemetry, or exploratory analysis?
- Keep it under `discussions/*` until promoted.

## Output guidance

When applying this skill, produce a concise authority decision:
- authoritative owner
- subordinate tool/skill
- promotion path, if any
- non-authoritative working area, if any

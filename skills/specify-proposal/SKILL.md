---
name: specify-proposal
description: "Use this meta-skill as guidance-first workflow scaffolding to turn a proposal/problem statement into gated proposal artifacts for proposal_register, leveraging json-tool for any JSON normalization, validation, derivation, or rendering work."
compatibility: "Meta-skill only. Guidance-first, contract-later. Keeps proposal_register as the promotion gate and treats json-tool as the authoritative JSON actuator whenever the workflow crosses a JSON boundary."
metadata:
  author: _404
  version: "0.1"
---

# Specify Proposal

Use this skill when a new proposal, contract family, or architectural packet must be formalized and gated before it becomes canonical.

At the current maturity level, treat this skill as workflow guidance and policy direction, not as a fully machine-complete contract engine.

## Trigger

- A new proposal domain or contract family needs definition.
- Discussion artifacts must be normalized into a proposal packet.
- A discussion packet must be promoted into `proposal_register`.
- A future canonical contract must be gated before promotion.

## Rules

- `proposal_register` is the promotion gate. Nothing becomes canonical without proposal gating.
- `specify-proposal` is a meta-skill. It orchestrates proposal normalization and gating; it is not the contract engine itself.
- Whenever the workflow crosses a JSON boundary before, during, or after a step, `json-tool` is the authoritative actuator.
- Keep this skill concise until a dedicated machine-readable interface is defined.
- Do not promote discussion stubs directly into live contracts.

## Current posture

- Use this skill as guidance-first scaffolding.
- Expect to refine it from real proposal runs.
- When the workflow hits ambiguity, treat that as a missing contract surface to be named and tightened, not as a reason to improvise silently.

Typical refinement points are:
- missing normalized proposal shape
- missing artifact naming or identity rules
- missing pre-JSON extraction/normalization rules
- missing gate and completeness criteria

## Minimal lifecycle

1. Bind the source problem or proposal input.
2. Identify whether the input is already in the required proposal shape or still needs pre-JSON extraction/normalization.
3. Normalize it into the current best-known internal proposal shape.
4. Gate completeness and underspecification.
4. Emit:
   - `spec_draft`
   - `proposal_register`
   - gate result
5. Promote only after gate pass.

## Output guidance

Required outputs are proposal artifacts, not runtime implementations:
- `spec_draft.v1.json`
- `proposal_register.v1.json`
- explicit gate outcome with underspecified items when present

Treat these as current artifact expectations and naming guidance, not as permanently fixed filenames unless a dedicated machine-readable contract says so.

## Subordinate stack

Use `json-tool` for:
- JSON normalization
- contract validation
- deterministic derivation
- render/export of reviewable artifacts

Use surrounding workflow judgment for:
- source binding
- pre-JSON extraction when the input is still prose or mixed discussion material
- identifying missing contract surfaces that should be refined into the skill or into proposal artifacts

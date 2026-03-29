# Git Flow: Plan

Phase-scoped planning instructions for the tri-phase contract.

Plan responsibilities:
- define the bounded batch on the contract branch or equivalent source authority
- emit the request-side contract packet under `$wt/PLAN`
- bind the batch to explicit gate, promotion, and rollback semantics
- keep plan output reviewable and replayable through the ledger

Plan packet minimum:
- `PLAN/README.md`
- `PLAN/request.instance.json`
- `PLAN/request.validation.json`
- `PLAN/contract.bindings.json`
- `PLAN/batch.manifest.json`
- `PLAN/integration_gate.plan.json`
- `PLAN/promotion.plan.json`

Plan review rule:
- plan approval is required before any bounded implementation slice may execute
- plan-level promotion evidence must describe only the plan packet, not implementation outputs that do not exist yet

Contract branch / integration worktree split:
- plan defines the approved bounded slice on the contract side
- implementation later executes that slice in the bounded integration worktree

Primary authority files:
- `control/git-flow/git_flow.manifest.json`
- `control/git-flow/git_flow.dag.json`
- `control/git-flow/plan/README.md`
- `prompt-registry/manifest.json`

Phase rule:
- plan owns bounded-batch definition, authority mapping, promotion intent, and rollback shape
- plan does not perform runtime implementation

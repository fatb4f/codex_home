# CLI Extension V2 Proposal

This proposal generalizes the shell-first extension profile into a runtime-neutral CLI profile.

It does not rewrite or invalidate the approved first shell slice.

It exists to:
- replace `shell_cli_role` with `cli_role`
- replace shell-specific lineage wording with runtime-neutral wording
- split implementation and verification targets by runtime family

Files:
- `spec_draft.v2.json`
- `proposal_register.v2.json`
- `gate_result.v2.json`
- `extension_profile.v2.json`
- `hof_prospect.v1.md`

Current status:
- proposal draft for runtime-neutral refactor

Direction:
- canonical metadata model remains authority
- runtime assets remain projection-only
- shell and Python adapters become runtime families under one CLI profile
- `hof` is tracked as a projection-generation-orchestration prospect, not a runtime adapter

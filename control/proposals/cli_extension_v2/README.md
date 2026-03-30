# CLI Extension V2 Proposal

This proposal generalizes the shell-first extension profile into a runtime-neutral CLI profile.

It does not rewrite or invalidate the approved first shell slice.

It exists to:
- replace `shell_cli_role` with `cli_role`
- replace shell-specific lineage wording with runtime-neutral wording
- split implementation and verification targets by runtime family

Files:
- `basis/metadata/canonical_semantic_model.schema.json`
- `basis/metadata/projection_artifact_manifest.schema.json`
- `basis/shell_cli_extension/extension_profile.v1.json`
- `basis/shell_cli_extension/extension_constraints.example.json`
- `basis/shell_cli_extension/python_cli_prospect.v1.md`
- `basis/shell_cli_extension/jsonargparse_projection_matrix.v1.json`
- `spec_draft.v2.json`
- `proposal_register.v2.json`
- `gate_result.v2.json`
- `extension_profile.v2.json`
- `extension_constraints.v2.json`
- `extension_constraints.v2.schema.json`
- `canonical_semantic_model.cli.example.json`
- `projection_artifact_manifest.cli.example.json`
- `compatibility_assessment.v2.json`
- `hof_prospect.v1.md`

Current status:
- proposal draft with runtime-neutral constraints, example artifacts, and compatibility assessment
- portable review basis is vendored locally under `basis/`

Direction:
- canonical metadata model remains authority
- runtime assets remain projection-only
- shell and Python adapters become runtime families under one CLI profile
- `hof` is tracked as a projection-generation-orchestration prospect, not a runtime adapter

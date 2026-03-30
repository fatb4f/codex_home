# Git Substrate Adapters V1 Proposal

This proposal opens the Git-substrate adapter-contract lane on top of the stabilized CLI realization pattern.

It does not implement `gix` or `sem`.

It exists to:
- classify `gix` and `sem` as projected Git-substrate adapters
- keep canonical metadata authority separate from Git adapter outputs
- define the first target-contract boundary for deterministic Git-state and semantic-diff projections
- reuse the normalized realization pattern instead of inventing a parallel adapter workflow

Files:
- `spec_draft.v1.json`
- `extension_profile.v1.json`
- `gix_target_contract.v1.json`
- `sem_target_contract.v1.json`
- `proposal_register.v1.json`
- `gate_result.v1.json`

Current status:
- proposal draft for Git-substrate projected adapters
- `gix` is scoped as the deterministic Git fact surface
- `sem` is scoped as the semantic diff enrichment surface
- target contracts exist at the proposal boundary
- implementation and verification runners are intentionally deferred

Direction:
- canonical metadata remains authority
- runtime assets remain projection-only
- Git adapter outputs are structured operational artifacts, not authority
- `gix` and `sem` are projected adapters over the Git substrate
- implementation must reuse the normalized realization pattern already established in `cli_extension_v2`

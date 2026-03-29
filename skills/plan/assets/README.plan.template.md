# Plan Packet

## artifact_paths
- `wt`:
- Packet: `$wt/PLAN/README.md`
- Metadata: `$wt/PLAN/packet.meta.json`
- Request: `$wt/PLAN/request.instance.json`
- Request validation: `$wt/PLAN/request.validation.json`
- Contract bindings: `$wt/PLAN/contract.bindings.json`
- Batch manifest: `$wt/PLAN/batch.manifest.json`
- Integration gate plan: `$wt/PLAN/integration_gate.plan.json`
- Promotion plan: `$wt/PLAN/promotion.plan.json`

## bounded_batch
- Bounded batch ID: <bounded_batch_id>
- Target layer: <target_layer>
- Target branch: <target_branch>
- Integration worktree ID: <integration_worktree_id>
- Deliverables:
  - <deliverable_1>

## contract_context
- Git flow manifest: `control/git-flow/git_flow.manifest.json`
- Git flow DAG: `control/git-flow/git_flow.dag.json`
- Prompt registry: `prompt-registry/manifest.json`
- Contract root: <contract_root>

## problem_set
- Objective: <objective>
- Failure signatures: <failure>
- Expected behavior:
- User impact:

## scope
- In scope:
- Out of scope:
- Constraints:
- Assumptions:

## assets_required
| asset | reason | status |
|---|---|---|
| <fill> | <fill> | ready |

## assets_impacted
| asset | impact |
|---|---|
| <fill> | <fill> |

## dependency_matrix
| asset | dependency | gap | evidence_or_proof | inferred |
|---|---|---|---|---|
| <fill> | <fill> | <fill> | <fill> | observed |

## integration_worktree_plan
- Integration surface: one integration worktree per bounded batch
- Base ref: `main`
- Worktree path: <worktree_path>
- Worktree audit object: `false`
- Evidence audit object: `true`

## gate_plan
- Authority gate scope: parent contract conformance
- Contract package gate scope: child contract validity
- Artifact conformance gate scope: runtime artifacts under merged child contract
- Required checks:
  - <check_1>

## promotion_plan
- Promotion mode: `patch_promotion`
- Target branch: <target_branch>
- Required evidence refs:
  - <evidence_ref_1>
- Post-promotion gates:
  - main_authority_gate
  - main_contract_package_gate
  - main_artifact_conformance_gate

## rollback_plan
- Rollback mode: retain worktree and reject promotion
- Rollback trigger:
- Recovery action:

## decision
- Status: `APPROVED` | `REJECTED` | `NEEDS_INFO`
- Decision rationale:
- Blocking items (if `REJECTED`):
- Required follow-up evidence:

## implement
- Mode: `dry-run`
- Git flow reference: `control/git-flow/plan/README.md`
- Evidence required:
  - <fill>
- Execution command(s):

## success_criteria
- [ ] Request and batch artifacts validate.
- [ ] Required checks are enumerated for the integration worktree.
- [ ] Promotion path is explicit and rollback-aware.

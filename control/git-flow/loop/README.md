# Git Flow: Loop

Phase-scoped loop instructions for the tri-phase contract:
- contract branch authority remains the source of workflow and schema truth
- one bounded integration worktree is used per loop iteration
- one separate loop-ledger worktree is used for review manifests and bundles

Loop responsibilities:
- initialize `$wt` and `$ledger_wt` explicitly
- route `PLAN -> DECISION -> IMPLEMENT -> VERIFY -> TERMINATE`
- deny execution before `decision == APPROVED`
- keep retry bounded at the verify boundary
- require plan review before implement and implement review before promotion

Loop transition contract:
1. `INIT`
   - establish source repo worktree and ledger worktree
2. `PLAN`
   - produce the request-side packet and bounded-batch contract
3. `DECISION`
   - approve, reject, or return for plan revision
4. `IMPLEMENT`
   - execute only the approved bounded slice in the integration worktree
5. `VERIFY`
   - validate request/response bridge and transition gate
6. `TERMINATE`
   - archive, bundle, and close out

Primary authority files:
- `control/git-flow/git_flow.manifest.json`
- `control/git-flow/git_flow.dag.json`
- `skills/loop/assets/workflow.json`

Phase rule:
- loop owns orchestration, not packet content
- packet content remains owned by the `plan` and `implement` contracts

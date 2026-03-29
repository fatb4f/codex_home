# Git Flow: Implement

Phase-scoped implementation instructions for the tri-phase contract.

Implement responsibilities:
- consume an approved request packet from `$wt/PLAN`
- execute only the approved bounded slice in `$wt`
- emit the response-side packet under `$wt/IMPLEMENT`
- keep apply behind explicit evidence and promotion gates

Implement packet minimum:
- `IMPLEMENT/IMPLEMENT.md`
- `IMPLEMENT/packet.meta.json`
- `IMPLEMENT/response.instance.json`
- `IMPLEMENT/response.manifest.json`
- `IMPLEMENT/response.validation.json`

Integration worktree rules:
- one bounded integration worktree per batch
- keep changes scoped to the approved deliverables
- prefer one logical commit per deliverable when Git operations are in scope
- re-run gates after conflicts or deliverable splits

Promotion rules:
- no promotion without `closeout_decision == APPROVED`
- no promotion without evidence gate `PASS`
- promotion occurs from the integration worktree back to trunk according to the shared manifest/DAG

Primary authority files:
- `control/git-flow/git_flow.manifest.json`
- `control/git-flow/git_flow.dag.json`
- `control/git-flow/implement/README.md`

Phase rule:
- implement owns execution and response evidence
- implement does not redefine loop orchestration or plan authority

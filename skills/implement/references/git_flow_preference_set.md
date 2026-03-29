# Git Flow Preference Set

Use this preference set when execution includes git lifecycle operations.

## Preferred model

- Trunk branch: `main`
- Integration branch/worktree from immutable `base_ref` SHA
- Separate loop-ledger worktree for review manifests and bundles
- One logical commit per deliverable
- Gate per deliverable before stacking next
- Squash promotion to trunk
- Preserve integration lineage via branch/tag

## Command skeleton

```bash
git worktree add ../wt-int-<run_id> -b int/<run_id> <base_sha>

# per deliverable in integration worktree
git add -A
git commit -m "D-001: <summary>"
# run gates

git checkout main
git merge --squash int/<run_id>
git commit -m "promote(<run_id>): D-001..D-00N"
git tag int/<run_id>-final int/<run_id>
```

## Deliverable commit metadata

- `Deliverable: D-<id>`
- `Gate: pass|needs-human`
- `Base-Ref: <sha>`

## Conflict policy

- Resolve on integration branch.
- Re-run gates after resolution.
- Split failing deliverables into smaller commits instead of mixed edits.

## Execution rule

- `apply` only after evidence gate is `PASS`.
- Keep proof refs for gate results in the implement packet.

# Plan Handoff

Execution starts only after a plan packet defines:
- parent issue
- deliverables
- validation gates
- rollback criteria
- `wt` integration worktree path
- `ledger_wt` loop ledger worktree path
- `reproduce_problem_set` to be reused by LOOP terminate (`confirmfix_problem_set`)

Execution packet must preserve deliverable IDs and parent/sub-issue linkage.
Implementation artifacts must be written under `$wt/IMPLEMENT/*`.

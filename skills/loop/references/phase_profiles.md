# Phase profiles

- `INIT`: create or bind the source integration worktree plus the `loop_ledger` worktree.
- `PLAN`: produce the plan packet and request/batch artifacts.
- `IMPLEMENT`: produce the execution packet and response artifacts.
- `VERIFY`: rerun live schema and bridge validation.
- `TERMINATE`: materialize ledger outputs, archive review bundles, and optionally prune one or both worktrees.

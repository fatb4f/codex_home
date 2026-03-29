---
name: loop
description: "Use this meta-skill to orchestrate lifecycle routing across plan and implement with explicit transitions, live contract validation, and ledger-backed handoffs."
compatibility: "Requires child skills: plan and implement. No execution before decision APPROVED."
allowed-tools: "Read Bash(gh:*) Bash(git:*) Bash(scripts/validate_loop_packet.py:*) Bash(scripts/validate_handoff.py:*) Bash(scripts/validate_contract_bridge.py:*)"
metadata:
  author: _404
  version: "1.0"
---

# Loop

Meta-skill for routing and controlling bounded-batch lifecycle loops.

## Worktree contract

- `$wt` is the git-flow integration worktree for the source repo under execution.
- `$ledger_wt` is a separate Git worktree of the loop ledger repo at `/home/_404/src/loop_ledger`.
- `PLAN` and `IMPLEMENT` packets are produced under `$wt/{PLAN,IMPLEMENT}` unless a project-specific contract says otherwise.
- Review manifests, copied evidence, and shareable review bundles are materialized through `$ledger_wt`.
- Do not overload `$wt` to mean the ledger surface. The two paths have different roles and must stay explicit.

## Child skill routing

- `PLAN` phase -> use `plan` skill.
- `IMPLEMENT` phase -> use `implement` skill.
- `VERIFY` phase -> use `scripts/validate_contract_bridge.py`.

## State machine

`INIT -> PLAN -> DECISION -> IMPLEMENT -> VERIFY -> TERMINATE`

Git-flow phase authority:
- `control/git-flow/loop/README.md`
- `control/git-flow/plan/README.md`
- `control/git-flow/implement/README.md`

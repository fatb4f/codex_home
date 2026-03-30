# Shell Script Spec

## Purpose

This spec defines the baseline contract for shell-script surfaces in the managed `/home/_404/src` workspace.

It exists to clear the shell pavement before broader Git-centric adapter work lands.
It also scopes shell surfaces into the earlier metadata model so they are treated as projections rather than authority.

## Scope

This spec applies to managed shell automation surfaces in `/home/_404/src`, especially:
- shared control scripts
- workflow entrypoints
- management automation

It does not treat ad hoc shell snippets as acceptable long-lived control surfaces.
It also does not attempt to govern:
- `.git/**`
- `_notrack/**`
- `_worktrees/**`
- third-party vendor shells except where those surfaces are explicitly adopted as first-class workspace tooling

## Current Baseline

Current tracked shell asset inventory:
- [shell_script_inventory.json](/home/_404/src/codex_home/control/shell/shell_script_inventory.json)

Current baseline assets include:
- `control/github/bootstrap_control_plane_project.sh`
- `kernel/scripts/*.sh`
- `dotfiles/scripts/*.sh`
- `gpt-registry/kernel/project/bundle/*.sh`

## Required Contract

### 0. Metadata-model position

- Shell scripts are projection assets.
- Shell scripts are non-authoritative by default.
- Authority remains in upstream policy, contract, schema, manifest, or registry surfaces.
- A long-lived shell asset should be traceable to:
  - a rooted source context
  - a semantic object or artifact-target role
  - a projection target
  - a projected artifact identity

### 0.1 Upstream contract rule

- A managed shell asset should declare explicit upstream contract refs where practical.
- If a shell surface does not yet have a clear upstream contract, that gap should be visible in the inventory rather than hidden.

### 1. Interpreter and safety

- Shell scripts must use an explicit Bash shebang when Bash semantics are required.
- Shell scripts must fail closed by default.
- `set -euo pipefail` is required unless a narrower justified pattern is documented inline.

### 2. Stable surface

- Long-lived shared shell workflows should not remain raw scripts indefinitely.
- Shared shell workflows should move toward:
  - Bashly for explicit CLI contract
  - Just for stable workflow verb exposure

### 3. Structured outputs

- Structured outputs should be emitted wherever practical.
- Shell surfaces should prefer:
  - JSON
  - NDJSON
  - JSONL
  - line-oriented machine-readable output
- Free-form prose should not be the primary machine boundary where avoidable.

### 4. Deterministic role

- Shell scripts should act as deterministic wrappers or orchestration surfaces.
- They should not hide authority, state, or workflow semantics in incidental output text.
- Inputs, outputs, and side effects should be reviewable from the script contract.
- A shell script may execute a workflow, but it should not become the semantic authority for that workflow.

### 5. Workspace layering

- Shared cross-repo shell policy lives in `codex_home`.
- Repo-local shells may refine or extend that policy for repo-specific workflows.
- A repo-local shell surface should not silently contradict the shared workspace shell contract.

### 6. Growth rule

- New shared shell surfaces should be added to the inventory.
- New shell surfaces should declare:
  - repo
  - projection status
  - authority class
  - upstream contract refs
  - role
  - structured-output expectation
  - transition target, if still pre-Bashly

## Preferred Evolution Path

For long-lived shared shell workflows:

1. inventory the raw script
2. define the CLI/output contract
3. wrap with Bashly
4. expose stable verbs through Just

## Immediate Implication

The current shell estate across `/home/_404/src` is acceptable as a baseline inventory, but it should be treated as transition-state infrastructure rather than a final shell interface model.

## Acceptance Marker

A shared shell workflow in `codex_home` is compliant when:
- it is inventoried
- it is explicitly treated as non-authoritative projection
- it uses a deterministic safety baseline
- it has an upstream contract posture
- it has a structured-output posture
- it has a declared path toward Bashly and Just where long-lived

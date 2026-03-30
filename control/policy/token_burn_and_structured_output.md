# Token-Burn And Structured Output Policy

## Purpose

This policy defines the shared `codex_home` position on token-burn reduction and deterministic operator surfaces.

It exists so these rules do not drift across:
- skills
- control workflows
- shared automation
- repo-local overlays

## Definitions

### token-burn

`token-burn` is the repeated cost of reconstructing workflow state, tool usage, intent, and authority from prose or ad hoc operator behavior.

Common sources include:
- re-deriving Git state from scratch
- re-deriving workflow intent from chat history
- re-explaining tool boundaries
- reinterpreting free-form shell output
- recreating review or evidence state from prose

### deterministic-first

`deterministic-first` means that shared workflows should prefer stable, reproducible, inspectable control surfaces before resorting to free-form interaction.

### structured outputs

`structured outputs` are machine-usable artifacts such as:
- JSON
- NDJSON
- JSONL
- line-oriented key/value outputs
- explicit refs and identifiers

Prose remains useful, but it should be a presentation layer where practical, not the primary machine boundary.

## Policy

1. Shared Codex workflows should reduce token-burn wherever practical.
2. Structured outputs should be emitted wherever practical.
3. Stable wrappers should be preferred over ad hoc command usage.
4. Shared control logic belongs in `codex_home` unless a repo-specific override is truly required.
5. Repo-local overlays should consume shared policy rather than silently redefining it.

## Token-Burn Strategy Substrates

Token-burn strategies are organized by substrate:
- shell
- python
- git

The policy is stable at the substrate level.
Specific tools may evolve, but the substrate responsibilities should remain explicit.

## Required Operator Surface Behaviors

### Shell substrate

- Preferred surfaces:
  - Bashly
  - Just
- Bash-based control surfaces should be composed through Bashly or an equivalently explicit wrapper.
- Just should remain the stable task and workflow verb layer where a named workflow entrypoint is needed.
- Ad hoc shell scripts are not preferred control surfaces for shared workflows.
- Structured outputs should be preferred at the shell boundary wherever practical.

### Python substrate

- Preferred surface:
  - Marimo
- Marimo is the preferred shared surface for Python script/app construction where practical.
- Free-standing Python scripts should be minimized when a Marimo-based surface would keep the workflow more inspectable and materializable.
- Marimo notebooks may call deterministic wrapper surfaces and hydrate notebook state from their outputs.
- In that model, Marimo may serve as a hydratable registry, inspection surface, and derivation surface over deterministic artifacts.
- Deterministic wrappers remain the fact-producing boundary; Marimo should not silently replace or redefine their contracts.

### Git substrate

- Preferred surfaces:
  - `gix`
  - `sem`
- `gix` should be used as the preferred deterministic Git access surface where practical.
- `sem` should be used for semantic diff enrichment where the workflow pattern requires more than changed-file truth.
- Git-centric workflows should prefer stable `repo_state`, `diff_state`, and related structured artifacts over repeated conversational reconstruction.
- Marimo may consume these Git-oriented deterministic artifacts as a hydratable registry layer, but the canonical capture should remain in the wrapper-produced artifacts.

Reference note for recurring Git-centric token-burn patterns:
- `/home/_404/src/src-ctrl/scratch/token-burn-patterns.md`

### JSON boundary

- At JSON boundaries, canonical wrappers should be preferred.
- If no narrower wrapper exists, the authoritative JSON actuator should remain explicit rather than improvised.

### Project and management automation

- Cross-repo management automation should be reproducible from repo state.
- GitHub Project setup, labels, milestones, and related management metadata should be scriptable where the platform allows it.

## Reuse Rule

Repo-local `.codex` or similar overlays may extend these policies, but they should not contradict them without an explicit local contract.

If a workflow is intended to be uniform across repos, its policy belongs here first.

## Current Concrete Surfaces

- `control/github/bootstrap_control_plane_project.sh`
- `control/github/control_plane_project_queries.md`
- `skills/tooling-policy/SKILL.md`
- `control/git-flow/*`
- `src-ctrl/scratch/token-burn-patterns.md` as the current Git-centric pattern note

## Acceptance Marker

`codex_home` is the shared control surface for cross-repo deterministic operator policy, including token-burn reduction and structured-output guidance.

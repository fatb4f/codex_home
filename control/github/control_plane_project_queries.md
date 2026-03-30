# Control Plane Project Queries

Project:
- `Control Plane`
- `https://github.com/users/fatb4f/projects/13`

Use these query conventions in the Project UI or with `gh project item-list --query`.

## Epics

```text
kind:epic
```

## Tranches

```text
kind:tranche
```

## Planned Work

```text
state:planned -status:Done
```

## In Review

```text
state:review
```

## Blocked

```text
state:blocked
```

## Kernel Lane

```text
repo:kernel
```

## src-ctrl Lane

```text
repo:src-ctrl
```

## codex_home Lane

```text
repo:codex-home
```

## scm.pattern

```text
lane:scm-pattern
```

## Metaschema

```text
lane:metaschema
```

## gitops_cell

```text
lane:gitops-cell
```

## codex_home

```text
lane:codex-home
```

## Needs Human Review

```text
gate:needs-human-review
```

## Ready For Realization

```text
gate:ready-for-realization
```

## Stale Basis

```text
gate:stale-basis
```

## Notes

- Project item hierarchy exists through GitHub sub-issues.
- The current `gh project item-list` output does not reliably expose the `Parent issue` field even when the hierarchy is present.
- Use issue hierarchy in GitHub plus these queries as the management view until Projects view automation is exposed cleanly.

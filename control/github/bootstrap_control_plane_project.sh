#!/usr/bin/env bash
set -euo pipefail

OWNER="${OWNER:-fatb4f}"
PROJECT_TITLE="${PROJECT_TITLE:-Control Plane}"
PROJECT_NUMBER="${PROJECT_NUMBER:-}"
REPOS=(
  "kernel"
  "src-ctrl"
  "codex_home"
)

MILESTONES=(
  "M1 scm.pattern normalization"
  "M2 metaschema authority lane"
  "M3 codex_home extraction and policy split"
  "M4 projection workflow alignment"
  "M5 gitops cell contract model"
  "M6 unified reconciliation baseline"
)

label_specs() {
  cat <<'EOF'
repo:kernel|1D76DB|Tracks work scoped to kernel
repo:src-ctrl|5319E7|Tracks work scoped to src-ctrl
repo:codex-home|A371F7|Tracks work scoped to codex_home
lane:scm-pattern|0052CC|scm.pattern workflow lane
lane:metaschema|0E8A16|metaschema lane
lane:gitops-cell|FBCA04|gitops cell lane
lane:projection-workflow|C2E0C6|projection workflow lane
lane:codex-home|BFD4F2|codex_home shared control lane
lane:tooling-policy|D4C5F9|tooling policy lane
kind:epic|B60205|Epic work item
kind:tranche|D93F0B|Bounded tranche
kind:packet|FBCA04|Packet work item
kind:authority|1D76DB|Authority work item
kind:validator|0E8A16|Validator work item
kind:projection|5319E7|Projection work item
kind:controller|C5DEF5|Controller work item
kind:docs|F9D0C4|Documentation work item
kind:tooling|D4C5F9|Tooling work item
kind:policy|FEF2C0|Policy work item
kind:followup|E4E669|Followup work item
state:planned|D4C5F9|Planned state
state:in-progress|1D76DB|In progress state
state:review|FBCA04|Review state
state:blocked|B60205|Blocked state
state:done|0E8A16|Done state
gate:needs-human-review|FBCA04|Needs human review gate
gate:ready-for-realization|0E8A16|Ready for realization gate
gate:stale-basis|B60205|Approval basis is stale
EOF
}

project_field_specs() {
  cat <<'EOF'
Lane|SINGLE_SELECT|[{"name":"scm-pattern","color":"GRAY","description":"scm.pattern lane"},{"name":"metaschema","color":"BLUE","description":"metaschema lane"},{"name":"gitops-cell","color":"GREEN","description":"gitops cell lane"},{"name":"projection-workflow","color":"YELLOW","description":"projection workflow lane"},{"name":"codex-home","color":"PURPLE","description":"codex home lane"},{"name":"tooling-policy","color":"ORANGE","description":"tooling policy lane"}]
Kind|SINGLE_SELECT|[{"name":"epic","color":"RED","description":"epic work item"},{"name":"tranche","color":"ORANGE","description":"bounded tranche"},{"name":"packet","color":"YELLOW","description":"packet work item"},{"name":"authority","color":"BLUE","description":"authority work item"},{"name":"validator","color":"GREEN","description":"validator work item"},{"name":"projection","color":"PURPLE","description":"projection work item"},{"name":"controller","color":"PINK","description":"controller work item"},{"name":"docs","color":"GRAY","description":"docs work item"},{"name":"tooling","color":"GRAY","description":"tooling work item"},{"name":"policy","color":"GRAY","description":"policy work item"},{"name":"followup","color":"GRAY","description":"followup work item"}]
State|SINGLE_SELECT|[{"name":"planned","color":"GRAY","description":"planned state"},{"name":"in-progress","color":"BLUE","description":"in progress state"},{"name":"review","color":"YELLOW","description":"review state"},{"name":"blocked","color":"RED","description":"blocked state"},{"name":"done","color":"GREEN","description":"done state"}]
Gate|SINGLE_SELECT|[{"name":"none","color":"GRAY","description":"no gate"},{"name":"needs-human-review","color":"YELLOW","description":"needs human review"},{"name":"ready-for-realization","color":"GREEN","description":"ready for realization"},{"name":"stale-basis","color":"RED","description":"stale basis"}]
Evidence Ref|TEXT|
Commit Ref|TEXT|
Upstream Deps|TEXT|
EOF
}

ensure_project_scope() {
  if ! gh auth status >/dev/null 2>&1; then
    echo "gh auth is required" >&2
    exit 1
  fi
}

ensure_project() {
  local existing
  existing="$(gh project list --owner "$OWNER" --format json | jq -r --arg title "$PROJECT_TITLE" '.projects[] | select(.title == $title) | .number' | head -n1 || true)"
  if [[ -n "$PROJECT_NUMBER" ]]; then
    echo "$PROJECT_NUMBER"
    return
  fi
  if [[ -n "$existing" ]]; then
    echo "$existing"
    return
  fi
  gh project create --owner "$OWNER" --title "$PROJECT_TITLE" --format json --jq '.number'
}

project_id() {
  local number="$1"
  gh project view "$number" --owner "$OWNER" --format json --jq '.id'
}

field_exists() {
  local number="$1" name="$2"
  gh project field-list "$number" --owner "$OWNER" --format json | jq -r --arg name "$name" '.fields[] | select(.name == $name) | .id' | head -n1
}

create_field() {
  local number="$1" name="$2" data_type="$3" options_json="${4:-}"
  if [[ "$data_type" == "TEXT" ]]; then
    gh project field-create "$number" --owner "$OWNER" --name "$name" --data-type TEXT >/dev/null
  else
    local option_names
    option_names="$(jq -r '.[].name' <<<"$options_json" | paste -sd, -)"
    gh project field-create "$number" --owner "$OWNER" --name "$name" --data-type SINGLE_SELECT --single-select-options "$option_names" >/dev/null
  fi
}

sync_project_fields() {
  local number="$1" pid="$2"
  while IFS='|' read -r name data_type options_json; do
    [[ -z "$name" ]] && continue
    if [[ -z "$(field_exists "$number" "$name")" ]]; then
      create_field "$number" "$name" "$data_type" "$options_json"
    fi
  done < <(project_field_specs)
}

sync_project_links() {
  local number="$1"
  for repo in "${REPOS[@]}"; do
    gh project link "$number" --owner "$OWNER" --repo "$OWNER/$repo" >/dev/null
  done
}

sync_labels() {
  local repo="$1"
  local existing
  existing="$(gh label list --repo "$OWNER/$repo" --limit 200 --json name --jq '.[].name')"
  while IFS='|' read -r name color desc; do
    [[ -z "$name" ]] && continue
    if grep -Fxq "$name" <<<"$existing"; then
      gh label edit "$name" --repo "$OWNER/$repo" --color "$color" --description "$desc" >/dev/null
    else
      gh label create "$name" --repo "$OWNER/$repo" --color "$color" --description "$desc" >/dev/null
    fi
  done < <(label_specs)
}

sync_all_labels() {
  for repo in "${REPOS[@]}"; do
    sync_labels "$repo"
  done
}

sync_milestones() {
  local repo="$1"
  local existing
  existing="$(gh api "repos/$OWNER/$repo/milestones?state=all&per_page=100" --jq '.[].title' || true)"
  for title in "${MILESTONES[@]}"; do
    if ! grep -Fxq "$title" <<<"$existing"; then
      gh api -X POST "repos/$OWNER/$repo/milestones" -f title="$title" >/dev/null
    fi
  done
}

sync_all_milestones() {
  for repo in "${REPOS[@]}"; do
    sync_milestones "$repo"
  done
}

main() {
  ensure_project_scope
  local number pid
  number="$(ensure_project)"
  pid="$(project_id "$number")"
  sync_project_fields "$number" "$pid"
  sync_project_links "$number"
  sync_all_labels
  sync_all_milestones
  echo "project_number=$number"
  echo "project_id=$pid"
  gh project field-list "$number" --owner "$OWNER" --format json
}

main "$@"

# Adapter-backed Bashly surface for the existing bootstrap script.
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LEGACY_SCRIPT="${SCRIPT_DIR%/bootstrap_control_plane_project_bashly/src}/bootstrap_control_plane_project.sh"

if [[ ! -f "$LEGACY_SCRIPT" ]]; then
  echo "Legacy bootstrap script not found: $LEGACY_SCRIPT" >&2
  exit 1
fi

exec "$LEGACY_SCRIPT"

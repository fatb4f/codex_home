#!/usr/bin/env python3
"""Compose a per-problem generated loop workflow from registry + base loop DAG."""

from __future__ import annotations

import argparse
import copy
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def load_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise SystemExit(f"invalid json object: {path}")
    return data


def build_skill_versions(registry: dict[str, Any]) -> dict[str, str]:
    out: dict[str, str] = {}
    for item in registry.get("skills", []):
        if not isinstance(item, dict):
            continue
        skill_id = item.get("skill_id")
        if not isinstance(skill_id, str):
            continue
        version = item.get("version", "unknown")
        out[skill_id] = str(version)
    return out


def annotate_nodes(nodes: list[dict[str, Any]], versions: dict[str, str]) -> list[dict[str, Any]]:
    boundary_map = {
        "N0_initialize": "init_to_sweep_preflight",
        "N1_sweep_preflight": "sweep_preflight_to_plan",
        "N4_implement": "implement_to_sweep_postflight",
        "N5_sweep_postflight": "sweep_postflight_to_verify",
    }
    out: list[dict[str, Any]] = []
    for node in nodes:
        n = copy.deepcopy(node)
        action = str(n.get("action", ""))
        phase = str(n.get("phase", ""))
        if "run_plan_skill" in action:
            skill = "plan"
        elif "run_implement_skill" in action:
            skill = "implement"
        elif "run_sweep_skill" in action or phase.startswith("SWEEP"):
            skill = "sweep"
        else:
            skill = "loop"
        n["skill_ref"] = f"{skill}@{versions.get(skill, 'unknown')}"
        node_id = n.get("id")
        if isinstance(node_id, str) and node_id in boundary_map:
            n["boundary_contract"] = boundary_map[node_id]
        out.append(n)
    return out


def md_escape(value: Any) -> str:
    text = str(value)
    return text.replace("|", "\\|").replace("\n", "<br>")


def workflow_markdown(workflow: dict[str, Any]) -> str:
    lines: list[str] = []
    lines.append("# Generated Loop Workflow")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append(f"- `kind`: `{workflow.get('kind', '')}`")
    lines.append(f"- `generated_at_utc`: `{workflow.get('generated_at_utc', '')}`")
    lines.append(f"- `objective`: `{workflow.get('objective', '')}`")
    lines.append(f"- `wt`: `{workflow.get('wt', '')}`")
    selected = workflow.get("selected_skills", [])
    if isinstance(selected, list) and selected:
        lines.append(f"- `selected_skills`: `{', '.join(str(s) for s in selected)}`")
    lines.append("")
    lines.append("## Nodes")
    lines.append("")
    lines.append("| id | phase | action | skill_ref | next | guards |")
    lines.append("|---|---|---|---|---|---|")
    nodes = workflow.get("nodes", [])
    if isinstance(nodes, list):
        for node in nodes:
            if not isinstance(node, dict):
                continue
            next_nodes = node.get("next", [])
            guards = node.get("guards", {})
            next_text = ", ".join(str(n) for n in next_nodes) if isinstance(next_nodes, list) else ""
            guards_text = ", ".join(str(k) for k in guards.keys()) if isinstance(guards, dict) else ""
            row = [
                md_escape(node.get("id", "")),
                md_escape(node.get("phase", "")),
                md_escape(node.get("action", "")),
                md_escape(node.get("skill_ref", "")),
                md_escape(next_text),
                md_escape(guards_text),
            ]
            lines.append(f"| {' | '.join(row)} |")
    lines.append("")
    lines.append("## Sources")
    lines.append("")
    sources = workflow.get("sources", {})
    if isinstance(sources, dict):
        for key in sorted(sources):
            lines.append(f"- `{key}`: `{sources[key]}`")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--objective", required=True, help="Problem objective for this generated workflow.")
    ap.add_argument("--wt", required=True, help="Integration worktree path.")
    ap.add_argument(
        "--skills-root",
        default=".",
        help="Root skills directory containing registry and loop assets.",
    )
    ap.add_argument(
        "--registry",
        default="registry.json",
        help="Registry path relative to skills root (default: registry.json).",
    )
    ap.add_argument(
        "--loop-workflow",
        default="loop/assets/workflow.json",
        help="Base loop workflow path relative to skills root.",
    )
    ap.add_argument(
        "--handoff-contract",
        default="loop/assets/handoff.contract.json",
        help="Handoff contract path relative to skills root.",
    )
    ap.add_argument(
        "--out",
        default="",
        help="Output path. Defaults to $wt/LOOP/workflow.generated.json",
    )
    args = ap.parse_args()

    skills_root = Path(args.skills_root).expanduser().resolve()
    wt = Path(args.wt).expanduser().resolve()
    registry_path = (skills_root / args.registry).resolve()
    loop_workflow_path = (skills_root / args.loop_workflow).resolve()
    handoff_path = (skills_root / args.handoff_contract).resolve()

    if not registry_path.exists():
        raise SystemExit(f"registry not found: {registry_path}")
    if not loop_workflow_path.exists():
        raise SystemExit(f"loop workflow not found: {loop_workflow_path}")
    if not handoff_path.exists():
        raise SystemExit(f"handoff contract not found: {handoff_path}")

    registry = load_json(registry_path)
    loop_workflow = load_json(loop_workflow_path)
    handoff_contract = load_json(handoff_path)
    skill_versions = build_skill_versions(registry)

    required_skills = {"loop", "sweep", "plan", "implement"}
    missing = sorted(s for s in required_skills if s not in skill_versions)
    if missing:
        raise SystemExit(f"registry missing required skills: {', '.join(missing)}")

    generated = copy.deepcopy(loop_workflow)
    nodes = generated.get("nodes", [])
    if not isinstance(nodes, list):
        raise SystemExit("loop workflow nodes must be a list")
    generated["nodes"] = annotate_nodes(nodes, skill_versions)

    generated["kind"] = "loop.workflow.generated.v1"
    generated["generated_at_utc"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    generated["objective"] = args.objective
    generated["wt"] = str(wt)
    generated["selected_skills"] = [
        f"loop@{skill_versions['loop']}",
        f"sweep@{skill_versions['sweep']}",
        f"plan@{skill_versions['plan']}",
        f"implement@{skill_versions['implement']}",
    ]
    generated["sources"] = {
        "registry": str(registry_path),
        "loop_workflow": str(loop_workflow_path),
        "handoff_contract": str(handoff_path),
    }
    generated["boundary_contracts"] = handoff_contract.get("boundary_contracts", {})
    generated["phase_gate"] = handoff_contract.get("phase_gate", {})

    out_path = Path(args.out).expanduser().resolve() if args.out else (wt / "LOOP" / "workflow.generated.json")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(generated, indent=2) + "\n", encoding="utf-8")
    out_md_path = out_path.with_suffix(".md")
    out_md_path.write_text(workflow_markdown(generated), encoding="utf-8")
    print(out_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

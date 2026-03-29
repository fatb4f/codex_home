#!/usr/bin/env python3
"""Build a machine-readable skill registry from skills/* assets."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def parse_frontmatter(skill_md: Path) -> dict[str, Any]:
    text = skill_md.read_text(encoding="utf-8")
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}

    end = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end = i
            break
    if end is None:
        return {}

    out: dict[str, Any] = {}
    for line in lines[1:end]:
        if not line.strip() or line.startswith(" "):
            continue
        if ":" not in line:
            continue
        k, v = line.split(":", 1)
        key = k.strip()
        val = v.strip().strip('"').strip("'")
        out[key] = val
    return out


def load_json(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        return None
    return data


def md_escape(value: Any) -> str:
    text = str(value)
    return text.replace("|", "\\|").replace("\n", "<br>")


def registry_markdown(registry: dict[str, Any]) -> str:
    lines: list[str] = []
    lines.append("# Skills Registry")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append(f"- `kind`: `{registry.get('kind', '')}`")
    lines.append(f"- `generated_at_utc`: `{registry.get('generated_at_utc', '')}`")
    lines.append(f"- `skills_root`: `{registry.get('skills_root', '')}`")
    lines.append("")
    lines.append("## Skills")
    lines.append("")
    lines.append("| skill_id | version | entry_node | exit_nodes | workflow_ref | interface_ref |")
    lines.append("|---|---|---|---|---|---|")
    skills = registry.get("skills", [])
    if isinstance(skills, list):
        for skill in skills:
            if not isinstance(skill, dict):
                continue
            exit_nodes = skill.get("exit_nodes", [])
            row = [
                md_escape(skill.get("skill_id", "")),
                md_escape(skill.get("version", "")),
                md_escape(skill.get("entry_node", "")),
                md_escape(", ".join(str(n) for n in exit_nodes) if isinstance(exit_nodes, list) else ""),
                md_escape(skill.get("workflow_ref", "")),
                md_escape(skill.get("interface_ref", "")),
            ]
            lines.append(f"| {' | '.join(row)} |")
    lines.append("")
    return "\n".join(lines)


def build_registry(skills_root: Path) -> dict[str, Any]:
    skill_items: list[dict[str, Any]] = []
    for entry in sorted(skills_root.iterdir(), key=lambda p: p.name):
        if not entry.is_dir():
            continue
        if entry.name.startswith(".") or entry.name == "scripts":
            continue
        skill_md = entry / "SKILL.md"
        if not skill_md.exists():
            continue

        frontmatter = parse_frontmatter(skill_md)
        assets = entry / "assets"
        workflow = load_json(assets / "workflow.json") or {}
        interface = load_json(assets / "interface.json") or {}

        nodes = workflow.get("nodes", [])
        exit_nodes: list[str] = []
        if isinstance(nodes, list):
            for n in nodes:
                if not isinstance(n, dict):
                    continue
                has_guards = isinstance(n.get("guards"), dict) and bool(n.get("guards"))
                has_next = isinstance(n.get("next"), list) and bool(n.get("next"))
                if not has_next and not has_guards:
                    node_id = n.get("id")
                    if isinstance(node_id, str):
                        exit_nodes.append(node_id)

        skill_id = frontmatter.get("name", entry.name)
        item = {
            "skill_id": skill_id,
            "directory": entry.name,
            "skill_md": str(skill_md.relative_to(skills_root)),
            "version": frontmatter.get("version", interface.get("skill_version", "unknown")),
            "description": frontmatter.get("description", ""),
            "compatibility": frontmatter.get("compatibility", ""),
            "allowed_tools": frontmatter.get("allowed-tools", ""),
            "workflow_ref": str((assets / "workflow.json").relative_to(skills_root))
            if (assets / "workflow.json").exists()
            else "",
            "interface_ref": str((assets / "interface.json").relative_to(skills_root))
            if (assets / "interface.json").exists()
            else "",
            "entry_node": workflow.get("start", ""),
            "exit_nodes": exit_nodes,
            "inputs": interface.get("entry_requires", []),
            "outputs": interface.get("exit_produces", []),
            "capabilities": interface.get("capabilities", []),
            "side_effects": interface.get("side_effects", []),
            "mutations": interface.get("mutations", {}),
        }
        skill_items.append(item)

    return {
        "kind": "skills.registry.v1",
        "generated_at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "skills_root": str(skills_root),
        "skills": skill_items,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--skills-root",
        default=".",
        help="Root skills directory (default: current directory).",
    )
    ap.add_argument(
        "--out",
        default="registry.json",
        help="Output registry file path (default: registry.json in skills root).",
    )
    args = ap.parse_args()

    skills_root = Path(args.skills_root).expanduser().resolve()
    out_path = Path(args.out).expanduser()
    if not out_path.is_absolute():
        out_path = (skills_root / out_path).resolve()

    reg = build_registry(skills_root)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(reg, indent=2) + "\n", encoding="utf-8")
    out_md_path = out_path.with_suffix(".md")
    out_md_path.write_text(registry_markdown(reg), encoding="utf-8")
    print(out_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

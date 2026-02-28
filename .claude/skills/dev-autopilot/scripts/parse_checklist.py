#!/usr/bin/env python3
"""
parse_checklist.py - Parse DevPlan checklist files to find pending/blocked modules.

Usage:
    python3 parse_checklist.py [DevPlan/]
    python3 parse_checklist.py DevPlan/backend-api/checklist.md

Output (JSON):
    {
        "apps": [
            {
                "name": "backend-api",
                "checklist": "DevPlan/backend-api/checklist.md",
                "phases": [
                    {
                        "name": "Phase 1 - 数据库设计",
                        "modules": [
                            {"name": "01-数据模型", "status": "done", "tasks": [...]},
                            {"name": "02-认证授权", "status": "pending", "tasks": [...]}
                        ]
                    }
                ],
                "summary": {"total": 5, "done": 1, "pending": 3, "blocked": 1},
                "next_pending": "02-认证授权"
            }
        ],
        "all_done": false
    }
"""

import sys
import os
import json
import re
from pathlib import Path


def parse_checklist_file(checklist_path: str) -> dict:
    """Parse a single checklist.md file."""
    path = Path(checklist_path)
    if not path.exists():
        return {"error": f"File not found: {checklist_path}"}

    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    lines = content.splitlines()
    phases = []
    current_phase = None
    current_module = None

    for line in lines:
        # Phase header (## Phase X: ...)
        phase_match = re.match(r"^##\s+(.+)", line)
        if phase_match:
            current_module = None
            current_phase = {
                "name": phase_match.group(1).strip(),
                "modules": []
            }
            phases.append(current_phase)
            continue

        # Top-level module: "- [ ] 02-模块名" or "- [x] 02-模块名"
        module_match = re.match(r"^- \[( |x)\] (.+)", line)
        if module_match and current_phase is not None:
            done = module_match.group(1) == "x"
            name = module_match.group(2).strip()
            current_module = {
                "name": name,
                "status": "done" if done else "pending",
                "tasks": []
            }
            current_phase["modules"].append(current_module)
            continue

        # Sub-task: "  - [ ] task description"
        task_match = re.match(r"^\s+- \[( |x)\] (.+)", line)
        if task_match and current_module is not None:
            done = task_match.group(1) == "x"
            task_name = task_match.group(2).strip()
            current_module["tasks"].append({
                "name": task_name,
                "done": done
            })

    # Calculate summary
    total = sum(len(p["modules"]) for p in phases)
    done_count = sum(
        sum(1 for m in p["modules"] if m["status"] == "done")
        for p in phases
    )
    pending_modules = [
        m for p in phases for m in p["modules"] if m["status"] == "pending"
    ]

    # Find next pending module (first one in order)
    next_pending = pending_modules[0]["name"] if pending_modules else None

    return {
        "checklist": str(checklist_path),
        "phases": phases,
        "summary": {
            "total": total,
            "done": done_count,
            "pending": len(pending_modules)
        },
        "next_pending": next_pending,
        "all_done": len(pending_modules) == 0
    }


def find_checklists(devplan_dir: str) -> list:
    """Find all checklist.md files under a DevPlan directory."""
    base = Path(devplan_dir)
    if not base.exists():
        return []

    # If it's directly a checklist file
    if base.is_file() and base.name == "checklist.md":
        return [str(base)]

    # Search for checklist.md files (one level deep for app dirs)
    checklists = []
    for item in sorted(base.iterdir()):
        if item.is_dir():
            checklist = item / "checklist.md"
            if checklist.exists():
                checklists.append(str(checklist))
        elif item.name == "checklist.md":
            checklists.append(str(item))

    return checklists


def print_summary(result: dict):
    """Print a human-readable summary."""
    for app in result["apps"]:
        print(f"\n{'='*60}")
        print(f"APP: {app['name']}")
        s = app["summary"]
        print(f"Progress: {s['done']}/{s['total']} modules done, {s['pending']} pending")

        for phase in app["phases"]:
            print(f"\n  {phase['name']}:")
            for module in phase["modules"]:
                status_icon = "[DONE]   " if module["status"] == "done" else "[PENDING]"
                print(f"    {status_icon} {module['name']}")
                # Show incomplete tasks
                for task in module["tasks"]:
                    if not task["done"]:
                        print(f"             - [ ] {task['name']}")

        if app["next_pending"]:
            print(f"\n  → Next module to develop: {app['next_pending']}")
        else:
            print(f"\n  ✅ All modules complete!")

    print(f"\n{'='*60}")
    if result["all_done"]:
        print("✅ All development complete!")
    else:
        total_pending = sum(a["summary"]["pending"] for a in result["apps"])
        print(f"📋 {total_pending} module(s) remaining")


def main():
    target = sys.argv[1] if len(sys.argv) > 1 else "DevPlan/"

    checklists = find_checklists(target)
    if not checklists:
        # Try treating target as a single checklist file
        if os.path.isfile(target):
            checklists = [target]
        else:
            print(json.dumps({"error": f"No checklist.md found in: {target}"}))
            sys.exit(1)

    apps = []
    for checklist_path in checklists:
        app_name = Path(checklist_path).parent.name
        parsed = parse_checklist_file(checklist_path)
        parsed["name"] = app_name
        apps.append(parsed)

    all_done = all(a.get("all_done", True) for a in apps)
    result = {"apps": apps, "all_done": all_done}

    # JSON output (for programmatic use)
    if "--json" in sys.argv:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print_summary(result)


if __name__ == "__main__":
    main()

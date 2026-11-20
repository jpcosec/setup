#!/usr/bin/env python3
"""Initialize one live Herdr workspace for the Opsys/DeskOps repository."""

from __future__ import annotations

import argparse
import os
from pathlib import Path
import sys

OPSYS_ROOT_CANDIDATES = (
    Path.home() / "proyectos/hum-ecosystem/tools/deskops",
    Path.home() / "repos/opsys",
)


def default_opsys_root() -> Path:
    """Pick the Opsys checkout: $OPSYS_ROOT, else the first candidate that exists."""
    override = os.environ.get("OPSYS_ROOT")
    if override:
        return Path(override)
    for candidate in OPSYS_ROOT_CANDIDATES:
        if (candidate / "pyproject.toml").exists():
            return candidate
    return OPSYS_ROOT_CANDIDATES[0]


def main() -> int:
    parser = argparse.ArgumentParser(description="Create the Opsys DeskOps Herdr workspace.")
    parser.add_argument("--opsys-root", type=Path, default=default_opsys_root())
    parser.add_argument("--agents", action="store_true", help="Start executor and tester Pi agents.")
    args = parser.parse_args()
    root = args.opsys_root.expanduser().resolve()
    if not (root / "pyproject.toml").exists():
        print(f"Opsys repository not found at {root}", file=sys.stderr)
        return 1

    sys.path.insert(0, str(root))
    from deskops.config import DeskConfig
    from deskops.operations import DeskopsOperations
    from deskops.runtime.herdr import AgentSpec, ExecutionPlan, HerdrClient, HerdrProvider
    from deskops.runtime.herdr import LayoutPaneSpec, ProcessSpec

    desk_config = DeskConfig.load(root / "desk")
    if desk_config.project_identity == "unknown-project":
        print("DeskOps project_identity is not established in desk/config.json", file=sys.stderr)
        return 1
    tasks = DeskopsOperations(root).list_tasks()
    desk_id = desk_config.project_identity

    panes = [
        LayoutPaneSpec("root", process=ProcessSpec("editor", ("nvim", "."))),
        LayoutPaneSpec("navigator", parent="root", direction="right", process=ProcessSpec("navigator", ("yazi", "."))),
        LayoutPaneSpec("tests", parent="root", direction="down", process=ProcessSpec("tests", ("pytest",))),
    ]
    if args.agents:
        panes.extend([
            LayoutPaneSpec("executor", parent="root", direction="right", agent=AgentSpec("executor", kind="pi")),
            LayoutPaneSpec("tester", parent="root", direction="down", agent=AgentSpec("tester", kind="pi")),
        ])

    client = HerdrClient()
    existing = client.call("workspace", "list").get("result", {}).get("workspaces", [])
    for workspace in existing:
        if isinstance(workspace, dict) and workspace.get("label") == desk_id:
            workspace_id = workspace.get("workspace_id", "unknown")
            print(f"Herdr Space already exists: {workspace_id} ({desk_id})")
            print("Attach with: herdr")
            return 0

    handle = HerdrProvider(client).create_workspace(
        ExecutionPlan(desk_id=desk_id, cwd=root, label=desk_id, panes=tuple(panes))
    )
    print(f"DeskOps identity: {desk_id}; tasks discovered: {len(tasks)}")
    print(f"Created Herdr Space: {handle.workspace_id} ({desk_id})")
    print(f"Panes: {handle.panes}")
    if handle.agents:
        print(f"Agents: {handle.agents}")
    print("Attach with: herdr")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

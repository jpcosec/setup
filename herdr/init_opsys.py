#!/usr/bin/env python3
"""Initialize one live Herdr workspace for the Opsys/DeskOps repository."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

DEFAULT_OPSYS_ROOT = Path("/home/jp/proyectos/hum-ecosystem/tools/deskops")


def main() -> int:
    parser = argparse.ArgumentParser(description="Create the Opsys DeskOps Herdr workspace.")
    parser.add_argument("--opsys-root", type=Path, default=DEFAULT_OPSYS_ROOT)
    parser.add_argument("--agents", action="store_true", help="Start executor and tester Pi agents.")
    args = parser.parse_args()
    root = args.opsys_root.expanduser().resolve()
    if not (root / "pyproject.toml").exists():
        print(f"Opsys repository not found at {root}", file=sys.stderr)
        return 1

    sys.path.insert(0, str(root))
    from deskops.runtime.herdr import AgentSpec, ExecutionPlan, HerdrClient, HerdrProvider
    from deskops.runtime.herdr import LayoutPaneSpec, ProcessSpec

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
        if isinstance(workspace, dict) and workspace.get("label") == "opsys":
            workspace_id = workspace.get("workspace_id", "unknown")
            print(f"Herdr Space already exists: {workspace_id} (opsys)")
            print("Attach with: herdr")
            return 0

    handle = HerdrProvider(client).create_workspace(
        ExecutionPlan(desk_id="opsys", cwd=root, label="opsys", panes=tuple(panes))
    )
    print(f"Created Herdr Space: {handle.workspace_id} (opsys)")
    print(f"Panes: {handle.panes}")
    if handle.agents:
        print(f"Agents: {handle.agents}")
    print("Attach with: herdr")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

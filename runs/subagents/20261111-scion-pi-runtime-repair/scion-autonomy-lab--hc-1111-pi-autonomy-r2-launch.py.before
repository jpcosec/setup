#!/usr/bin/env python3
"""Keep one Pi conversation per Scion agent, including Docker stop/resume."""
import json
import os
from pathlib import Path
import sys


BRIDGE = Path("/usr/local/lib/scion-pi/scion-events.ts")
RECOVERY_PROMPT = ("Resume autonomous desk coordination from durable DeskOps state. "
                   "Reconcile existing Scion children before dispatch; inspect their evidence, "
                   "continue independent testing and declared closeout gates. "
                   "Do not replay the initial task or create duplicate children. "
                   "If the phase is complete or a real blocker remains, report it through sciontool.")


VALUE_FLAGS = {
    "--provider", "--model", "--tools", "-t", "--thinking", "--models",
    "--system-prompt", "--append-system-prompt", "--extension", "-e",
    "--skill", "--prompt-template", "--theme",
}
SWITCH_FLAGS = {
    "--offline", "--verbose", "--no-tools", "-nt", "--no-extensions", "-ne",
    "--no-skills", "-ns", "--no-prompt-templates", "-np", "--no-themes",
    "--no-context-files", "-nc",
}


def options_only(args):
    """Retain harness options, but never replay the initial positional task."""
    result = []
    i = 0
    while i < len(args):
        arg = args[i]
        if arg in ("--continue", "-c", "--resume", "-r"):
            i += 1
            continue
        if arg in VALUE_FLAGS:
            if i + 1 == len(args):
                raise ValueError("Missing Pi option value")
            result.extend(args[i:i + 2])
            i += 2
        elif arg in SWITCH_FLAGS:
            result.append(arg)
            i += 1
        elif arg.startswith("-"):
            raise ValueError("Unsupported Pi option on resume; inspect harness configuration")
        else:
            i += 1
    return result


def main():
    args = sys.argv[1:]
    if any(arg.split("=", 1)[0] in ("--session", "--session-dir", "--no-session", "--fork") for arg in args):
        raise ValueError("Session selection belongs to the Scion Pi launcher")
    agent_dir = Path(os.environ.get("PI_CODING_AGENT_DIR", "~/.pi/agent")).expanduser()
    session = agent_dir / "scion" / "session.jsonl"
    session.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    if session.exists():
        with session.open() as stream:
            header = json.loads(stream.readline())
        if (not isinstance(header, dict) or header.get("type") != "session"
                or not isinstance(header.get("id"), str) or not header["id"]
                or not isinstance(header.get("cwd"), str) or not Path(header["cwd"]).is_absolute()):
            raise ValueError("Invalid persisted Pi session; refusing replacement")
        if Path(header.get("cwd", "")).resolve() != Path.cwd():
            raise ValueError("Pi session workspace changed; refusing implicit migration")
        args = options_only(args)
        if os.environ.get("DESKOPS_AUTONOMOUS") == "1":
            args.append(RECOVERY_PROMPT)
    # Explicit loading avoids discovery in cheap --no-extensions review processes.
    if "--no-extensions" not in args and "-ne" not in args and BRIDGE.is_file():
        if str(BRIDGE) not in args:
            args = ["--extension", str(BRIDGE), *args]
    os.environ["PI_OFFLINE"] = "1"
    os.environ["PI_SKIP_VERSION_CHECK"] = "1"
    os.execvp("pi", ["pi", "--offline", "--session", str(session), *args])


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError):
        print("Pi launch failed: inspect session state and harness options; no arguments displayed.", file=sys.stderr)
        sys.exit(1)

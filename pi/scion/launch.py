#!/usr/bin/env python3
"""Keep one Pi conversation per Scion agent, including Docker stop/resume."""
import json
import os
from datetime import datetime, timezone
from pathlib import Path
import sys
import uuid


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


def configured_model_options(agent_dir, args):
    """Make Scion's resolved selection authoritative, including on resume."""
    model_index = next((i for i, arg in enumerate(args) if arg == "--model"), None)
    if model_index is not None:
        if model_index + 1 == len(args):
            raise ValueError("Missing Pi model")
        if any(arg == "--provider" or arg.startswith("--provider=") for arg in args):
            return args
        # Scion 0.2.21 injects its raw model alias again on resume. Pi's
        # --model is a fuzzy catalogue search, not Scion alias resolution.
        if args[model_index + 1] != os.environ.get("SCION_MODEL"):
            return args
        args = args[:model_index] + args[model_index + 2:]
    elif any(arg.startswith("--model=") for arg in args):
        return args
    if any(arg == "--provider" or arg.startswith("--provider=") for arg in args):
        raise ValueError("Pi provider requires an explicit model")
    settings = json.loads((agent_dir / "settings.json").read_text())
    if not isinstance(settings, dict):
        raise ValueError("Invalid provisioned Pi settings")
    provider, model = settings.get("defaultProvider"), settings.get("defaultModel")
    if not all(isinstance(value, str) and value.strip() for value in (provider, model)):
        raise ValueError("Pi requires a provisioned provider and model")
    return ["--provider", provider, "--model", model, *args]


FORK_DIR = Path("/workspace/.scion/fork-from")


def fork_base(session, cwd, base_dir=FORK_DIR, agent=None):
    """On first start, fork ``<base_dir>/<agent>.jsonl`` into ``session`` (DSP-1).

    Same shape as Pi's ``SessionManager.forkFrom``: a new header (new id, this cwd, ``parentSession``) and every
    non-header entry copied. Executors forked from one base share its prefix, which the provider serves from cache.
    Returns True when a fork was written."""
    agent = agent or os.environ.get("SCION_AGENT_NAME", "")
    base = base_dir / f"{agent}.jsonl"
    if session.exists() or not agent or not base.is_file():
        return False
    entries = [json.loads(line) for line in base.read_text().splitlines() if line.strip()]
    source = next((e for e in entries if isinstance(e, dict) and e.get("type") == "session"), None)
    if source is None:
        raise ValueError("Fork base has no session header")
    header = {"type": "session", "version": source.get("version", 3), "id": str(uuid.uuid4()),
              "timestamp": datetime.now(timezone.utc).isoformat(), "cwd": str(cwd), "parentSession": str(base)}
    body = [json.dumps(e) for e in entries if e is not source]
    session.write_text("\n".join([json.dumps(header), *body]) + "\n")
    session.chmod(0o600)
    return True


def main():
    args = sys.argv[1:]
    if any(arg.split("=", 1)[0] in ("--session", "--session-dir", "--no-session", "--fork") for arg in args):
        raise ValueError("Session selection belongs to the Scion Pi launcher")
    agent_dir = Path(os.environ.get("PI_CODING_AGENT_DIR", "~/.pi/agent")).expanduser()
    session = agent_dir / "scion" / "session.jsonl"
    session.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    fork_base(session, Path.cwd())
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
    args = configured_model_options(agent_dir, args)
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

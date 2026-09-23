"""One HerdrCommandDoc payload per herdr subcommand, derived from the real `herdr --help`
output (following pron's docs_sync/command_docs.py pattern).

Difference vs pron: herdr is a closed binary — there is no click group to introspect. The
deriver instead shells out to the real binary and parses `--help`, which is equally
structured:
  * `herdr --help`            -> discovers the groups
  * `herdr <group> --help`    -> discovers the subcommands of each group
  * `herdr <group> <sub> --help` -> syntax + arguments of each command

Fields the help does not provide (returns, returns_jq, example, errors, notes) are read
from the existing hand-written atoms at desk/atoms/herdr/atom-herdr-<group>-<sub>.md
(sections '## Que devuelve', '## Ejemplo real', '## Errores conocidos', '## Notas').
"""

from __future__ import annotations

import argparse
import os
import re
import subprocess
from typing import Any

import yaml

HERDR_VERSION = "0.9.0"
HERDR_BIN = "herdr"
ATOMS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "desk", "atoms", "herdr")

# Pseudo-subcommands that appear in some --help outputs but are not real commands.
PSEUDO_SUBCOMMANDS = {"https"}

# Existing-atom section headings mapped to HerdrCommandDoc fields the --help cannot give.
MD_SECTIONS = {
    "returns": "## Que devuelve",
    "example": "## Ejemplo real",
    "errors": "## Errores conocidos",
    "notes": "## Notas",
}


def _run(args: list[str]) -> str:
    """Run a herdr command and return combined output; empty string on failure."""
    try:
        proc = subprocess.run(
            [HERDR_BIN, *args],
            capture_output=True,
            text=True,
            timeout=30,
        )
        return (proc.stdout or "") + (proc.stderr or "")
    except (OSError, subprocess.TimeoutExpired):
        return ""


def _md_section(md_path: str, heading: str) -> str | None:
    """Content of one '## <heading>' section in an atom markdown file, or None."""
    if not md_path or not os.path.isfile(md_path):
        return None
    lines = open(md_path, encoding="utf-8").read().splitlines()
    out: list[str] = []
    active = False
    for line in lines:
        if line.startswith("## "):
            if active:
                break
            if line[3:].strip() == heading[3:].strip():
                active = True
            continue
        if active:
            out.append(line)
    return "\n".join(out).strip() or None


def _jq_lines(text: str | None) -> str | None:
    """The jq invocations inside a '## Que devuelve' section, as returns_jq."""
    if not text:
        return None
    lines = [ln.strip() for ln in text.splitlines() if re.search(r"\bjq\b", ln)]
    return "\n".join(lines).strip() or None


def _discover_groups() -> list[str]:
    """Groups = first token of each 'herdr <group> ...' usage line that turns out to have a
    'Commands:' list of its own."""
    top = _run(["--help"])
    candidates = sorted(
        {m.group(1) for m in re.finditer(r"^\s*herdr\s+([a-z][a-z0-9-]*)\b", top, re.M)}
    )
    groups = []
    for g in candidates:
        if re.search(r"^Commands:", _run([g, "--help"]), re.M):
            groups.append(g)
    return groups


def _discover_subcommands(group: str) -> list[str]:
    """Subcommand names from the 'Commands:' block of 'herdr <group> --help'."""
    help_text = _run([group, "--help"])
    block = help_text.split("Commands:", 1)
    if len(block) < 2:
        return []
    block = block[1].split("Are you an AI?", 1)[0]
    cmds: list[str] = []
    for line in block.splitlines():
        m = re.match(r"^\s{2}(\S+)\s+(.*\S)\s*$", line)
        if m:
            name = m.group(1)
            if name in PSEUDO_SUBCOMMANDS:
                continue
            cmds.append(name)
    return cmds


def _infer_type(signature: str, description: str) -> str:
    """Best-effort type: 'enum' when 'possible values' listed, 'numero' when the placeholder
    is a numeric unit, else 'texto'. The --help gives no explicit type, so this mapping is
    heuristic and may be wrong for unusual placeholders."""
    if "possible values" in description:
        return "enum"
    m = re.search(r"<([A-Z][A-Z0-9_]*)>", signature)
    if m and re.fullmatch(r"(?:MS|MSECS|N|SEC(?:S)?|SECONDS?|MILLIS(?:ECONDS)?|BYTES?|COUNT)", m.group(1)):
        return "numero"
    return "texto"


def _parse_arguments(help_text: str) -> str:
    """Markdown table from the 'Arguments:'/'Options:' blocks, same shape as the existing
    atoms: columns opcion | tipo | obligatorio | que hace."""
    rows: list[tuple[str, str, str, str]] = []

    def parse_block(heading: str, positional: bool):
        if heading not in help_text:
            return
        block = help_text.split(heading, 1)[1]
        # Cut the block at the next top-level section heading, whatever it is.
        block = re.split(r"^[A-Z][a-zA-Z ]+:", block, maxsplit=1, flags=re.M)[0]
        entries = [e for e in re.split(r"\n[ \t]*\n", block) if e.strip()]
        # A bracketed metadata continuation ('[possible values: ...]', '[default: ...]')
        # belongs to the previous entry. Real positionals like '[AGENT_ARG]...' do not.
        merged: list[str] = []
        for entry in entries:
            if re.match(r"^\[\s*(?:possible values|default|choices)", entry.lstrip()) and merged:
                merged[-1] += "\n" + entry
            else:
                merged.append(entry)
        entries = merged
        for entry in entries:
            lines = [ln for ln in entry.splitlines() if ln.strip()]
            if not lines:
                continue
            signature = lines[0].strip()
            description = " ".join(ln.strip() for ln in lines[1:]).strip()
            if not signature.startswith(("-", "<", "[")):
                continue
            required = "no"
            if positional:
                required = "no" if signature.startswith("[") else "si"
            rows.append((signature, _infer_type(signature, description), required, description))

    parse_block("Arguments:", positional=True)
    parse_block("Options:", positional=False)

    if not rows:
        return ""
    header = "| opcion | tipo | obligatorio | que hace |\n|---|---|---|---|"
    body = "\n".join(
        f"| {op} | {typ} | {req} | {desc} |".replace("\n", " ") for op, typ, req, desc in rows
    )
    return f"{header}\n{body}"


def _payload(group: str, sub: str) -> dict[str, Any] | None:
    help_text = _run([group, sub, "--help"])
    if not help_text.strip():
        return None

    lines = help_text.splitlines()
    synopsis = ""
    for line in lines:
        if line.strip() and not line.startswith(("Usage:", " ")):
            synopsis = line.strip()
            break

    syntax = ""
    for i, line in enumerate(lines):
        if line.startswith("Usage:"):
            syntax = line[len("Usage:"):].strip()
            break

    md_path = os.path.join(ATOMS_DIR, f"atom-herdr-{group}-{sub}.md")
    returns = _md_section(md_path, MD_SECTIONS["returns"])
    example = _md_section(md_path, MD_SECTIONS["example"])
    errors = _md_section(md_path, MD_SECTIONS["errors"])
    notes = _md_section(md_path, MD_SECTIONS["notes"])
    returns_jq = _jq_lines(returns)

    return {
        "id": f"atom-herdr-{group}-{sub}",
        "command_path": f"herdr {group} {sub}",
        "command_group": group,
        "synopsis": synopsis,
        "syntax": syntax,
        "arguments": _parse_arguments(help_text),
        "returns": returns,
        "returns_jq": returns_jq,
        "example": example,
        "errors": errors,
        "notes": notes,
        "tags": [f"system:herdr", f"layer:runtime", f"topic:{group}"],
        "provenance": f"herdr {group} {sub} --help (herdr {HERDR_VERSION})",
    }


class HerdrCommandDocs:
    """One HerdrCommandDoc payload per herdr subcommand, mirroring pron's CommandDocs
    iteration shape: discover, then one dict per command."""

    def __call__(self) -> list[dict[str, Any]]:
        payloads: list[dict[str, Any]] = []
        for group in _discover_groups():
            for sub in _discover_subcommands(group):
                payload = _payload(group, sub)
                if payload:
                    payloads.append(payload)
        return payloads


def main() -> None:
    parser = argparse.ArgumentParser(description="Derive HerdrCommandDoc payloads from real `herdr --help` output.")
    parser.add_argument("--out", required=True, help="Directory to write one YAML payload per command.")
    args = parser.parse_args()

    os.makedirs(args.out, exist_ok=True)
    payloads = HerdrCommandDocs()()
    for payload in payloads:
        with open(os.path.join(args.out, f"{payload['id']}.yaml"), "w", encoding="utf-8") as fh:
            yaml.safe_dump(payload, fh, sort_keys=False, allow_unicode=True)

    with_arguments = sum(1 for p in payloads if p["arguments"])
    with_returns_jq = sum(1 for p in payloads if p["returns_jq"])
    print(f"payloads={len(payloads)} with_arguments={with_arguments} with_returns_jq={with_returns_jq} out={args.out}")


if __name__ == "__main__":
    main()
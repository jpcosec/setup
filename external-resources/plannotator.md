---
# Human-readable name of the resource
name: Plannotator OSS
# Official docs or repository URL
page: https://docs.plannotator.ai/open-source
# true | false — whether the resource is installed locally
installed: true
# Local install path or install command; set when installed is true
install_path: ~/.local/bin/plannotator (binary); data dir ~/.plannotator/
# Namespaced tags from desk/atoms/tag-namespaces.yaml; repeated tags group related fichas
tags:
- system:plannotator
- layer:agent-hooks
- topic:plan-review
---

# Plannotator OSS

## Summary

_One paragraph: what this resource is and why it matters to this setup._

Local, open-source feedback tool for coding agents. It opens plans,
Markdown, HTML, local code changes, and PR/MR URLs in a browser
interface, collects text selections, comments, and images as
annotations, and returns the structured feedback to the agent session.
Dual-licensed MIT / Apache-2.0 (backnotprop/plannotator).

## How it's used

_How the resource is used in this setup: commands, hooks, workflows._

- Wired as a stdin hook of an agent host (Claude Code, Codex, OpenCode,
  Copilot CLI, Gemini CLI, Pi, Amp, Droid, Kiro CLI): the host pipes the
  hook event into `plannotator`, which starts a temporary local server
  bound to 127.0.0.1 and opens the review session in the browser.
- `plannotator review` opens local Git, Jujutsu, GitButler, or Perforce
  changes, or a GitHub PR / GitLab MR URL, for line-comment review.
- Sessions store plans, history, drafts, and session records under
  ~/.plannotator (plans/, history/, drafts/, sessions/).

## Status

_How it is currently working; keep empty when not installed._

Binary is present and functional. Historical usage recorded: 131 plan
reviews under ~/.plannotator/plans (e.g. unified-cli-search-run-review
2026-03-29, wikipu-remediation-plan 2026-04-07 with annotations,
approved, and denied verdicts). Most recent recorded plans date from
March-April 2026. The sibling Artifact Server product is not installed.

## Issues log

_Dated log of problems, quirks, and fixes; keep empty when not installed._

- 2026-09-13: running the binary directly (`plannotator --help`,
  `plannotator version`) fails with "Failed to parse hook event from
  stdin". Expected behavior: it is a stdin hook program, not an
  interactive CLI; it only does something when an agent host pipes a
  hook event.
- 2026-09-13: no active hook wiring found in ~/.codex/hooks.json (only
  the herdr session hook), ~/.codex/config.toml, or ~/.pi settings, so
  the tool is currently dormant despite being installed.

# Native Pi resume diagnosis

Independent read-only agent pi_resume_diagnosis traced Scion pkg/agent/run.go:919-922, launcher options_only, and pinned Pi resolveCliModel. Scion forwards --model small from its stored model alias on resume. Pi resolves that fuzzy pattern to openrouter/mistralai/voxtral-small-24b-2507, bypassing restored session/settings. The same session, correct DeepSeek registry, settings and credential environment were verified; no session corruption or lost credential.

Source fix normalizes a forwarded model equal to SCION_MODEL using the provider/model pair already resolved by provision.py; explicit provider/model pairs and differing explicit models are preserved. Invalid bindings fail before execution. Independent review found and resolved the matching explicit provider/model pair edge case, covered by regression.

Installation evidence: old r2 and r3 containers retained image79bde despite resume --image or incorrectly scoped config sync. They are preserved failed deployment attempts, not acceptance of the patch. Native --no-hub local install then Hub global sync plus project install with actual absolute project root correctly updates all3 Hub configs; hub-installed-configs.json records exact images. Final acceptance must use r4 agents and actual Docker image IDs.

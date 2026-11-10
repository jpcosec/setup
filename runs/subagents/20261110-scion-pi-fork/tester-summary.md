# Independent runtime validation

Result: PASS. 20 isolated pytest cases passed. Installer passed bash syntax validation and read-only --help.

Regression coverage: first launch forwards the original task and pins the exact agent-local session; persisted-session launch preserves provider/model/tool and context options while dropping original positional prompts and resume selection; malformed JSON, invalid headers, missing/relative/mismatched cwd and reserved session override forms are refused without replacing session contents. Dummy-only secret tests inspect base64 value, project scope, target, bearer authorization and PUT method; non-success statuses, exceptions containing dummy credentials and KeyboardInterrupt produce sanitized output.

No blocking implementation defects found in the tested paths. Tests stub exec and HTTP opener; they do not establish actual Docker/Scion stop/resume, remote API behavior, image contents or real model completion. Those require the separately scoped operational smoke evidence. Installer implementation and Dockerfile were inspected read-only; installer build was not run.

Only the authorized test file and tester evidence files were written. No real credentials, API calls, images, agents, task documents, implementation changes or commits were used.

## Follow-up acceptance

Made test source resolution portable relative to the test file. Complete setup pytest passed: 20 tests, all runtime regression cases. Rechecked installer syntax and read-only help.

Independently inspected sanitized smoke-before-stop.txt, smoke-after-resume.txt, session-before.json and session-after.json. Operational evidence accepted: initial deskops task listing and Pi 0.67.3 both exited 0; nonce CANELO-482173 was introduced only by a subsequent orchestration message, acknowledged before stop, and recalled after resume without a new tool call or replayed initial request. Both session headers retain id 01a1c3a1-1449-77e4-8e78-b43dbb40370f and cwd /workspace. The after-resume terminal transcript includes restored prior history; its newly appended interaction is the recall request and correct answer. Acceptance is based on recorded evidence, without independent agent operations.

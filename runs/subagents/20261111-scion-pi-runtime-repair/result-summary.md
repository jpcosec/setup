# Scion Pi runtime repair

Root cause: Scion forwards raw --model small on resume; Pi fuzzy resolution picks an unauthenticated OpenRouter Voxtral model. The launcher now translates Scion model arguments using the provisioned resolved provider/model, preserves explicit overrides and fails closed on incomplete bindings.

Installed native global pi and pi-autonomy configs and the laboratory project pi override point to local.scion/pi-autonomy:e9ba9e2-r2. Source remains jpcosec/pi-mono e9ba9e2, Pi0.67.3, Scion0.2.21; image contains only the launcher/bridge runtime layer over the existing image, without dependency upgrades. Explicit qualified local name prevents configured registry rewriting.

Fresh real work passes under both installed Pi configurations with no image override. Both stopped/resumed agents preserve their original session IDs and deepseek/deepseek-flash model, append an independently verified follow-up edit and pass the three original tests unchanged. Claude normal launch passes with the current host login projected using native user-scoped CLAUDE_AUTH, without harness-auth override or manual login.

Full Setup pytest:52passed6.28seconds. Independent read-only review resolved an explicit provider/model edge and found no remaining blocker. Execution-to-testing and testing-to-closeout handoffs passed the configured model, credentials, image and session continuity obligations. No bound guardrail unmet. Closeout verify declared tests/commit/atom-materialization and found all three.

Historical failures and installation attempts remain evidence, not acceptance: old images and incorrectly scoped sync did not exercise the patch. Installed configurations and actual Docker image IDs are checked separately. Existing runtime compatibility image names are migrated with rollback image IDs preserved; stopped production coordinator data is not erased or dispatched.


Final legacy migration acceptance passed with the original session id and new work, after waiting for the native Pi prompt to be ready. Actual Docker image is the normal corrected image, not the temporary diagnostic layer. Compatibility aliases include the original laboratory localhost-qualified aliases. The temporary diagnostic image was removed. Production coordinator remains stopped; no production task was started.

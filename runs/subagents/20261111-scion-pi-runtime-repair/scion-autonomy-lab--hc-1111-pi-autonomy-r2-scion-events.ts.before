/** Pi 0.67.3 native events -> Scion 0.2.21's existing Claude dialect.
 * Never forward input, tool arguments/results, transcripts or diagnostics.
 */
import { spawn } from "node:child_process";

const EVENTS = {
  session_start: "SessionStart",
  input: "UserPromptSubmit",
  agent_start: "agent-start",
  agent_end: "Stop",
  tool_execution_start: "PreToolUse",
  tool_execution_end: "PostToolUse",
};

export function payload(event) {
  const hook_event_name = EVENTS[event.type];
  if (!hook_event_name) return undefined;
  const result = { hook_event_name };
  if (event.type.startsWith("tool_execution_")) {
    // Names and ids only; bound and reject arbitrary text in these fields.
    if (typeof event.toolName === "string" && /^[\w.-]{1,80}$/.test(event.toolName))
      result.tool_name = event.toolName;
    if (typeof event.toolCallId === "string" && /^[\w:.-]{1,160}$/.test(event.toolCallId))
      result.tool_use_id = event.toolCallId;
  }
  return result;
}

export function emit(event, run = spawn) {
  const data = payload(event);
  if (!data) return Promise.resolve(true);
  return new Promise((resolve) => {
    let done = false;
    let timer;
    const finish = (ok) => { if (!done) { done = true; clearTimeout(timer); resolve(ok); } };
    try {
      const child = run("sciontool", ["hook", "--dialect=claude"],
        { stdio: ["pipe", "ignore", "ignore"] });
      timer = setTimeout(() => { child.kill("SIGKILL"); finish(false); }, 5000);
      child.on("error", () => finish(false));
      child.on("close", (code) => finish(code === 0));
      child.stdin.on("error", () => finish(false));
      child.stdin.end(JSON.stringify(data));
    } catch { finish(false); }
  });
}

export default function scionEvents(pi) {
  for (const name of Object.keys(EVENTS)) {
    pi.on(name, async (event) => {
      if (!(await emit(event))) {
        // No child errors or payloads: hook diagnostics can contain credentials.
        process.stderr.write("Scion event delivery failed.\n");
      }
    });
  }
}

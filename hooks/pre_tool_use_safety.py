"""
pre_tool_use_safety.py
----------------------
Blocks dangerous shell commands before Claude executes them.

Hook type: PreToolUse
Trigger:   Bash tool

Register in settings.json:
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [{"type": "command", "command": "python /path/to/pre_tool_use_safety.py"}]
      }
    ]
  }
"""

import json
import sys
import re

# ── Blocked patterns ──────────────────────────────────────────────────────────
# Add or remove patterns to match your team's safety requirements.
# Each entry is a (regex_pattern, human_readable_reason) tuple.

BLOCKED_PATTERNS = [
    (r"\brm\s+-rf\b",                      "rm -rf is not allowed — too destructive"),
    (r"\bgit\s+push\s+--force\b",          "force push is blocked — use --force-with-lease or ask a human"),
    (r"\bgit\s+reset\s+--hard\b",          "git reset --hard discards uncommitted work — blocked"),
    (r"\bgit\s+clean\s+-f",                "git clean -f deletes untracked files — blocked"),
    (r"\bdrop\s+table\b",                  "DROP TABLE blocked — run database destructive operations manually"),
    (r"\btruncate\s+table\b",              "TRUNCATE TABLE blocked — run database destructive operations manually"),
    (r"\bnpm\s+run\s+db:reset\b",          "db:reset is destructive — blocked"),
    (r"\bprisma\s+migrate\s+reset\b",      "prisma migrate reset is destructive — blocked"),
    (r">\s*/dev/null\s+2>&1.*&\s*$",       "background processes that suppress output are blocked"),
    (r"\bcurl\b.*\|\s*(bash|sh)\b",        "pipe to shell from curl is blocked — inspect scripts before running"),
    (r"\bwget\b.*\|\s*(bash|sh)\b",        "pipe to shell from wget is blocked — inspect scripts before running"),
    (r"\bchmod\s+777\b",                   "chmod 777 is a security risk — use more restrictive permissions"),
    (r"\bsudo\s+rm\b",                     "sudo rm is blocked — too destructive"),
]

# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError:
        # If we can't parse the input, allow and move on
        print(json.dumps({}))
        return

    tool_name = payload.get("tool_name", "")
    tool_input = payload.get("tool_input", {})

    # This hook is only meaningful for Bash commands
    if tool_name != "Bash":
        print(json.dumps({}))
        return

    command = tool_input.get("command", "")

    for pattern, reason in BLOCKED_PATTERNS:
        if re.search(pattern, command, re.IGNORECASE):
            response = {
                "decision": "block",
                "reason": f"Safety hook blocked this command: {reason}\n\nCommand was: {command}"
            }
            print(json.dumps(response))
            return

    # Command is safe — allow it
    print(json.dumps({}))


if __name__ == "__main__":
    main()

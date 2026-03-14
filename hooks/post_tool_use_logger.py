"""
post_tool_use_logger.py
-----------------------
Logs every tool use to a local file after it executes.
Useful for auditing, debugging, and understanding what Claude did in a session.

Hook type: PostToolUse
Trigger:   * (all tools)

Register in settings.json:
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "*",
        "hooks": [{"type": "command", "command": "python /path/to/post_tool_use_logger.py"}]
      }
    ]
  }

Log location: ~/claude_tool_log.jsonl (one JSON object per line)
Change LOG_FILE below to customize.
"""

import json
import sys
import os
from datetime import datetime

# ── Config ────────────────────────────────────────────────────────────────────

LOG_FILE = os.path.expanduser("~/claude_tool_log.jsonl")

# Set to True to also truncate long outputs in the log (keeps file size manageable)
TRUNCATE_OUTPUT = True
MAX_OUTPUT_LENGTH = 500  # characters

# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError:
        print(json.dumps({}))
        return

    tool_name  = payload.get("tool_name", "unknown")
    tool_input = payload.get("tool_input", {})
    tool_output = payload.get("tool_response", {})

    # Optionally truncate large outputs
    if TRUNCATE_OUTPUT:
        output_str = json.dumps(tool_output)
        if len(output_str) > MAX_OUTPUT_LENGTH:
            tool_output = {"truncated": output_str[:MAX_OUTPUT_LENGTH] + "... [truncated]"}

    log_entry = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "tool":      tool_name,
        "input":     tool_input,
        "output":    tool_output,
    }

    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps(log_entry) + "\n")
    except OSError:
        # Never crash Claude Code because of a logging failure
        pass

    # PostToolUse hooks cannot block — just return empty
    print(json.dumps({}))


if __name__ == "__main__":
    main()

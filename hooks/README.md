# Hooks

Hooks are scripts that run automatically before or after Claude uses a tool. They let you enforce guardrails, log activity, or trigger external systems — without interrupting your workflow.

## How Hooks Work

1. Claude decides to use a tool (e.g. run a bash command, edit a file)
2. Your hook script receives a JSON payload on **stdin** describing the action
3. Your script writes a JSON response to **stdout**
4. Claude Code reads the response and proceeds, modifies, or blocks the action

## Hook Types

| Type | When it runs | Can block? |
|---|---|---|
| `PreToolUse` | Before a tool executes | Yes |
| `PostToolUse` | After a tool executes | No |
| `Notification` | When Claude sends a notification | No |
| `Stop` | When Claude finishes a task | No |

## Where to Put Hooks

```
~/.claude/hooks/          # Global — runs for all projects
.claude/hooks/            # Project — runs for this project only
```

## Two Things That Will Save You Frustration

**1. Use absolute paths in settings.json**
Relative paths silently fail. Always use the full path to your hook script:
```
# Wrong — will silently not run
"command": "python hooks/pre_tool_use_safety.py"

# Right
"command": "python /Users/yourname/.claude/hooks/pre_tool_use_safety.py"
```
On Windows use forward slashes or escape backslashes:
```
"command": "python C:/Users/yourname/.claude/hooks/pre_tool_use_safety.py"
```

**2. Make your script executable (macOS/Linux)**
```bash
chmod +x ~/.claude/hooks/pre_tool_use_safety.py
```
On Windows this is not required — Python scripts run without it.

## Registering Hooks in settings.json

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "python ~/.claude/hooks/pre_tool_use_safety.py"
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "*",
        "hooks": [
          {
            "type": "command",
            "command": "python ~/.claude/hooks/post_tool_use_logger.py"
          }
        ]
      }
    ],
    "Notification": [
      {
        "matcher": "*",
        "hooks": [
          {
            "type": "command",
            "command": "python ~/.claude/hooks/notification_bell.py"
          }
        ]
      }
    ]
  }
}
```

## Pre-Tool-Use Response Format

To **allow** the action (do nothing):
```json
{}
```

To **block** the action:
```json
{
  "decision": "block",
  "reason": "Explanation shown to Claude and the user"
}
```

To **allow with a modified message** back to Claude:
```json
{
  "decision": "allow",
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "additionalContext": "Note: this file is read-only in production"
  }
}
```

## Files in This Folder

| File | What it does |
|---|---|
| `pre_tool_use_safety.py` | Blocks dangerous shell commands |
| `post_tool_use_logger.py` | Logs every tool use to a file |
| `notification_bell.py` | Plays a sound when Claude finishes |

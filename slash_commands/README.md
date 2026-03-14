# Slash Commands

Slash commands are custom `/commands` you define as Markdown files. Each file becomes a command you can type in Claude Code.

## How They Work

- Create a `.md` file in `~/.claude/commands/` (global) or `.claude/commands/` (project)
- The filename becomes the command name: `commit.md` → `/commit`
- The file content is the prompt that gets sent to Claude when you run the command
- You can reference the current git diff, selected files, or any context

## Special Variables

| Variable | What it inserts |
|---|---|
| `$ARGUMENTS` | Any text typed after the command name |
| `$CURRENT_FILE` | The file currently open in your editor |

Example: if your command file contains `Review $ARGUMENTS for security issues`, then `/review src/auth.py` sends `Review src/auth.py for security issues`.

## Files in This Folder

| Command | What it does |
|---|---|
| `/commit` | Stages changes and writes a conventional commit message |
| `/review-pr` | Reviews the current branch diff like a senior engineer |
| `/explain` | Explains selected code or a file in plain language |
| `/standup` | Summarizes recent git activity for a standup update |

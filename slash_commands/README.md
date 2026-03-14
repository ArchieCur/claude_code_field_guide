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

## Markdown Reference

Slash command files are rendered with **GitHub Flavored Markdown (GFM)**. Tables, task lists, strikethrough, alerts, and Mermaid diagrams are all supported — but not every Markdown feature works the same across platforms.

If you're writing commands that will also be used in Obsidian, GitLab, Pandoc, or other tools, check which syntax is supported where:

**[Markdown Flavors Comparison](https://github.com/ArchieCur/MARKDOWN_FLAVORS)** — a living reference comparing syntax support across 14 Markdown flavors including GFM, Obsidian, Pandoc, and more.

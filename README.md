# Claude Code Field Guide

A practitioner's reference repo — ready-to-use templates for the files that make Claude Code work in the real world.

Companion to the [Claude Code course on deeplearning.ai](https://www.deeplearning.ai).

---

## What's Here and Where It Goes

| File/Folder | Where it goes on your machine |
|---|---|
| `CLAUDE_md_templates/` | Copy chosen template to your project root as `CLAUDE.md` |
| `settings/settings.json` | `~/.claude/settings.json` (global) or `.claude/settings.json` (project) |
| `keybindings/keybindings.json` | `~/.claude/keybindings.json` |
| `hooks/` | `~/.claude/hooks/` (global) or `.claude/hooks/` (project) |
| `slash_commands/` | `~/.claude/commands/` (global) or `.claude/commands/` (project) |

> **Global vs. project:** Files in `~/.claude/` apply everywhere. Files in `.claude/` inside a project apply only to that project. Project settings override global ones.

---

## Quick Reference: Claude Code File Structure

```
~/.claude/                        # Global config (applies to all projects)
  settings.json                   # Model, permissions, env vars
  keybindings.json                # Custom keyboard shortcuts
  commands/                       # Global slash commands
    commit.md                     # Available as /commit everywhere
  hooks/                          # Global hooks
    pre_tool_use_safety.py

your-project/
  CLAUDE.md                       # Project instructions for Claude
  .claude/                        # Project-level config
    settings.json                 # Overrides global settings for this project
    commands/                     # Project-specific slash commands
    hooks/                        # Project-specific hooks
```

---

## Sections

- [CLAUDE.md Templates](CLAUDE_md_templates/) — Instructions Claude reads before every session
- [Settings](settings/) — Model selection, permissions, environment variables
- [Keybindings](keybindings/) — Custom keyboard shortcuts
- [Hooks](hooks/) — Scripts that run before/after tool use
- [Slash Commands](slash_commands/) — Custom `/commands` for repeated workflows

---

## Philosophy

Claude Code's power is mostly configuration, not code. The right `CLAUDE.md` prevents the most common mistakes. The right hooks enforce the guardrails your team needs. Slash commands turn your most-used workflows into one keystroke.

This repo is the copy-paste layer between the course and your real projects.

---

*v1.0.0 2026-03-13*  
Written by Claude Code 

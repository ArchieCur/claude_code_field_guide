# Claude Code Field Guide

A practitioner's reference repo — ready-to-use templates for the files that make Claude Code work in the real world.

Companion to the [Claude Code course on deeplearning.ai](https://www.deeplearning.ai).

---

## What's Here and Where It Goes

**Templates and Config** — copy these to your machine

| File/Folder | Where it goes on your machine |
|---|---|
| `CLAUDE_md_templates/` | Copy chosen template to your project root as `CLAUDE.md` |
| `settings/settings.json` | `~/.claude/settings.json` (global) or `.claude/settings.json` (project) |
| `keybindings/keybindings.json` | `~/.claude/keybindings.json` |
| `hooks/` | `~/.claude/hooks/` (global) or `.claude/hooks/` (project) |
| `slash_commands/` | `~/.claude/commands/` (global) or `.claude/commands/` (project) |

> **Global vs. project:** Files in `~/.claude/` apply everywhere. Files in `.claude/` inside a project apply only to that project. Project settings override global ones.

**Feature Guides** — read these, then configure Claude Code

| Folder | What it covers | Relevant path on your machine |
|---|---|---|
| `channels/` | Push external events into a running Claude Code session (Telegram, Discord, webhooks, CI) | Configured via `--channels` flag at session start |
| `dispatch/` | Delegate tasks from your phone to your desktop — and trigger Claude Code via webhooks and external events | Configured via Claude Desktop + mobile app pairing |
| `scheduled_tasks/` | Run recurring tasks on a schedule — CLI session-scoped (`/loop`) and durable Desktop tasks | CLI tasks: session memory only. Desktop tasks: `~/.claude/scheduled-tasks/` |
| `remote_control/` | Steer your local Claude Code session from your phone, tablet, or any browser | Configured via `claude --remote-control` or `/remote-control` |
| `memory/` | How Claude remembers your project — CLAUDE.md vs. auto memory, memory hygiene, subagent memory | Auto memory: `~/.claude/projects/<project>/memory/` |

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
  projects/                       # Auto memory (one directory per git repo)
    <project>/memory/
      MEMORY.md                   # Index — first 200 lines loaded every session
      *.md                        # Topic files — read on demand
  scheduled-tasks/                # Desktop scheduled tasks (Desktop app only)
    <task-name>/SKILL.md

your-project/
  CLAUDE.md                       # Project instructions for Claude
  .claude/                        # Project-level config
    settings.json                 # Overrides global settings for this project
    commands/                     # Project-specific slash commands
    hooks/                        # Project-specific hooks
```

---

## Sections

**Configuration and Templates**
- [CLAUDE.md Templates](CLAUDE_md_templates/) — Instructions Claude reads before every session
- [Settings](settings/) — Model selection, permissions, environment variables
  - [Auto Mode](settings/auto_mode.md) — Auto-approve safe commands; reduce prompts with `/fewer-permission-prompts`
  - [Effort Levels](settings/effort_levels.md) — Tune Opus 4.7's adaptive thinking with `/effort`
  - [Recaps and Focus Mode](settings/recaps_and_focus.md) — Summaries after long tasks; hide intermediate output with `/focus`
- [Keybindings](keybindings/) — Custom keyboard shortcuts
- [Hooks](hooks/) — Scripts that run before/after tool use
- [Slash Commands](slash_commands/) — Custom `/commands` for repeated workflows
  - [/go](slash_commands/go.md) — Test, simplify, and open a PR in one shot

**Feature Guides**
- [Channels](channels/) — React to external events inside a running session
- [Dispatch](dispatch/) — Delegate tasks from your phone and trigger Claude Code via webhooks
- [Scheduled Tasks](scheduled_tasks/) — Automate recurring work on a schedule
- [Remote Control](remote_control/) — Access your local session from any device
- [Memory](memory/) — How Claude remembers your project across sessions

> **Migrating from another AI coding tool?** Anthropic's [Import memory](https://claude.ai) feature on claude.ai lets you export memory from ChatGPT, Gemini, or Copilot and bring it into Claude. For Claude Code specifically, the right home for that context is your `~/.claude/CLAUDE.md` — your personal instructions file that applies across all projects. See [Memory](memory/) for how the two memory systems work.

---

## Philosophy

Claude Code's power is mostly configuration, not code. The right `CLAUDE.md` prevents the most common mistakes. The right hooks enforce the guardrails your team needs. Slash commands turn your most-used workflows into one keystroke.

The features added in v1.1.0 extend this idea further. Channels, Scheduled Tasks, Remote Control, and Auto Memory don't change what Claude Code is — they change when and where it works. Claude Code is no longer only a tool you invoke. It can watch for events, run on a schedule, stay reachable from your phone, and learn from your corrections over time.

Dispatch completes that picture. With Dispatch, you don't need to be at your desk to assign work. Send a task from your phone, walk away, and come back to results. Pair it with Channels for webhook and chat app triggers, and Claude Code becomes something closer to a background agent than a coding assistant — one you can reach from anywhere and hand off work to at any hour. The configuration layer got bigger. The principle stayed the same.

Opus 4.7 shifts the balance further toward autonomy. Auto mode replaces permission babysitting with a model-based safety classifier. Effort levels replace manual thinking-budget tuning with a single dial. Focus mode and Recaps let you step away from long tasks and return to a clean summary. The `/go` skill closes the loop: test, simplify, ship. The principle is the same as always — configuration over code — but the ceiling on what you can hand off keeps rising.

This repo is the copy-paste layer between the course and your real projects.

---

*v1.3.0 2026-04-26*
Written by Claude Code in collaboration with ArchieCur and Sonnet 4.6

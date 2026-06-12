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
| `code_review/` | Multi-agent PR analysis with severity-tagged findings + Auto-fix for live CI failures and review comments | GitHub App + admin setup at [claude.ai/admin-settings/claude-code](https://claude.ai/admin-settings/claude-code) |
| `routines/` | Cloud-based automation triggered by schedule, API call, or GitHub events — runs when your laptop is closed | Managed at [claude.ai/code/routines](https://claude.ai/code/routines) or `/schedule` in the CLI |
| `agent_teams/` | Coordinate multiple Claude Code instances with shared tasks and inter-agent messaging | Enable with `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` in settings.json |
| `managed_agents/` | Managed Agents API orientation — multi-agent sessions, outcomes, dreams, and webhooks for production deployments | Anthropic API with `managed-agents-2026-04-01` beta header |
| `enterprise/` | Large codebase and enterprise deployment patterns — harness build sequence, CLAUDE.md at scale, skills and plugins, LSP integrations, maintenance and governance | Apply patterns in your project's `.claude/` and root CLAUDE.md |
| `dynamic_workflows/` | Script-driven orchestration of dozens to hundreds of subagents — codebase audits, large migrations, cross-checked research, and repeatable orchestration patterns | `.claude/workflows/` (project) or `~/.claude/workflows/` (personal) |
| `worktrees/` | Git worktree isolation for parallel sessions — `--worktree` flag, `.worktreeinclude` for env files, subagent isolation, and cleanup | `.claude/worktrees/` under your project root |
| `Claude_Code_Desktop/` | Claude Code in the desktop app — parallel sessions, diff review, app preview, computer use, cloud and SSH sessions, Dispatch, and enterprise configuration | Desktop app settings + `.claude/launch.json` for preview servers |

---

## Run Agents in Parallel

Claude Code can parallelize work in four main ways. The right one depends on who coordinates the work, whether workers need to communicate, and whether they edit the same files.

| Approach | What it gives you | Use it when |
|:---|:---|:---|
| [Subagents](https://code.claude.com/docs/en/sub-agents.md) | Delegated workers inside one session that do a side task in their own context and return a summary | A side task would flood your main conversation with results you won't reference again |
| [Agent view](https://code.claude.com/docs/en/agent-view.md) | One screen to dispatch and monitor sessions running in the background, opened with `claude agents` | You have several independent tasks to hand off and want to check status at a glance |
| [Agent teams](agent_teams/) | Multiple coordinated sessions with a shared task list and inter-agent messaging, managed by a lead | You want Claude to split a project into pieces, assign them, and keep the workers in sync |
| [Dynamic workflows](Dynamic_Workflows) | A script that runs many subagents and cross-checks their results, for work too big to coordinate one turn at a time | A job outgrows a handful of subagents, or you want findings verified against each other: a codebase-wide audit, a 500-file migration, cross-checked research |

Two supporting tools work across all approaches:

- [Worktrees](Worktrees) give each session a separate git checkout so parallel sessions never edit the same files. Agent view moves each dispatched session into its own worktree automatically. Subagents can each get one too.
- `/batch` is a skill that has Claude split one large change into 5–30 worktree-isolated subagents that each open a pull request. It's a packaged use of subagents and worktrees, not a separate coordination style.

**Choosing an approach:**
- Who coordinates the work? Claude inside one conversation → subagents. You hand off and check back → agent view. Claude plans and supervises peers → agent teams. A script holds the plan → dynamic workflows.
- Do workers need to talk to each other? Subagents and agent view sessions report only results. Agent teammates share a task list and message each other directly. Workflow agents don't communicate — results flow through script variables.
- Do tasks touch the same files? Use [worktrees](Worktrees) to isolate. Agent teams don't auto-isolate teammates, so partition work so each teammate owns different files.

Running several sessions or subagents at once multiplies token usage. See [Costs](https://code.claude.com/docs/en/costs.md) for usage and rate-limit details.

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
  workflows/                      # Saved dynamic workflow scripts (personal)
    deep-audit.js                 # Available as /deep-audit in every project
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
    workflows/                    # Saved dynamic workflow scripts (shared with team)
    worktrees/                    # Isolated git worktrees for parallel sessions
    launch.json                   # Preview server config for Desktop app
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
- [Scheduled Tasks](scheduled_tasks/) — Automate recurring work on a schedule (local/Desktop)
- [Remote Control](remote_control/) — Access your local session from any device
- [Memory](memory/) — How Claude remembers your project across sessions
- [Code Review + Auto-fix](code_review/) — Multi-agent PR analysis and automated CI/review response
- [Routines](routines/) — Cloud-based automation on schedule, API trigger, or GitHub events
- [Agent Teams](agent_teams/) — Coordinate multiple Claude Code instances with the Advisor strategy (Opus/Sonnet/Haiku)
- [Managed Agents API](managed_agents/) — Orientation to sessions, outcomes, dreams, and webhooks for production agent deployment
- [Enterprise & Large Codebase Guide](enterprise/) — Harness build sequence, CLAUDE.md at scale, skills and plugins, LSP integrations, and governance for large teams
- [Dynamic Workflows](Dynamic_Workflows) — Script-driven orchestration of subagents at scale; `ultracode`, `/deep-research`, and saved workflow commands
- [Worktrees](Worktrees) — Git isolation for parallel sessions; `--worktree` flag, subagent isolation, and `.worktreeinclude`
- [Claude Code Desktop](Claude_Code_Desktop/) — The desktop app: parallel sessions, diff review, app preview, computer use, cloud and SSH sessions

> **Migrating from another AI coding tool?** Anthropic's [Import memory](https://claude.ai) feature on claude.ai lets you export memory from ChatGPT, Gemini, or Copilot and bring it into Claude. For Claude Code specifically, the right home for that context is your `~/.claude/CLAUDE.md` — your personal instructions file that applies across all projects. See [Memory](memory/) for how the two memory systems work.

---

## Philosophy

Claude Code's power is mostly configuration, not code. The right `CLAUDE.md` prevents the most common mistakes. The right hooks enforce the guardrails your team needs. Slash commands turn your most-used workflows into one keystroke.

The features added in v1.1.0 extend this idea further. Channels, Scheduled Tasks, Remote Control, and Auto Memory don't change what Claude Code is — they change when and where it works. Claude Code is no longer only a tool you invoke. It can watch for events, run on a schedule, stay reachable from your phone, and learn from your corrections over time.

Dispatch completes that picture. With Dispatch, you don't need to be at your desk to assign work. Send a task from your phone, walk away, and come back to results. Pair it with Channels for webhook and chat app triggers, and Claude Code becomes something closer to a background agent than a coding assistant — one you can reach from anywhere and hand off work to at any hour. The configuration layer got bigger. The principle stayed the same.

Opus 4.7 shifts the balance further toward autonomy. Auto mode replaces permission babysitting with a model-based safety classifier. Effort levels replace manual thinking-budget tuning with a single dial. Focus mode and Recaps let you step away from long tasks and return to a clean summary. The `/go` skill closes the loop: test, simplify, ship. The principle is the same as always — configuration over code — but the ceiling on what you can hand off keeps rising.

v2.0.0 extends the field guide into the GitHub loop and the cloud. Code Review and Auto-fix bring Claude into the PR lifecycle — not just writing code but analyzing it before merge and watching it after, responding to CI failures and reviewer comments autonomously. Routines push the "works when your laptop is closed" idea to its logical conclusion: fully cloud-based automation triggered by a schedule, an API call, or a GitHub event, with no local process required. Agent Teams introduce collaborative multi-agent work with the Advisor strategy — Opus at the top making judgment calls, Sonnet handling implementation, Haiku handling tools — a tiered model configuration that balances capability and cost. And the Managed Agents API section orients practitioners toward Anthropic's production-grade agent layer, where sessions, outcomes, dreams, and webhooks give you programmatic control over agents you're building into products rather than using yourself.

The ceiling keeps rising. The principle stays the same.

v2.1.0 brings the field guide to enterprise scale. The central thesis, drawn from Anthropic's Applied AI team's observations across large deployments, is that the harness matters more than the model. Two teams with identical model access but different harness configurations produce dramatically different results. The enterprise section makes this concrete: a build sequence that follows the model's own behavior (CLAUDE.md before hooks, skills before plugins, connectors last), layered CLAUDE.md hierarchies that load the right context without bloating every session, skills and plugins that turn tribal knowledge into distributed infrastructure, and LSP integrations that give Claude symbol-level navigation where text search fails at scale. At enterprise scale, configuration becomes organizational — the right harness isn't just files you write, it's a living system a team owns, reviews on a cadence, and governs deliberately. Cross-functional working groups, designated ownership, and AI code review policies aren't bureaucracy. They're the harness applied to the human layer. The ceiling keeps rising. The principle stays the same.

v2.2.0 extends Claude Code from a tool you run into an orchestrator you design. Dynamic workflows move the plan into code: instead of Claude deciding turn by turn what to spawn next, a JavaScript script holds the loop, the branching, and the intermediate results. A single run can drive hundreds of agents, resume after interruption, and apply a repeatable quality pattern — independent agents adversarially reviewing each other's findings, or drafting a plan from several angles before you commit to one. Worktrees get their own section because they're no longer a footnote to parallel sessions: they're the isolation primitive that makes every parallel approach safe, and worth understanding on their own terms. The Desktop app gets a full field guide entry because it's a different surface, not just a window on the CLI — parallel sessions with automatic worktrees, visual diff review with inline commenting, an embedded browser that verifies changes after every edit, computer use for anything without an API, and cloud sessions that keep running after you close your laptop. Across all three additions, the same principle holds: the ceiling keeps rising because the configuration space keeps growing. The orchestration itself is now configurable. Design it deliberately.

---

*v2.2.0 2026-06-12*
Written by Claude Code in collaboration with ArchieCur and Sonnet 4.6
*Enterprise section developed from Anthropic Applied AI team, "How Claude Code works in large codebases" (May 2026)*

---

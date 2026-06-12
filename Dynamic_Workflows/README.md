# Dynamic Workflows

A dynamic workflow is a JavaScript script that orchestrates subagents at scale. Claude writes the script for the task you describe; a runtime executes it in the background while your session stays responsive. Intermediate results live in script variables — not Claude's context window — so a single run can drive dozens to hundreds of agents without exhausting your session.

> Requires Claude Code v2.1.154 or later. Available on all paid plans, Anthropic API, Amazon Bedrock, Google Cloud Vertex AI, and Microsoft Foundry. On Pro, enable from the Dynamic workflows row in `/config`.

Reach for a workflow when a task needs more agents than one conversation can coordinate, or when you want the orchestration codified as a repeatable script: a codebase-wide bug sweep, a 500-file migration, cross-checked research, a plan drafted from several independent angles before you commit to one.

---

## When to use a workflow

The key difference between approaches is who holds the plan:

| | Subagents | Skills | Agent teams | Workflows |
|:---|:---|:---|:---|:---|
| **Who decides what runs next** | Claude, turn by turn | Claude, following the prompt | The lead agent, turn by turn | The script |
| **Intermediate results** | Claude's context window | Claude's context window | Shared task list | Script variables |
| **What's repeatable** | The worker definition | The instructions | The team definition | The orchestration itself |
| **Scale** | A few delegated tasks per turn | Same as subagents | A handful of long-running peers | Dozens to hundreds of agents per run |
| **Interruption** | Restarts the turn | Restarts the turn | Teammates keep running | Resumable in the same session |

A workflow also lets you apply a repeatable quality pattern: independent agents can adversarially review each other's findings before they're reported, or draft a plan from several angles and weigh them, giving you a more trustworthy result than a single pass.

**Skip workflows when:** the task fits in a handful of subagents, intermediate results need to land in Claude's context for further conversation, or you don't need the orchestration to be repeatable.

See [Run Agents in Parallel](../README.md#run-agents-in-parallel) for the full comparison across all approaches including agent view.

---

## Run a bundled workflow

The quickest way to see a workflow in action is `/deep-research`:

```text
/deep-research What changed in the Node.js permission model between v20 and v22?
```

This fans out web searches across several angles, fetches and cross-checks sources, votes on each claim, and returns a cited report with claims that didn't survive cross-checking filtered out. Requires the WebSearch tool.

Watch progress from `/workflows`, or from the task panel below the input box — a one-line summary appears there while the run is going. Press the down arrow to focus it, then Enter to expand.

---

## Before you run

Workflows can span dozens to hundreds of agents and run for a long time. Four things to check before you start:

- **Scope the task narrowly first.** Run the workflow on one directory instead of the whole repo, or a narrow question instead of a broad one. Verify it does what you want at small scale before widening the scope. A full-codebase run on a large repo can be expensive and takes time to stop once started.

- **Pre-authorize your tools.** Shell commands, web fetches, and MCP tools not in your allowlist can prompt mid-run and stall a long workflow. Before starting, add any commands the agents will need to your allowlist in `.claude/settings.json`. If you're unsure what the workflow will call, use **View raw script** at the approval prompt to check before saying yes.

- **Check your model.** Run `/model` before a large workflow if you usually switch to a smaller model for routine work. Every agent in the workflow uses your session's model unless the script routes a stage to a different one. You can also ask Claude to use a smaller model for stages that don't need the strongest one when you describe the task.

- **Plan to stay in the session.** Resume only works within the same Claude Code session. If you close the app or your machine loses power while a workflow is running, the next session starts fresh — completed agent work is not recovered. For very long runs, keep the session open and use `p` in `/workflows` to pause rather than exit.

---

## Have Claude write a workflow

### Trigger with `ultracode`

Include the keyword `ultracode` in your prompt to run a single task as a workflow without changing the session's effort level. Natural-language requests like "use a workflow" or "run a workflow" work too:

```text
ultracode: audit every API endpoint under src/routes/ for missing auth checks
```

```text
ultracode: migrate all 400 test files in tests/ from Jest to Vitest
```

Claude Code highlights the keyword in your input. If you didn't mean to start a workflow, press `Option+W` on macOS or `Alt+W` on Windows/Linux to dismiss the highlight for that prompt, or backspace while the cursor is right after the highlighted keyword. To stop the keyword from triggering at all, turn off **Ultracode keyword trigger** in `/config`.

### Set session-wide with `/effort ultracode`

`/effort ultracode` combines `xhigh` reasoning with automatic workflow orchestration for the whole session. Claude plans a workflow for every substantive task — a single request can trigger several workflows in sequence (understand the code, make the change, verify it):

```text
/effort ultracode
```

Drop back with `/effort high` when returning to routine work. Ultracode resets when you start a new session. Available only on models that support `xhigh` effort.

---

## Approve the plan before it runs

In the CLI, the per-run prompt shows the planned phases and four options:

- **Yes, run it** — start the run
- **Yes, and don't ask again for `<name>` in `<path>`** — start and skip the prompt for this workflow in this project from now on
- **View raw script** — read the generated JavaScript before deciding
- **No** — cancel

`Ctrl+G` opens the script in your editor. `Tab` lets you adjust the prompt before the run starts.

| Permission mode | When you're prompted |
|:---|:---|
| Default, accept edits | Every run, unless you've selected "don't ask again" |
| Auto | First launch only; any Yes records consent and later launches start without prompting |
| Bypass permissions, `-p`, Agent SDK | Never — runs immediately |

In the Desktop app, an approval card shows the workflow name, phase list, and a token-usage caution, with **Once**, **Always**, and **Deny** actions.

---

## Watch the run

```text
/workflows
```

Select a run and press Enter to open its progress view. The view shows each phase with agent counts, token totals, and elapsed time.

| Key | Action |
|:---|:---|
| `↑` / `↓` | Select a phase or agent |
| `Enter` or `→` | Drill into phase, then into an agent to see its prompt, tool calls, and result |
| `Esc` | Back out one level |
| `j` / `k` | Scroll within agent detail when it overflows |
| `p` | Pause or resume the run |
| `x` | Stop the selected agent, or stop the whole workflow when focus is on the run |
| `r` | Restart the selected running agent |
| `s` | Save the run's script as a reusable command |

---

## Save and reuse workflows

When a run does what you wanted, press `s` in the `/workflows` view. `Tab` toggles between two save locations:

- `.claude/workflows/` in your project — shared with everyone who clones the repo
- `~/.claude/workflows/` in your home directory — available in every project, visible only to you

Press Enter to save. The workflow runs as `/<name>` in future sessions. If a project workflow and a personal workflow share a name, the project one runs.

### Pass input to a saved workflow

Saved workflows accept input through the `args` parameter, readable as a global `args` inside the script. Claude passes structured data, so the script can call array and object methods on `args` directly:

```text
Run /triage-issues on issues 1024, 1025, and 1030
```

If `args` is omitted, the global is `undefined` inside the script.

---

## Behavior and limits

| Constraint | Why |
|:---|:---|
| No mid-run user input | Only agent permission prompts can pause a run. For sign-off between stages, run each stage as its own workflow |
| No direct filesystem or shell access from the workflow script itself | Agents read, write, and run commands; the script coordinates the agents |
| Up to 16 concurrent agents (fewer on limited hardware) | Bounds local resource use |
| 1,000 agents total per run | Prevents runaway loops |

Subagents inside a workflow always run in `acceptEdits` mode and inherit your tool allowlist, regardless of your session's permission mode. File edits are auto-approved. Shell commands, web fetches, and MCP tools not in your allowlist can still prompt mid-run — add them to your allowlist before starting a long run.

---

## Resume after a pause

If you stop a run, agents that already completed return their cached results; the rest run live. Resume from `/workflows` by selecting a paused run and pressing `p`, or ask Claude to relaunch with the same script.

Resume works within the same Claude Code session. If you exit Claude Code while a workflow is running, the next session starts the workflow fresh.

---

## Cost

A workflow spawns many agents — a single run can use meaningfully more tokens than working through the same task in conversation. Runs count toward your plan's usage and rate limits like any other session.

To gauge spend before committing to a large task:

- Run on a small slice first: one directory instead of the whole repo, or a narrow question instead of a broad one
- Check `/model` before a large run if you usually switch to a smaller model for routine work
- Ask Claude to use a smaller model for stages that don't need the strongest one
- The `/workflows` view shows per-agent token usage as the run progresses; stop at any time without losing completed work

---

## Turn workflows off

- Toggle **Dynamic workflows** off in `/config` — persists across sessions
- Set `"disableWorkflows": true` in `~/.claude/settings.json`
- Set `CLAUDE_CODE_DISABLE_WORKFLOWS=1` in your environment

For your whole organization, use the toggle on the [Claude Code admin settings](https://claude.ai/admin-settings/claude-code) page, or set `"disableWorkflows": true` in managed settings. When disabled, bundled workflow commands are unavailable, `ultracode` no longer triggers a run, and `ultracode` is removed from the `/effort` menu.

---

## Related resources

- [Dynamic workflows docs](https://code.claude.com/docs/en/workflows.md)
- [Run agents in parallel](../README.md#run-agents-in-parallel) — compare all parallel approaches
- [Workflow recipes](workflow_recipes.md) — copy-paste prompts for common scenarios
- [Subagents](https://code.claude.com/docs/en/sub-agents.md) — the worker primitive workflows orchestrate
- [Manage costs](https://code.claude.com/docs/en/costs.md)

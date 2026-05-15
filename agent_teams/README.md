# Agent Teams

> Experimental — disabled by default. Enable with `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`.
> Requires Claude Code v2.1.32 or later (`claude --version` to check).

Coordinate multiple Claude Code instances working together. One session acts as the team lead — it creates tasks, assigns work, and synthesizes results. Teammates each run in their own context window and can message each other directly.

---

## Enable agent teams

Add to `~/.claude/settings.json`:

```json
{
  "env": {
    "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"
  }
}
```

Or set in your shell environment before launching Claude Code.

---

## When to use agent teams

Agent teams shine when **parallel exploration adds real value**:

- Research and review — teammates investigate different aspects simultaneously
- New modules — teammates each own a separate piece without file conflicts
- Debugging competing hypotheses — teammates test different theories in parallel
- Cross-layer changes — frontend, backend, and tests each owned by a different teammate

**Skip agent teams when:** tasks are sequential, teammates would edit the same files, or coordination overhead outweighs the parallel benefit. A single session or subagents handle those better.

### Agent teams vs. subagents

| | Subagents | Agent teams |
|:--|:--|:--|
| **Communication** | Report results back to main agent only | Teammates message each other directly |
| **Coordination** | Main agent manages all work | Shared task list with self-coordination |
| **Best for** | Focused tasks where only the result matters | Complex work requiring discussion and collaboration |
| **Token cost** | Lower — results summarized back | Higher — each teammate is a separate Claude instance |

---

## Start a team

Tell Claude what you want in natural language:

```text
Create an agent team to review PR #142. Spawn three reviewers:
- One focused on security implications
- One checking performance impact
- One validating test coverage
Have them each review and report findings.
```

```text
I'm designing a CLI tool to track TODO comments. Create an agent team
to explore this from different angles: one teammate on UX, one on
technical architecture, one playing devil's advocate.
```

Claude creates the team, spawns teammates, and coordinates work. In the lead's terminal, all teammates and their current tasks are listed.

---

## The Advisor strategy

The most effective model configuration for agent teams follows a tiered approach:

| Role | Model | Why |
|:---|:---|:---|
| **Team lead / Advisor** | Claude Opus | Highest reasoning — coordinates, synthesizes, makes architectural calls |
| **Teammates / General work** | Claude Sonnet | Strong capability at lower cost — handles implementation |
| **Tool-heavy subtasks** | Claude Haiku | Fast and cheap — ideal for search, lookup, formatting tasks |

Configure teammates at spawn time:

```text
Create a team with 3 teammates. Use Sonnet for each teammate.
Use Opus for the lead.
```

Or set a default in `/config` → **Default teammate model**.

This pattern keeps the expensive model focused on judgment calls while Sonnet handles the bulk of implementation and Haiku handles mechanical tool use.

---

## Control your team

### Display modes

- **In-process** (default): all teammates run inside your main terminal. Use `Shift+Down` to cycle through teammates and type to message them directly.
- **Split panes**: each teammate gets its own pane. Requires tmux or iTerm2.

Set in `~/.claude/settings.json`:

```json
{
  "teammateMode": "in-process"
}
```

Or force for a single session: `claude --teammate-mode in-process`

### Talk to teammates directly

- **In-process mode:** `Shift+Down` to cycle, then type to send. Press `Enter` to view a teammate's session, `Escape` to interrupt. `Ctrl+T` toggles the task list.
- **Split-pane mode:** click into a teammate's pane to interact directly.

### Require plan approval

For risky tasks, require teammates to plan before implementing:

```text
Spawn an architect teammate to refactor the auth module.
Require plan approval before they make any changes.
```

The teammate stays in read-only plan mode until the lead approves. Rejected plans get feedback and the teammate revises and resubmits.

### Shut down and clean up

```text
Ask the researcher teammate to shut down
```

When done, always clean up through the lead:

```text
Clean up the team
```

This removes shared team resources. Clean up fails if active teammates are still running — shut them down first.

---

## Best practices

**Give teammates enough context in the spawn prompt.** Teammates load CLAUDE.md and project context but not the lead's conversation history:

```text
Spawn a security reviewer with the prompt: "Review src/auth/ for
security vulnerabilities. Focus on token handling, session management,
and input validation. The app uses JWT tokens in httpOnly cookies.
Report issues with severity ratings."
```

**Team size:** Start with 3–5 teammates. Each teammate is a separate Claude instance with its own context window — token costs scale linearly. More teammates don't always mean faster work.

**Task sizing:** Aim for 5–6 tasks per teammate. Too small = coordination overhead dominates. Too large = teammates run too long without check-ins.

**Avoid file conflicts.** Two teammates editing the same file leads to overwrites. Break work so each teammate owns a different set of files.

**Start with research.** If you're new to agent teams, begin with read-only tasks — reviewing a PR, researching a library, investigating a bug. These show the value of parallel exploration without coordination complexity.

**Watch for the lead doing work itself.** If the lead starts implementing instead of delegating:

```text
Wait for your teammates to complete their tasks before proceeding.
```

---

## Enforce quality gates with hooks

| Hook | When it runs | Exit code 2 effect |
|:---|:---|:---|
| `TeammateIdle` | Teammate is about to go idle | Sends feedback, keeps teammate working |
| `TaskCreated` | A task is being created | Prevents creation, sends feedback |
| `TaskCompleted` | A task is being marked complete | Prevents completion, sends feedback |

---

## Known limitations

- `/resume` and `/rewind` don't restore in-process teammates
- Teammates sometimes fail to mark tasks completed — check manually if a task appears stuck
- Maximum 25 concurrent threads per session
- No nested teams — teammates can't spawn their own teams
- Split-pane mode doesn't work in VS Code integrated terminal, Windows Terminal, or Ghostty

---

## Related resources

- [Agent teams docs](https://code.claude.com/docs/en/agent-teams.md)
- [Subagents](https://code.claude.com/docs/en/sub-agents.md) — lighter-weight delegation within a single session
- [Worktrees](https://code.claude.com/docs/en/worktrees.md) — manual parallel sessions without automated coordination
- [Agent view](https://code.claude.com/docs/en/agent-view.md) — monitor background agents from one place

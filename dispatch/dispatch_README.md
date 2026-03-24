# Dispatch

Dispatch is Claude's mobile-to-desktop task delegation system. You assign work from your phone, Claude does it on your desktop, and you come back to completed tasks.

It's built into Claude Desktop and the Claude mobile app — not a separate Claude Code feature. Under the hood, it creates a single persistent conversation thread between your devices. Development tasks get routed to Claude Code on your machine; document and knowledge tasks go to Cowork.

---

## The ecosystem: Dispatch vs. the alternatives

Dispatch is one of four ways to trigger Claude Code remotely. Before using it, make sure it's the right tool.

| | **Dispatch** | **Remote Control** | **Channels** | **Scheduled Tasks** |
|---|---|---|---|---|
| **Trigger from** | Claude mobile app | claude.ai or mobile | Telegram, Discord, webhooks | Time-based schedule |
| **Best for** | Delegating work while away | Steering in-progress work | Reacting to external events | Recurring, unattended automation |
| **Claude runs on** | Your desktop | Your machine (CLI/VS Code) | Your machine (CLI) | Cloud or your machine |
| **Desktop must be on** | Yes | Yes | Yes | Only for Desktop Tasks |
| **Parallel tasks** | No | Multiple sessions (server mode) | Per-session | Yes |
| **Setup time** | ~2 minutes (QR code) | One command | Plugin install + auth | Minimal |

**Choose Dispatch when:**
- You want to assign work from your phone and walk away
- You don't need to monitor progress in real time
- The task is self-contained enough to describe in a message
- You're already using Claude Desktop

**Choose Remote Control instead when:**
- You want to actively steer a session from another device
- The task is ambiguous and you may need to intervene

**Choose Channels instead when:**
- You need a webhook or CI/CD trigger
- You want push notifications when something happens
- You're integrating with Telegram or Discord

**Choose Scheduled Tasks instead when:**
- The work is time-based, not event-based
- You need tasks to survive machine restarts

---

## How Dispatch works

```
Phone (Claude mobile app)
  → Send task via Dispatch thread
  → Claude routes task type
  → Development task → Claude Code on your desktop
  → Knowledge task → Cowork (web-based)
  → Claude does the work
  → You return to desktop to review results
```

The conversation thread is persistent. Context carries over from message to message — you don't re-explain your project every time.

---

## Setup

Dispatch requires a Pro or Max subscription and both Claude Desktop and the Claude mobile app.

1. Open Claude Desktop
2. Open the Claude mobile app
3. In the mobile app, tap **New Conversation → Dispatch**
4. Scan the QR code shown on your desktop
5. Done — you now have a persistent Dispatch thread

Total setup time: about 2 minutes.

**Dispatch uses your claude.ai subscription OAuth — not your API key.** If you're used to setting `ANTHROPIC_API_KEY` for Claude Code sessions, this is different. API key auth will not work with Dispatch.

---

## Giving Dispatch good tasks

Dispatch succeeds or fails based on task clarity. Claude cannot ask follow-up questions while you're away.

**Works well:**
- "Write unit tests for the `auth` module and commit them"
- "Refactor `UserCard.tsx` to use the new design tokens — reference `design-system.md` for the token names"
- "Run the test suite and summarize any failures"

**Fails often:**
- Multi-step tasks with ambiguous requirements
- Tasks that assume files or context you haven't mentioned
- Anything where Claude would normally ask a clarifying question

When Dispatch fails, Claude usually explains what went wrong. That explanation is your starting point for a better-worded retry.

---

## Key limitations

**Desktop must stay on.** If your machine sleeps, closes, or loses network, Dispatch tasks fail. Disable sleep when you're expecting work to run.

**Single-threaded.** One task at a time. A second message waits for the first to finish. No parallel execution, no batching.

**No completion notifications.** Claude won't push an alert when the task finishes. You check back on your desktop.

**Unattended permission prompts block.** If Claude hits a permission prompt mid-task, the session pauses and waits. For unattended use in trusted environments, use `--dangerously-skip-permissions` when starting Claude Code — but understand what you're allowing before you do.

---

## Related

- [dispatch_channels_webhooks.md](dispatch_channels_webhooks.md) — Triggering Claude Code via webhooks, Telegram, Discord, and custom events
- [remote_control/remote_control_README.md](../remote_control/remote_control_README.md) — Controlling a live session from another device
- [scheduled_tasks/scheduled_tasks_README.md](../scheduled_tasks/scheduled_tasks_README.md) — Time-based automation

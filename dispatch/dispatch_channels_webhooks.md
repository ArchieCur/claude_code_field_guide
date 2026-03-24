# Channels & Webhooks

If you want to trigger Claude Code from an external system — a CI/CD pipeline, a webhook, Telegram, Discord — that's **Channels**, not Dispatch. The two are often confused because they both involve "triggering Claude remotely," but they work differently.

**Dispatch**: You send a task from your phone. One persistent thread. Human-initiated.
**Channels**: External events push into a running Claude Code session. Programmatic. Event-driven.

---

## What Channels are

Channels are MCP servers that push events into an active Claude Code session. When an event arrives, Claude sees it and can respond — running code, editing files, sending replies.

Think of it as giving Claude a message inbox that external systems can write to.

**Supported channels:**
- **Telegram** — via `plugin:telegram@claude-plugins-official`
- **Discord** — via `plugin:discord@claude-plugins-official`
- **Fakechat** — localhost demo for testing (no credentials needed)
- **Custom webhooks** — build your own MCP channel server

Channels are a research preview feature as of early 2026. Syntax and behavior may change.

---

## Requirements

- Claude Code v2.1.80 or later
- **Authentication via claude.ai** — not API keys. Console and API key auth are not supported.
- Team or Enterprise plans require an admin to enable Channels via the `channelsEnabled` setting first.

---

## Setup: Telegram

```bash
# Install the plugin
/plugin install telegram@claude-plugins-official

# Configure with your Telegram bot token
/telegram:configure <bot-token>

# Add yourself as an approved sender
/telegram:access pair <pairing-code>

# Set to allowlist mode (only approved senders can trigger Claude)
/telegram:access policy allowlist

# Start Claude Code with Channels enabled
claude --channels plugin:telegram@claude-plugins-official
```

---

## Setup: Discord

```bash
# Install the plugin
/plugin install discord@claude-plugins-official

# Configure with your Discord bot token
/discord:configure <bot-token>

# Add an approved sender
/discord:access pair <pairing-code>

# Lock down to allowlist
/discord:access policy allowlist

# Start with Channels enabled
claude --channels plugin:discord@claude-plugins-official
```

---

## Setup: Custom webhooks

For CI/CD pipelines and other HTTP-based triggers, build an MCP channel server that accepts the incoming event and forwards it to Claude Code. Third-party tools like Hookdeck CLI can bridge external webhooks to a local channel server.

The general pattern:
1. External service fires webhook to your endpoint
2. Your MCP channel server receives it and formats the event
3. Claude Code session receives the event via the channel
4. Claude acts on it

---

## Running multiple channels

Pass multiple `--channels` flags to run more than one at a time:

```bash
claude --channels plugin:telegram@claude-plugins-official \
       --channels plugin:discord@claude-plugins-official
```

---

## Gotchas and common mistakes

### 1. Channels die when the session dies

Claude Code must be running for events to be received. Close the terminal, lose the session — events that arrive while it's down are dropped. There's no queuing.

For always-on event handling, you need a background process keeping the session alive. A common pattern is running `claude --channels ...` inside a `tmux` or `screen` session on a server or always-on machine.

### 2. Authentication is claude.ai OAuth, not API keys

This catches almost everyone coming from standard Claude Code usage. If your workflow authenticates via `ANTHROPIC_API_KEY`, that won't work for Channels. You need to log in via `claude login` and use your claude.ai subscription credentials.

### 3. Not locking down your allowlist

The default policy allows any sender to push events into your session. This is a meaningful security risk — anyone who can message your bot can execute prompts on your machine. Always set the access policy to `allowlist` and pair only trusted senders before exposing a channel to the internet.

### 4. Confusing "allowlist" with authentication

Gating by sender identity protects against unauthorized users, but the channel itself is the trust boundary — not the chat platform. A compromised Telegram account in your allowlist can trigger Claude. Treat channel access the same way you'd treat SSH access.

### 5. Third-party plugins require an explicit flag

Only Anthropic-maintained plugins load with the standard `--channels` flag. Loading any other plugin requires:

```bash
--dangerously-load-development-channels
```

The flag name is intentional. Understand what a plugin can do before you load it.

### 6. Research preview means it can break

Channel plugin IDs, `--channels` syntax, and access control APIs are all subject to change. Pin your setup notes with the Claude Code version you tested on, and re-verify after updates. Use `/doctor` to diagnose issues after an upgrade.

### 7. Permission relay confusion

Some channel plugins support forwarding permission prompts back to the remote sender. This sounds convenient but changes your security model significantly — the remote user now has permission to approve actions on your local machine. Only enable permission relay if you fully trust the sender and understand the implications.

### 8. Fakechat is localhost only

The Fakechat channel is useful for testing your setup without external credentials, but it only works on `localhost`. Don't mistake a successful Fakechat test for proof that your production Telegram or webhook setup will work.

---

## Channels vs. Scheduled Tasks for event-driven work

A common question: should I use Channels or Scheduled Tasks for recurring work?

Use **Channels** when: an external system signals that something happened (CI failed, a user messaged you, a webhook fired). Claude reacts to the event.

Use **Scheduled Tasks** when: work should run on a fixed schedule regardless of external events (nightly test run, morning PR summary). Claude initiates based on time.

They're not mutually exclusive. A pattern that works well: a Telegram channel for ad hoc requests, scheduled tasks for regular recurring work.

---

## Related

- [dispatch_README.md](dispatch_README.md) — Mobile-to-desktop task delegation
- [remote_control/remote_control_README.md](../remote_control/remote_control_README.md) — Controlling a live session from another device
- [scheduled_tasks/scheduled_tasks_README.md](../scheduled_tasks/scheduled_tasks_README.md) — Time-based automation

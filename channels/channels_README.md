# Channels

Channels let external systems push events into your running Claude Code session. Instead of waiting at your terminal, Claude reacts to messages and events that arrive while you're away — from Telegram, Discord, webhooks, CI pipelines, or any custom source.

> **Status:** Research preview. Requires Claude Code v2.1.80+ and a claude.ai login (not Console API keys).

---

## What Problem Does This Solve?

Without Channels, Claude Code is fully reactive — it only responds when you type. Channels flip this: external systems can push events **into** your open session, where Claude already has your codebase, memory, and context loaded.

**Before Channels:**
- You had to manually check CI failures, alerts, or messages
- Each new Claude session started fresh with no context
- Automation required polling or external orchestration

**With Channels:**
- A failed CI run arrives in your session → Claude reads the logs and suggests a fix
- A teammate DMs your Claude bot on Telegram → Claude answers with full codebase awareness
- A monitoring alert fires → Claude diagnoses it against your current code

---

## How Channels Work

Channels are MCP servers that act as event bridges:

1. You install or configure a channel (Telegram, Discord, webhook, etc.)
2. You start Claude Code with `--channels` to enable it
3. An external event arrives → the channel server receives it → pushes it to your session via `notifications/claude/channel`
4. Claude processes the event (optionally replying via a reply tool)

**Two modes:**
- **One-way**: Claude receives alerts, CI events, monitoring data — no reply
- **Two-way**: Claude receives a message AND sends a reply back to the source (e.g., Telegram bot that answers questions)

---

## Quick Start: Telegram Channel

```bash
# 1. Install the official Telegram plugin
/plugin install telegram@claude-plugins-official
/reload-plugins

# 2. Configure with your bot token (get one from @BotFather on Telegram)
/telegram:configure <your-bot-token>

# 3. Start Claude with the channel enabled
claude --channels plugin:telegram@claude-plugins-official

# 4. DM your bot in Telegram — Claude will ask you to pair
/telegram:access pair <code-from-telegram>
/telegram:access policy allowlist
```

Now you can DM your bot on Telegram and Claude will reply with full codebase context.

---

## Quick Start: Discord Channel

```bash
# 1. Install the official Discord plugin
/plugin install discord@claude-plugins-official
/reload-plugins

# 2. Configure with your bot token (from Discord Developer Portal)
/discord:configure <your-bot-token>

# 3. Start Claude with the channel enabled
claude --channels plugin:discord@claude-plugins-official

# 4. DM your bot in Discord — Claude will ask you to pair
/discord:access pair <code-from-discord>
/discord:access policy allowlist
```

---

## Quick Start: Multiple Channels

```bash
# Enable both Telegram and Discord simultaneously
claude --channels plugin:telegram@claude-plugins-official plugin:discord@claude-plugins-official
```

---

## Testing Without a Real Account: Fakechat

Anthropic provides a localhost demo channel with no authentication required:

```bash
# Great for testing your channel setup locally
claude --channels plugin:fakechat@claude-plugins-official
```

---

## Custom Channels (Webhooks, CI, Monitoring)

For custom integrations, define a channel as an MCP server in `.mcp.json`:

```json
{
  "mcpServers": {
    "webhook": {
      "command": "bun",
      "args": ["./webhook-channel.ts"]
    }
  }
}
```

Then start Claude with:

```bash
# --dangerously-load-development-channels is required during research preview
# for channels not on Anthropic's approved allowlist
claude --dangerously-load-development-channels server:webhook
```

### Building a Custom Channel (TypeScript)

A minimal custom channel MCP server needs three things:

**1. Declare the channel capability:**
```typescript
capabilities: {
  experimental: { 'claude/channel': {} }
}
```

**2. Add instructions to Claude's system prompt:**
```typescript
instructions: 'Messages arrive as <channel source="webhook">. Reply with the reply tool.'
```

**3. Push events via the notification API:**
```typescript
await mcp.notification({
  method: 'notifications/claude/channel',
  params: {
    content: 'Deploy to staging failed — exit code 1 on step "run tests"',
    meta: { severity: 'high', run_id: 'ci-4521' }  // optional metadata
  },
})
```

**What Claude receives in context:**
```xml
<channel source="webhook" severity="high" run_id="ci-4521">
Deploy to staging failed — exit code 1 on step "run tests"
</channel>
```

**4. (Optional) Register a reply tool** for two-way channels using standard MCP tool registration.

---

## Security: What You MUST Know

### Sender Allowlisting
Channels maintain an allowlist of approved senders. Only paired/approved senders can push events to your session. The pairing flow (send a message → Claude returns a code → you approve) bootstraps this list.

### Gate on Sender Identity, Not Room/Channel
In group chats (Discord servers, Telegram groups), any member could send messages. Gate permissions on **sender identity**, not the room/channel, to prevent prompt injection.

```bash
# Right approach: allowlist specific user IDs
/telegram:access policy allowlist  # only paired users get through

# Wrong approach: trusting all messages from a group chat
# Anyone in the group could inject malicious instructions
```

### The `--channels` Flag Is Required
Simply listing a server in `.mcp.json` does NOT enable it as a channel. It must also be named in `--channels`. This is intentional — channels can push into your session, so opt-in per session is enforced.

### What NOT to Do
- Do NOT enable channels in a session with access to production credentials without careful sender controls
- Do NOT use a group chat as a channel input without sender allowlisting
- Do NOT ignore the `--dangerously-load-development-channels` warning — it exists because unreviewed channels can push arbitrary content to your session
- Do NOT share your bot token — it grants full channel access

---

## Enterprise Controls

| Plan | Channels Default |
|------|-----------------|
| Pro/Max (personal) | Available; opt-in per session with `--channels` |
| Team / Enterprise | Disabled by default; admin must enable |

**For admins:** Enable via `claude.ai → Admin settings → Claude Code → Channels` or set `channelsEnabled: true` in managed settings.

---

## Channels vs. Other Claude Code Features

| Feature | What It Does |
|---------|-------------|
| **Channels** | Push events *into* your running session; Claude reacts while you're away |
| **Remote Control** | Drive your local session from your phone/browser |
| **Web sessions** | Delegate async tasks to cloud; check back later |
| **Slack integration** | Start Claude tasks from a Slack conversation |
| **Standard MCP** | Claude queries the server on-demand; nothing is pushed |

---

## Available Channels (Research Preview)

| Channel | Install Command |
|---------|----------------|
| Telegram | `/plugin install telegram@claude-plugins-official` |
| Discord | `/plugin install discord@claude-plugins-official` |
| Fakechat (local demo) | `/plugin install fakechat@claude-plugins-official` |

Community and official channel implementations: [github.com/anthropics/claude-plugins-official](https://github.com/anthropics/claude-plugins-official)

---

## Official Docs

- [Channels Overview](https://code.claude.com/docs/en/channels)
- [Building Custom Channels](https://code.claude.com/docs/en/channels-reference)

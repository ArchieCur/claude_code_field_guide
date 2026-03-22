# Remote Control

Remote Control connects claude.ai or the Claude mobile app to a Claude Code session running on your local machine. You can steer your local session from your phone, tablet, or any browser — while all code execution, file access, and MCP servers stay on your machine. Nothing moves to the cloud.

> **Minimum version:** Claude Code v2.1.51+ | **Requires:** claude.ai OAuth login (not API keys)

---

## What Problem Does This Solve?

You're deep into a debugging session at your desk. You need to step away — couch, commute, meeting — but don't want to lose the thread. Remote Control lets you pick up exactly where you left off from your phone, without losing your local environment.

**What stays local:**
- Your filesystem and all file access
- Local MCP servers and tools
- Project configuration and memory
- All code execution

**What Remote Control adds:**
- A window into that session from any device
- Messages sync in real time across terminal, browser, and phone simultaneously
- Automatic reconnection if your network drops or laptop sleeps briefly

---

## Security Model

Remote Control is **outbound-only**. Your machine never opens an inbound port.

Here's the exact flow:
1. When you start Remote Control, your local Claude Code process makes outbound HTTPS requests to the Anthropic API and begins polling for work
2. When you connect from another device, the Anthropic server routes messages between the web/mobile client and your local session over a streaming connection
3. All traffic travels over TLS — the same transport as any Claude Code API call
4. The connection uses multiple short-lived credentials, each scoped to a single purpose and expiring independently. This limits the blast radius if any single credential were compromised

**What NOT to assume:**
- Your code is not stored in Anthropic's cloud infrastructure during a Remote Control session
- Remote Control is not the same as running Claude Code on the web — there's no cloud VM executing your code
- Data is encrypted in transit but **not encrypted at rest** in your local session (same as any local Claude Code session)

---

## Authentication Requirements

Remote Control requires **claude.ai OAuth** — not an API key.

**Supported plans:** Pro, Max, Team (admin must enable), Enterprise (admin must enable)
**Not supported:** Free plan, API keys, Bedrock, Vertex AI, Foundry credentials

If you have `ANTHROPIC_API_KEY` set in your environment, it will override your OAuth login and break Remote Control. Unset it:

```bash
unset ANTHROPIC_API_KEY
```

Also check `~/.zshrc`, `~/.bashrc`, or `~/.profile` and remove any `export ANTHROPIC_API_KEY=...` lines, then run `/login` inside Claude Code.

---

## Three Ways to Start Remote Control

### Method 1: Interactive Session with Remote Control Enabled

Start a normal Claude Code session that also accepts remote connections:

```bash
claude --remote-control

claude --remote-control "My Project Name"
```

You work in the terminal as normal. Any device that connects sees the same conversation.

### Method 2: Enable Remote Control on an Existing Session

From within an already-running session:

```bash
/remote-control

/remote-control My Project Name
```

Carries over your existing conversation history. Displays a session URL and QR code immediately.

> **Note:** `--verbose`, `--sandbox`, and `--no-sandbox` flags are not available with this command.

### Method 3: Server Mode (Dedicated Remote Control Process)

```bash
claude remote-control
```

Runs as a headless server with no interactive terminal. Designed for concurrent sessions, worktrees, and dedicated remote workflows. See [Server Mode](server_mode.md) for the full guide.

### Enable Remote Control for All Sessions Automatically

Run `/config` inside Claude Code and set **Enable Remote Control for all sessions** to `true`. Every new interactive Claude Code session will register itself as a remote session automatically.

---

## Connecting From Another Device

Once Remote Control is active, you have three options:

**1. Open the session URL directly**
A URL is displayed in the terminal. Open it in any browser to go directly to your session on claude.ai/code.

**2. Scan the QR code**
In server mode (`claude remote-control`), press **spacebar** to toggle QR code display. Scan it with the Claude mobile app to connect directly.

**3. Find the session by name**
Open [claude.ai/code](https://claude.ai/code) or the Claude mobile app. Remote Control sessions appear in the session list with a computer icon and a green status dot when online.

### Getting the Mobile App

Run `/mobile` inside Claude Code to display a QR code linking to:
- **iOS:** App Store — Claude by Anthropic
- **Android:** Google Play — Claude by Anthropic

---

## Session Title

Your session's display name is determined in this order:
1. Name passed to `--remote-control`, `/remote-control`, or `--name`
2. Title set with `/rename`
3. Last meaningful message in existing conversation history
4. Your first prompt after connecting

---

## What You Can and Cannot Do Remotely

**You can:**
- Read files, edit code, run commands (subject to existing permission rules)
- Work with git, create commits, open pull requests
- Use all local MCP servers and tools
- Send messages from terminal, browser, and phone interchangeably — they all stay in sync
- Have Claude ask you clarifying questions mid-task that you answer from your phone

**You cannot:**
- Run interactive bash commands that require stdin (e.g., an editor that opens in the terminal, interactive `npm` prompts)
- Access code that isn't cloned locally — Remote Control is a window into your machine, not a cloud environment
- Run multiple simultaneous Remote Control sessions per interactive process (use [Server Mode](server_mode.md) for concurrent sessions)

---

## Remote Control vs. Channels vs. Web Sessions

These three features are frequently confused. They solve different problems.

| | Remote Control | Channels | Web Sessions (claude.ai) |
|--|---------------|----------|--------------------------|
| **You drive it from** | Phone / browser | External system pushes events in | claude.ai web interface |
| **Code runs on** | Your machine | Your machine | Anthropic cloud VM |
| **Access your local env** | Yes — full access | Yes — full access | No |
| **Works on code not cloned locally** | No | No | Yes (clones from GitHub) |
| **Best for** | Continuing local work from another device | Reacting to CI alerts, chat events, webhooks | Long-running background tasks without local setup |
| **Requires terminal open** | Yes | Yes | No |

**The one-sentence version:**
- **Remote Control:** You steer your local session from somewhere else
- **Channels:** External events push into your running local session
- **Web sessions:** You hand off a task to a cloud VM entirely

---

## Known Limitations and Rough Edges

These are real constraints to design around, not bugs that will be fixed soon:

**1. Terminal must stay open**
Remote Control runs as a local process. If you close your terminal or stop the `claude` process, the session ends. There is no background daemon — your terminal is the server.

**2. Extended network outage timeout**
If your machine is awake but cannot reach the network for roughly 10 minutes, the session times out and the process exits. Reconnection requires restarting.

**3. No interactive stdin**
Commands requiring keyboard input in the terminal (editors, interactive installers, password prompts) cannot be driven from the remote interface.

**4. Computer must stay awake**
If your laptop sleeps, the Remote Control connection drops. It reconnects when the machine wakes, but tasks running at sleep time are interrupted.

**5. One session per interactive process**
In interactive mode, each `claude` process supports one Remote Control session. For concurrent sessions, use [Server Mode](server_mode.md) with `--spawn worktree`.

---

## Troubleshooting

**90% of Remote Control failures are caused by:**
(1) API key overriding OAuth, or 
(2) plan/admin restrictions.
Check these first.

### "Remote Control is not yet enabled for your account"

One of these environment variables is interfering:

```bash
unset CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC
unset DISABLE_TELEMETRY
unset CLAUDE_CODE_USE_BEDROCK
unset CLAUDE_CODE_USE_VERTEX
unset CLAUDE_CODE_USE_FOUNDRY
```

If that doesn't fix it, refresh your credentials:

```bash
/logout
/login
```

### "Remote Control is disabled by your organization's policy"

Three possible causes:

1. **You're authenticated with an API key, not OAuth** — run `/login` to switch to claude.ai OAuth
2. **Your Team/Enterprise admin hasn't enabled it** — they need to toggle it on at [claude.ai/admin-settings/claude-code](https://claude.ai/admin-settings/claude-code)
3. **The admin toggle is grayed out** — your org has a data retention or compliance configuration incompatible with Remote Control. Contact Anthropic support.

### "Remote credentials fetch failed"

Check in order:
1. Are you signed in? Run `/login`
2. Is port 443 outbound to `api.anthropic.com` open? (Corporate firewalls and proxies sometimes block this)
3. Is your subscription active? Verify at claude.ai

---

## Enterprise and Team Controls

Remote Control is **off by default** for Team and Enterprise plans. An admin must enable it.

**Admin steps:**
1. Go to [claude.ai/admin-settings/claude-code](https://claude.ai/admin-settings/claude-code)
2. Toggle Remote Control on
3. Users in the org can now use all Remote Control commands

If the toggle is grayed out, your org's data retention or compliance settings conflict with Remote Control. This cannot be resolved from the admin panel — contact Anthropic support.

**Pro and Max users:** Remote Control is available by default, no admin action needed.

---

## What NOT to Do

- **Don't use Remote Control expecting to run interactive terminal commands remotely.** If a command needs stdin — editor, password prompt, interactive installer — it won't work from the remote interface.
- **Don't close your terminal and expect the session to keep running.** Close the terminal = end the session. There is no background process.
- **Don't set `ANTHROPIC_API_KEY` and wonder why Remote Control won't authenticate.** API keys override OAuth and Remote Control requires OAuth.
- **Don't use Remote Control as a substitute for web sessions when you need to work on code not cloned locally.** Remote Control is a window into your machine, not a cloud environment.
- **Don't ignore the 10-minute network timeout.** If you're on a flaky connection, design your prompts so Claude can complete meaningful work in chunks, not one long uninterrupted task.

---

## Official Docs

- [Remote Control Overview](https://code.claude.com/docs/en/remote-control)

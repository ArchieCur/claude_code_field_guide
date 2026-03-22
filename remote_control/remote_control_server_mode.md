# Remote Control: Server Mode

Server mode runs a dedicated, headless Remote Control process — no interactive terminal, no manual session management. It's designed for when you want persistent remote access with concurrent sessions or Git worktree isolation.

If you just want to add remote access to a session you're already in, see the [main Remote Control guide](README.md).

---

## When to Use Server Mode

**Use server mode when:**
- You want a persistent remote entry point that's always ready (not tied to an active terminal session)
- You need multiple people to connect to the same Claude Code session simultaneously
- You want each remote session to get its own isolated Git worktree
- You're running Claude Code on a remote machine (e.g., a dev box or always-on workstation) and want to reach it from anywhere

**Use interactive mode (`claude --remote-control`) when:**
- You're working locally and want to also access your session from your phone
- You want to keep a terminal prompt open alongside remote access

---

## Starting Server Mode

```bash
claude remote-control
```

The process stays running, waiting for remote connections. It displays a session URL and listens for incoming connections via outbound HTTPS polling (no inbound ports opened).

### With a Custom Name

```bash
claude remote-control --name "My Project"
```

The name appears in the session list at claude.ai/code and in the Claude mobile app. Makes it easy to identify the right session when you have multiple servers running.

### Displaying the QR Code

Press **spacebar** to toggle QR code display on and off. Scan it with the Claude app to connect directly from your phone without typing a URL.

---

## Spawn Modes: How Concurrent Sessions Are Created

The `--spawn` flag controls what happens when a second device connects while one is already active.

```bash
claude remote-control --spawn same-dir     # default
claude remote-control --spawn worktree
```

Press **`w`** at runtime to toggle between modes without restarting.

### `same-dir` (Default)

All concurrent sessions share the same working directory.

```bash
claude remote-control --spawn same-dir
```

**When to use:** Read-only sessions (reviewing, summarizing, answering questions). Or when you want all sessions to see the same files and are comfortable managing potential conflicts manually.

**Risk:** If two sessions edit the same file simultaneously, you will get conflicts. There is no locking mechanism.

### `worktree`

Each new concurrent session gets its own Git worktree — a separate checkout of the repository in an isolated directory.

```bash
claude remote-control --spawn worktree
```

**Requires:** The working directory must be a Git repository.

**What this means in practice:**
- Session A and Session B each have their own file copies
- Changes in Session A do not affect Session B
- Each session can be committed, reviewed, or discarded independently
- Worktrees are cleaned up when the session ends

**When to use:** Any time multiple sessions might write to files. Parallel reviews, concurrent experiments, or team members hitting the same server.

**What NOT to do with `worktree` mode:**
- Don't use it on a non-Git directory — it will fail at connection time
- Don't assume worktree branches are automatically merged — manage them like any Git branch

---

## Capacity: Maximum Concurrent Sessions

```bash
claude remote-control --capacity 8
```

Sets the maximum number of concurrent sessions the server will accept. Default is 32.

**When to lower this:**
- You're on a resource-constrained machine and don't want 32 simultaneous Claude processes competing for memory and CPU
- You want to enforce a "one at a time" policy: `--capacity 1`

**When to raise or leave at default:**
- Team workflows where multiple members may connect simultaneously
- You have a powerful workstation and want generous headroom

---

## Verbose Logging

```bash
claude remote-control --verbose
```

Outputs detailed connection and session logs to stdout. Useful when:
- Diagnosing connection failures
- Confirming that sessions are properly connecting and disconnecting
- Debugging spawn behavior in `worktree` mode

---

## Sandboxing

```bash
claude remote-control --sandbox
claude remote-control --no-sandbox
```

Sandboxing restricts the server session's access to the filesystem and network beyond the working directory. Off by default.

**When to enable:** If the server is accessible to others and you want to limit what Claude Code can reach — particularly in team environments where you're exposing the session to colleagues who might send unexpected prompts.

**Trade-off:** Sandboxing prevents Claude from accessing files outside the project directory, which may break legitimate workflows that span multiple directories or read from `~/.claude/`.

---

## Full Flag Reference

```bash
claude remote-control [flags]

--name "Session Name"     Display name in session list and Claude app
--spawn same-dir          All sessions share working directory (default)
--spawn worktree          Each session gets isolated Git worktree
--capacity N              Max concurrent sessions (default: 32)
--verbose                 Detailed connection and session logs
--sandbox                 Enable filesystem/network sandboxing
--no-sandbox              Explicitly disable sandboxing (default behavior)
```

**Runtime controls (keyboard shortcuts while server is running):**

| Key | Action |
|-----|--------|
| `spacebar` | Toggle QR code display |
| `w` | Toggle spawn mode between `same-dir` and `worktree` |

---

## Practical Example: Always-On Dev Box

You have a desktop workstation or home server that's always on. You want to reach your development environment from your laptop or phone without keeping a terminal window open.

```bash
# On your dev box
cd ~/projects/my-app
claude remote-control --name "my-app dev" --spawn worktree --capacity 4 --verbose
```

From your laptop or phone:
1. Open the Claude app or claude.ai/code
2. Find "my-app dev" in the session list
3. Connect and pick up your session

Each time you connect, you get your own isolated worktree. No conflicts with yourself or with colleagues connecting to the same server.

---

## What NOT to Do

- **Don't use `--spawn same-dir` when multiple sessions will write files.** Without worktree isolation, concurrent edits to the same files will conflict. There is no locking.
- **Don't use `--spawn worktree` outside a Git repository.** The server will fail to create worktrees for connecting sessions.
- **Don't set `--capacity` to a number your machine can't handle.** Each concurrent session runs a Claude Code process. On a modest machine, 32 simultaneous sessions would be ruinous. Set a realistic limit.
- **Don't expect `--sandbox` to be a full security boundary.** It restricts filesystem and network access but is not a hardened security sandbox. Don't expose a Remote Control server to untrusted users.
- **Don't forget the terminal dependency.** Even in server mode, if you `Ctrl+C` or the terminal process exits, the server stops. Use `tmux`, `screen`, or a process manager if you want the server to survive terminal disconnects.

---

## Official Docs

- [Remote Control Overview](https://code.claude.com/docs/en/remote-control)

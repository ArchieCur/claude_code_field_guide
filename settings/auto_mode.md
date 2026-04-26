# Auto Mode and Permission Management

## Auto Mode

Auto mode is Claude Code's safest alternative to unattended operation. Instead of babysitting Claude through permission prompts — or bypassing safety with `--dangerously-skip-permissions` — auto mode routes each permission prompt to a model-based classifier that decides whether the command is safe to run. Safe commands are auto-approved. Risky ones still surface for your review.

The result: you can start a long task and switch focus to something else. You can run multiple Claude instances in parallel. When one finishes, you pick it up.

### Availability

Auto mode requires:
- **Model**: Opus 4.7
- **Plan**: Max, Teams, or Enterprise

### Enabling Auto Mode

| Interface | How to enable |
|---|---|
| CLI | Shift-Tab to cycle through modes (Ask → Plan → Auto) |
| Desktop app | Mode dropdown in the toolbar |
| VSCode | Mode dropdown in the toolbar |

The three modes:

| Mode | Behavior |
|---|---|
| **Ask** (default) | Prompts you for every permission |
| **Plan** | Claude proposes a plan before acting |
| **Auto** | Model classifier auto-approves safe commands |

### How the Classifier Works

When a permission prompt fires in auto mode, it is routed to a classifier model rather than to you. The classifier evaluates the command against a safety policy. If safe, it auto-approves and Claude continues. If not, it surfaces the prompt to you as usual.

This means auto mode is not `--dangerously-skip-permissions`. Risky commands (destructive file operations, force pushes, dropping databases) still require your approval.

---

## /fewer-permission-prompts

Even outside auto mode, you can reduce interruptions by tuning your permissions allowlist. The `/fewer-permission-prompts` skill automates this.

It scans your session history to find bash and MCP tool calls that repeatedly triggered permission prompts but are safe for your workflow. It then recommends a list of commands to add to your `settings.json` allowlist.

### Usage

Run it at the end of a session where you were interrupted often:

```
/fewer-permission-prompts
```

Review the recommendations, then add the ones that make sense to your `settings.json`:

```json
"permissions": {
  "allow": [
    "Bash(npm run lint)",
    "Bash(npm run build)"
  ]
}
```

### When to Use Each Approach

| Approach | Best for |
|---|---|
| Auto mode | Long-running tasks where you want to walk away entirely |
| `/fewer-permission-prompts` | Tuning your allowlist to reduce interruptions without auto mode |
| `--dangerously-skip-permissions` | Not recommended — no safety net |

> **Tip:** Run `/fewer-permission-prompts` after your first few sessions with a new project. You will quickly identify the safe commands that keep interrupting you and get them out of the way permanently.

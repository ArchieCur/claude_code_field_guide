# Claude Code Desktop

Desktop runs the same engine as the CLI — your CLAUDE.md files, settings, MCP servers, and hooks all carry over. What Desktop adds is a visual layer: parallel sessions with automatic git isolation, an embedded browser for live preview, inline diff review, and a sidebar that keeps every session in one window.

---

## What Desktop adds

| Feature | CLI | Desktop |
|:---|:---|:---|
| Parallel sessions | Separate terminals + `--worktree` flag | Sidebar tabs, each in its own worktree automatically |
| Diff review | Text output | Visual diff with inline commenting |
| App preview | External browser | Embedded browser with auto-verify after every edit |
| PR monitoring | Manual `gh` polling | CI status bar with auto-fix and auto-merge |
| Side questions | New session or subagent | Side chat (`Cmd+;`) using current session context |
| Computer use | Via MCP on macOS only | Full screen and app control on macOS and Windows |
| Mobile dispatch | Not available | Dispatch — send tasks from your phone |
| Session management | `--resume` / `--continue` flags | Sidebar with filter, group, and archive controls |

---

## Start a session

Configure four things in the prompt area before your first message:

- **Environment**: Local (your machine), Remote (Anthropic's cloud), or an SSH connection
- **Project folder**: the directory or repo Claude works in
- **Model**: pick from the dropdown next to the send button; changeable mid-session
- **Permission mode**: how much autonomy Claude has; changeable mid-session

| Permission mode | Behavior | Use when |
|:---|:---|:---|
| Ask permissions | Claude asks before every file edit or command | New projects or unfamiliar codebases |
| Auto accept edits | File edits auto-approved; commands still prompt | You trust the changes and want faster iteration |
| Plan mode | Read-only exploration, then proposes a plan | Complex tasks — review the approach before any edits |
| Auto | All actions with background safety checks | Routine work where you want minimal interruption |
| Bypass permissions | No prompts except explicit ask rules | Sandboxed containers only |

> **Best practice:** Start complex tasks in Plan mode so Claude maps the approach before touching files. Switch to Auto accept edits to execute once you've approved the plan.

> **Auto mode availability:** requires Claude Opus 4.6 or later, or Sonnet 4.6. In Enterprise deployments routing to Google Cloud Vertex AI, set `CLAUDE_CODE_ENABLE_AUTO_MODE` and use Opus 4.7 or 4.8.

---

## Parallel sessions

Click **+ New session** (`Cmd+N` / `Ctrl+N`) to open a second session alongside the first. Each session gets its own git worktree automatically — changes in one session never touch files in another until you commit.

Worktrees are stored in `<project-root>/.claude/worktrees/` by default. Add this to your `.gitignore`:

```text
.claude/worktrees/
```

To copy gitignored files (`.env`, secrets) into each new worktree automatically, create a `.worktreeinclude` at your project root:

```text .worktreeinclude
.env
.env.local
config/secrets.json
```

**View two sessions side by side:** hold `Cmd` / `Ctrl` and click a session in the sidebar. `Cmd+\` / `Ctrl+\` closes the focused pane. `Ctrl+Tab` / `Ctrl+Shift+Tab` cycles through all open sessions.

**Archive a session:** hover over it in the sidebar and click the archive icon. To archive automatically when a PR merges or closes, enable **Auto-archive after PR merge or close** in Settings → Claude Code.

To change the worktree directory or set a branch prefix that gets prepended to every Claude-created branch, go to Settings → Claude Code.

---

## Arrange your workspace

The Code tab is built around panes you can position freely: chat, diff, preview, terminal, file editor, plan, tasks, and subagent. Drag a pane by its header to reposition it; drag an edge to resize. Open additional panes from the **Views** menu in the session toolbar.

**Terminal pane:** press `Ctrl+\`` to toggle. Opens in the session's working directory and shares the same environment as Claude, so `npm test` and `git status` see the same files Claude is editing. Available in local sessions only.

**File editor pane:** click any file path in the chat or diff viewer to open it. Make spot edits and click **Save** to write them back. Available in local and SSH sessions.

**View modes:** press `Ctrl+O` to cycle between Normal (tool calls collapsed), Verbose (every step Claude takes), and Summary (final responses and changes only). Use Verbose when debugging why Claude took a specific action.

### Keyboard shortcuts

| Shortcut | Action |
|:---|:---|
| `Cmd+N` / `Ctrl+N` | New session |
| `Ctrl+Tab` / `Ctrl+Shift+Tab` | Next or previous session |
| `Cmd+Shift+D` | Toggle diff pane |
| `Cmd+Shift+P` | Toggle preview pane |
| `Ctrl+\`` | Toggle terminal pane |
| `Cmd+\` | Close focused pane |
| `Cmd+;` / `Ctrl+;` | Open side chat |
| `Ctrl+O` | Cycle view modes |
| `Cmd+Shift+M` | Open permission mode menu |
| `Cmd+Shift+I` | Open model menu |
| `Cmd+Shift+E` | Open effort menu |
| `Cmd+/` / `Ctrl+/` | Show all keyboard shortcuts |

On Windows, use `Ctrl` in place of `Cmd` except where noted.

---

## Review changes

### Diff view

When Claude edits files, a `+N -N` indicator appears in the session toolbar. Click it to open the diff viewer: file list on the left, per-file changes on the right.

Click any line to leave an inline comment. After commenting across multiple lines, submit all at once with `Cmd+Enter` / `Ctrl+Enter`. Claude reads all comments and makes the revisions in one pass, then produces a new diff to review.

Click **Review code** in the diff toolbar to have Claude evaluate the changes itself before you commit. It flags compile errors, definite logic errors, security vulnerabilities, and obvious bugs — not style, formatting, or anything a linter would catch.

### PR monitoring

After opening a PR, a CI status bar appears in the session. Claude Code polls GitHub check results via the GitHub CLI.

- **Auto-fix:** Claude reads failing CI output and iterates until checks pass
- **Auto-merge:** Claude merges the PR once all checks pass (squash merge). Requires auto-merge to be enabled in your GitHub repository settings.

> Requires the [GitHub CLI (`gh`)](https://cli.github.com/) installed and authenticated.

---

## Preview your app

Claude can start a dev server and open an embedded browser to verify its own changes. For most projects it detects the setup automatically and stores the configuration in `.claude/launch.json`. See the included `launch.json` template for common configurations.

**Auto-verify** is on by default: after every file edit Claude takes screenshots, checks for errors, clicks through the UI, and iterates before completing its response. Disable per-project by adding `"autoVerify": false` to `.claude/launch.json`, or toggle it from the **Preview** dropdown.

From the preview pane you can:

- Interact with the running app directly in the embedded browser
- Start or stop servers from the **Preview** dropdown
- Toggle **Persist sessions** so cookies and local storage survive server restarts (avoids re-logging in during development)
- Click any HTML, PDF, image, or video path in the chat to open it in the preview pane

---

## Side chats

A side chat lets you ask Claude a question using the session's full context without adding anything back to the main thread. Use it to check an assumption, understand a piece of code, or explore an idea without steering the session off course.

Press `Cmd+;` / `Ctrl+;` or type `/btw` in the prompt box to open a side chat. Close it and the main session continues exactly where it left off. Available in local and SSH sessions.

---

## Computer use

Computer use lets Claude open apps, control your screen, and interact with anything that has no CLI or API — native apps, hardware control panels, mobile simulators, proprietary tools with no API.

> Research preview on macOS and Windows. Requires a Pro or Max plan. Not available on Team or Enterprise plans.

**How Claude decides which tool to use:** it tries the most precise option first — a connector, then Bash, then Claude in Chrome, then computer use as the last resort. Computer use is reserved for things nothing else can reach.

### Enable computer use

1. Update to the latest Claude Desktop
2. Go to **Settings → General** and turn on the **Computer use** toggle
3. **macOS only:** grant **Accessibility** and **Screen Recording** in System Settings (the Settings page shows current status of each; click the badge to open the relevant pane)
4. **Windows:** the toggle takes effect immediately — no additional permissions needed

### App permissions

The first time Claude needs to interact with an app, a prompt appears in your session. Approvals last for the current session. Access tiers are fixed by app category and cannot be changed:

| Tier | What Claude can do | Applies to |
|:---|:---|:---|
| View only | See the app in screenshots | Browsers, trading platforms |
| Click only | Click and scroll; no typing or keyboard shortcuts | Terminals, IDEs |
| Full control | Click, type, drag, and use keyboard shortcuts | Everything else |

> Terminals, Finder / File Explorer, and System Settings / Settings show an extra warning before you approve — these apps have broad reach.

**Configure in Settings → General:**
- **Denied apps:** add apps here to reject them without prompting
- **Unhide apps when Claude finishes:** while Claude is working your other windows are hidden; toggle this off to keep them visible

### Dispatch-spawned sessions and computer use

If computer use is enabled, sessions spawned by Dispatch can use it too. App approvals in those sessions expire after 30 minutes and re-prompt, rather than lasting the full session.

---

## Cloud and SSH sessions

### Cloud sessions

Select **Remote** instead of **Local** when starting a session to run on Anthropic's cloud infrastructure. The session continues even if you close the app or shut down your computer. Monitor progress from [claude.ai/code](https://claude.ai/code) or the Claude iOS app.

Cloud sessions also support **multiple repositories:** click **+** next to the repo pill to add additional repos to the session, each with its own branch selector. Useful for tasks that span codebases — updating a shared library and its consumers in one session.

**Use cloud sessions when:**
- The task will outlast your machine or network connection
- You want to check progress from another device
- The task spans multiple repositories

### SSH sessions

SSH sessions run Claude Code on a remote machine while using Desktop as your interface — useful for codebases that live on cloud VMs, dev containers, or servers with specific hardware or dependencies.

Add a connection from the environment dropdown → **+ Add SSH connection**. Provide:
- **Name:** a friendly label
- **SSH Host:** `user@hostname` or a host from `~/.ssh/config`
- **SSH Port:** defaults to 22
- **Identity File:** path to your private key; leave empty to use the default key

Once added, select the connection from the dropdown to start a session on that machine. Desktop installs Claude Code on the remote automatically the first time you connect. The remote machine must run Linux or macOS.

SSH sessions support permission modes, connectors, plugins, and MCP servers. The terminal and file editor panes are available; the preview pane is not.

**Pre-configure connections for your team** via managed settings (distributable via MDM):

```json
{
  "sshConfigs": [
    {
      "id": "shared-dev-vm",
      "name": "Shared Dev VM",
      "sshHost": "user@dev.example.com",
      "sshPort": 22,
      "sshIdentityFile": "~/.ssh/id_ed25519",
      "startDirectory": "~/projects"
    }
  ]
}
```

**Restrict which hosts users can connect to** with `sshHostAllowlist` in managed settings:

```json
{
  "sshHostAllowlist": ["*.devboxes.example.com", "bastion.example.com"]
}
```

Patterns are case-insensitive. `*` matches any host; `*.example.com` matches the domain and all subdomains. Anything else is an exact match. The check resolves against the hostname after `~/.ssh/config` processing, so `Host` aliases are permitted as long as the resolved `HostName` matches.

> `sshHostAllowlist` is read from managed settings only — user or project settings are ignored. It governs Desktop connections only, not network egress or `ssh` commands run through the Bash tool.

---

## Enterprise

Desktop supports enterprise deployment through the admin console, managed settings files, and MDM / group policy.

**Admin console** at [claude.ai/admin-settings/claude-code](https://claude.ai/admin-settings/claude-code):
- Enable or disable Claude Code in the desktop app
- Enable or disable web sessions for your organization
- Enable or disable Remote Control
- Disable Bypass permissions mode org-wide

**Managed settings keys:**

| Key | What it does |
|:---|:---|
| `permissions.disableBypassPermissionsMode` | Set to `"disable"` to prevent Bypass permissions mode |
| `disableAutoMode` | Set to `"disable"` to remove Auto mode from the selector |
| `autoMode` | Customize what the auto-mode safety classifier trusts and blocks |
| `sshConfigs` | Pre-configure SSH connections for all users |
| `sshHostAllowlist` | Restrict SSH sessions to approved host patterns |
| `managedMcpServers` | Push MCP server configurations to all users (3P deployments only) |

Managed settings override project and user settings. Place `disableBypassPermissionsMode` and `disableAutoMode` in managed settings to prevent users from overriding them. `autoMode` classifier rules are not read from checked-in `.claude/settings.json` — a cloned repo cannot inject its own rules.

**Device management:**
- macOS: `com.anthropic.claudefordesktop` preference domain via Jamf, Kandji, or similar
- Windows: registry at `SOFTWARE\Policies\Claude`; use MSIX package or `.exe` installer for deployment

For the full enterprise build sequence and harness configuration, see the [enterprise folder](../enterprise/).

---

## Dispatch

[Dispatch](https://support.claude.com/en/articles/13947068) is a persistent conversation in the Claude Cowork tab. Message it a task and it decides how to handle it — development work routes to a Code session automatically.

Tasks that route to Code: fixing bugs, updating dependencies, running tests, opening PRs. Research, document editing, and spreadsheet work stay in Cowork.

Code sessions spawned by Dispatch appear in the sidebar with a **Dispatch** badge. You get a push notification on your phone when the session finishes or needs your approval.  

**More detail-** [Dispatch](dispatch/dispatch_README.md)  


> Requires Pro or Max plan. Not available on Team or Enterprise.

---

## Key settings reference

| Setting | Where to change | What it does |
|:---|:---|:---|
| Worktree location | Settings → Claude Code | Override the default `.claude/worktrees/` path |
| Branch prefix | Settings → Claude Code | Prepend a string to every worktree branch name |
| Auto-archive | Settings → Claude Code | Archive sessions automatically when their PR merges |
| Auto-verify | `.claude/launch.json` or Preview dropdown | Toggle automatic post-edit browser verification |
| Persist preview sessions | Settings → Claude Code | Keep cookies/storage across dev server restarts |
| Computer use | Settings → General | Enable screen and app control (Pro/Max only) |
| Denied apps | Settings → General | Block specific apps from computer use without prompting |
| MAX_THINKING_TOKENS | Local environment editor | Set to `0` to disable extended thinking |

Set environment variables for local sessions and dev servers from the environment dropdown → hover **Local** → click the gear icon. Variables are stored encrypted on your machine and apply to every local session and preview server.

---

## Moving between Desktop and CLI

Desktop and CLI share the same configuration — CLAUDE.md files, settings, MCP servers, hooks, and models are identical in both. You can run them simultaneously on the same project.

To move a CLI session into Desktop: run `/desktop` in the terminal. Claude saves the session and opens it in the app, then exits the CLI. Available on macOS and Windows with a Claude subscription; not available with API key auth or on Bedrock, Vertex AI, or Foundry.

---

## Related resources

- [Desktop app docs](https://code.claude.com/docs/en/desktop.md)
- [Worktrees](https://code.claude.com/docs/en/worktrees.md) — worktree mechanics in depth
- [Computer use safety guide](https://support.claude.com/en/articles/14128542)
- [Cloud sessions](https://code.claude.com/docs/en/claude-code-on-the-web.md)
- [Dispatch help](https://support.claude.com/en/articles/13947068)
- [Enterprise configuration guide](https://support.claude.com/en/articles/12622667-enterprise-configuration)

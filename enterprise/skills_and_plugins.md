# Skills and Plugins at Scale

In a large codebase with dozens of task types, not all expertise needs to be present in every session. Loading everything into CLAUDE.md bloats context and degrades performance. Skills and plugins solve this through progressive disclosure: specialized knowledge loads only when the task calls for it, and what works for one engineer reaches every engineer through plugins.

---

## Skills: progressive disclosure for large codebases

A skill is a `SKILL.md` file that Claude loads automatically when relevant, or that you invoke directly with `/skill-name`. Unlike CLAUDE.md content — which loads in every session — a skill's content only costs context when the skill is actually used.

**Move this out of CLAUDE.md and into skills:**
- Multi-step procedures (deploy workflows, release processes, migration steps)
- Domain-specific conventions that apply to one part of the codebase
- Reference material that's useful sometimes but noise most of the time
- Security review checklists, performance analysis patterns, documentation templates

**Keep this in CLAUDE.md:**
- Facts Claude needs to navigate the codebase (what top-level directories are, key naming conventions)
- Non-obvious gotchas that apply to any task in this project
- Pointers to skills: "For deployment, use `/deploy`"

---

## Path-scoped skills

Skills can be scoped to specific paths so they only activate when Claude is working in a relevant part of the codebase. A payments team can bind their deployment skill to `services/payments/` — it never auto-loads when someone is working in `services/auth/`.

Set the `paths` field in the skill's frontmatter:

```yaml
---
name: payments-deploy
description: Deploy the payments service to production
paths: services/payments/**
disable-model-invocation: true
---

Deploy the payments service:
1. Run the payments test suite: `cd services/payments && npm test`
2. Build: `npm run build`
3. Push to the payments deployment target
4. Verify the health check at https://payments.internal/health
```

This prevents skills from competing for context in parts of the codebase where they don't apply — especially valuable in monorepos where teams own separate services with different deployment patterns, test commands, and conventions.

---

## Where skills live

| Location | Path | Who can use it |
|:---|:---|:---|
| Personal | `~/.claude/skills/<skill-name>/SKILL.md` | You, across all projects |
| Project | `.claude/skills/<skill-name>/SKILL.md` | Everyone working in this project |
| Plugin | `<plugin>/skills/<skill-name>/SKILL.md` | Everyone with the plugin installed |
| Enterprise | Managed settings | All users in the organization |

For skills that should reach everyone on a team, put them in a plugin rather than asking everyone to copy files manually.

---

## Controlling who invokes a skill

Two frontmatter fields control whether Claude triggers a skill automatically or whether it requires explicit invocation:

| Frontmatter | You can invoke | Claude can invoke |
|:---|:---|:---|
| (default) | Yes | Yes |
| `disable-model-invocation: true` | Yes | No |
| `user-invocable: false` | No | Yes |

Use `disable-model-invocation: true` for skills with side effects you want to control — deployments, releases, anything that sends external messages. You don't want Claude deciding to deploy because the code looks ready.

Use `user-invocable: false` for background context skills that inform Claude's behavior but aren't meant to be commands — a `legacy-api-context` skill that explains how an old system works, for example.

---

## Controlling how a skill executes

Beyond who can invoke a skill, frontmatter fields let you control *how* it runs. This matters at enterprise scale where context management, security, and team usability all carry more weight.

| Field | What it does | When to use it |
|:---|:---|:---|
| `context: fork` | Runs the skill in an isolated sub-agent with its own context window | Exploratory or verbose skills — prevents attentional residue from accumulating in the main session |
| `allowed-tools` | Restricts which tools the skill can access during execution | Enforce least-privilege access; prevent accidental destructive actions inside a skill |
| `argument-hint` | Shown during autocomplete to prompt the user for required inputs | Any skill that needs a specific parameter (file path, service name, target environment) to work correctly |

A skill that maps a subsystem, for example, is exactly the kind of verbose exploration that benefits from `context: fork` — the findings come back as a summary, and the main session stays clean:

```yaml
---
name: map-subsystem
description: Map the structure and dependencies of a subsystem. Use when exploring an unfamiliar part of the codebase.
context: fork
allowed-tools: Read Grep Glob
argument-hint: <subsystem-path>
---

Map the subsystem at $ARGUMENTS:
1. Identify all entry points and public interfaces
2. Trace key dependencies
3. Note any non-obvious constraints or gotchas
4. Write findings to subsystem-map.md
```

`allowed-tools` is also a governance tool: a skill distributed through a team plugin can declare exactly which tools it needs, so security reviewers can audit skill permissions the same way they audit any other access policy.

---

## Plugins: distributing what works

A plugin bundles skills, hooks, MCP server configurations, and other settings into a single installable package. When you've invested in building the right skills and hooks for your team's workflow, a plugin is how you stop that knowledge from staying tribal.

When a new engineer installs the team plugin on day one, they immediately have the same context and capabilities as someone who has been working in the codebase for a year — without any manual file copying or tribal knowledge transfer.

**Standalone config vs. plugins:**

| | Standalone (`.claude/`) | Plugin |
|:---|:---|:---|
| **Scope** | One project | Anywhere it's installed |
| **Sharing** | Manual copy | `/plugin install` |
| **Updates** | Manual | Versioned, distributed through marketplace |
| **Skill names** | `/skill-name` | `/plugin-name:skill-name` |

Start with standalone config in `.claude/skills/` while iterating. Convert to a plugin when the skills are stable and you want them to reach others.

---

## Creating a plugin

Every plugin is a directory with a `.claude-plugin/plugin.json` manifest:

```json
{
  "name": "payments-team",
  "description": "Skills and hooks for the payments service team",
  "version": "1.0.0"
}
```

Plugin structure:

```
payments-team/
├── .claude-plugin/
│   └── plugin.json          ← manifest (only file that goes here)
├── skills/
│   └── payments-deploy/
│       └── SKILL.md
├── hooks/
│   └── hooks.json
└── .mcp.json                ← MCP server configurations (if any)
```

> **Common mistake**: Don't put `skills/`, `hooks/`, or other directories inside `.claude-plugin/`. Only `plugin.json` goes there. Everything else belongs at the plugin root.

Test locally before distributing:

```bash
claude --plugin-dir ./payments-team
```

---

## Distributing through a marketplace

A plugin marketplace is a repository with a `marketplace.json` index listing available plugins. Teams configure it once in settings, and every developer installs from it using `/plugin install`.

Add the marketplace to your settings:

```json
{
  "marketplaces": [
    {
      "name": "Internal Tools",
      "sourceType": "github",
      "sourceUrl": "https://github.com/your-org/claude-plugins"
    }
  ]
}
```

For regulated organizations, host the marketplace in a private repository and control which plugins are listed. This lets you vet plugins centrally rather than relying on every developer to make good choices independently. Plugin updates reach everyone through the marketplace rather than requiring manual file distribution.

---

## Converting existing config to a plugin

If you already have skills or hooks in `.claude/`, converting them to a plugin is straightforward:

```bash
mkdir -p my-plugin/.claude-plugin
```

Create the manifest:

```json
{
  "name": "my-plugin",
  "description": "Migrated from standalone configuration",
  "version": "1.0.0"
}
```

Then copy your existing files:

```bash
cp -r .claude/commands my-plugin/
cp -r .claude/skills my-plugin/    # if any
```

For hooks, create `my-plugin/hooks/hooks.json` using the same format as the `hooks` object in your `settings.json`.

---

## Related

- [README.md](README.md) — The full harness overview and build sequence
- [maintenance_and_governance.md](maintenance_and_governance.md) — Managing plugin marketplaces for governance
- [../hooks/README.md](../hooks/README.md) — Hooks for automation and enforcement
- [Agent Skills docs](https://code.claude.com/docs/en/skills) — Complete skills reference
- [Plugins docs](https://code.claude.com/docs/en/plugins) — Complete plugins reference
- [Plugin marketplaces](https://code.claude.com/docs/en/plugin-marketplaces) — Setting up and managing plugin distribution

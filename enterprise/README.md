# Enterprise & Large Codebase Guide

Claude Code runs in production across multi-million-line monorepos, decades-old legacy systems, and organizations with thousands of developers. The challenges at that scale are distinct: build commands that differ per subdirectory, legacy code with no conventional structure, teams who independently rebuild the same tooling, and governance questions that don't arise when it's just you.

This section covers the patterns that work at scale, drawn from Anthropic's Applied AI team's observations across large deployments.

---

## The harness matters more than the model

The most common misconception about Claude Code is that performance is determined by the model. In practice, the ecosystem built around the model — the **harness** — determines outcomes more than the model alone.

The harness has five extension points plus two additional capabilities. Build them in order: each layer builds on what came before.

| Component | What it does | When it loads | Common mistake |
|:---|:---|:---|:---|
| **CLAUDE.md files** | Context Claude reads at session start | Every session, automatically | Letting it become a dumping ground — it should be pointers and critical gotchas only |
| **Hooks** | Scripts that run before/after tool events | On matching tool events | Using hooks only to block bad actions, not to propose CLAUDE.md updates or load dynamic context |
| **Skills** | On-demand expertise that loads only when relevant | When task matches skill description | Loading all expertise into CLAUDE.md instead — skills exist specifically to avoid that |
| **Plugins** | Bundles of skills, hooks, and MCP config, distributable across a team | When installed and enabled | Keeping good setups tribal — what works for one engineer should reach everyone |
| **MCP servers** | Connections to internal tools, data sources, and APIs Claude can't otherwise reach | Per session, based on configuration | Adding MCP before the simpler layers are solid |
| **LSP integrations** | Symbol-level code navigation matching what a developer sees in their IDE | When Claude navigates code | Skipping LSP in compiled-language codebases where grep returns thousands of false matches |
| **Subagents** | Isolated Claude instances that take a task, do the work, and return only the result | On demand | Reaching for subagents before the rest of the harness is in place |

---

## Build sequence

The order matters. A harness built out of sequence leaves each layer weaker.

1. **CLAUDE.md first** — Claude needs codebase knowledge before anything else works well. Start at the root, add subdirectory files as you go deeper.
2. **Hooks second** — Once Claude is navigating correctly, hooks make the setup self-correcting. A stop hook that proposes CLAUDE.md updates compounds every session.
3. **Skills third** — Move specialized knowledge and procedures out of CLAUDE.md and into skills that load only when needed.
4. **Plugins fourth** — Package what works into a distributable form so it reaches every engineer automatically.
5. **MCP + LSP last** — Connect Claude to internal tools and give it symbol-level navigation once the foundation is solid.

### Why this order?

It's easy to focus on *what* to include and lose sight of *how and when the model actually uses it*. The sequence follows the model's behavior, not your preferences as a configurator:

- **Hooks are the on/off switches.** They control what Claude can and can't do. Those boundaries need to be in place before you add complexity on top of them.
- **Skills load progressively.** There's no point packaging specialized expertise until you know what expertise is actually needed session to session. Build the skill when the pattern repeats, not in anticipation of it.
- **Plugins deliver what isn't native.** A plugin is a wrapper around things you've already proven work. Packaging unproven config just distributes the problem.
- **MCP + LSP last** means the model isn't navigating a laundry list of connectors and servers at the start of every task. A lean, well-structured harness first — connections to the outside world after.

---

## Getting started checklist

### Foundation
- [ ] Write a root CLAUDE.md covering project structure, key conventions, and critical gotchas
- [ ] Add subdirectory CLAUDE.md files for modules with their own conventions or build commands
- [ ] Add `.claude/settings.json` with `permissions.deny` rules to exclude generated files and build artifacts
- [ ] Verify Claude can find, read, and build the right things before going further

### Hooks
- [ ] Add a stop hook that reflects on the session and proposes CLAUDE.md updates
- [ ] Add a start hook for any context that varies by developer or module
- [ ] Wire lint and formatting checks as hooks (deterministic enforcement beats instructions)

### Skills and plugins
- [ ] Identify procedures that recur across sessions and move them to skills
- [ ] Scope skills to the paths where they apply
- [ ] Package org-wide skills into a plugin and distribute it through your marketplace

### Navigation
- [ ] Install a code intelligence plugin for your primary language(s)
- [ ] Install the corresponding language server binary
- [ ] Verify Claude uses symbol lookup rather than grep for common function lookups

### Organization
- [ ] Assign a DRI or team responsible for the Claude Code configuration
- [ ] Document which plugins and skills are approved for use
- [ ] Establish a review process for AI-generated code changes
- [ ] Schedule a configuration review for three months out

---

## What's in this folder

| File | Covers |
|:---|:---|
| [claude_md_at_scale.md](claude_md_at_scale.md) | Layered CLAUDE.md hierarchies, lean root files, subdirectory scoping, codebase maps |
| [skills_and_plugins.md](skills_and_plugins.md) | Progressive disclosure with skills, path-scoped skills, packaging and distributing plugins |
| [lsp_integrations.md](lsp_integrations.md) | Symbol-level navigation, language server setup, when LSP matters most |
| [maintenance_and_governance.md](maintenance_and_governance.md) | CLAUDE.md review cadence, ownership models, governance for regulated industries |

---

## Related

- [hooks/README.md](../hooks/README.md) — Hook scripts for automation and enforcement
- [CLAUDE_md_templates/](../CLAUDE_md_templates/) — Starting templates for CLAUDE.md
- [agent_teams/README.md](../agent_teams/README.md) — Coordinating multiple Claude instances
- [Anthropic blog: How Claude Code works in large codebases](https://claude.com/blog/how-claude-code-works-in-large-codebases)

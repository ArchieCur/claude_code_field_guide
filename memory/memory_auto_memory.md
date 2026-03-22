# Auto Memory

Auto memory lets Claude accumulate knowledge across sessions without you writing anything. As you work, Claude saves notes for itself — build commands, debugging insights, architecture decisions, code style preferences, workflow habits. It doesn't save something every session. It decides what's worth remembering based on whether the information would be useful in a future conversation.

> **Minimum version:** Claude Code v2.1.59+ | Check with `claude --version`

---

## Enabling and Disabling Auto Memory

Auto memory is **on by default**.

**Toggle it in a session:**
```bash
/memory    # then use the auto memory toggle
```

**Disable via settings** (`~/.claude/settings.json` or `.claude/settings.json`):
```json
{
  "autoMemoryEnabled": false
}
```

**Disable via environment variable:**
```bash
export CLAUDE_CODE_DISABLE_AUTO_MEMORY=1
```

---

## Where Memory Lives

Each project gets its own memory directory:

```
~/.claude/projects/<project>/memory/
├── MEMORY.md          # Concise index — loaded every session (first 200 lines)
├── debugging.md       # Detailed notes on debugging patterns
├── api-conventions.md # API design decisions
└── ...                # Any other topic files Claude creates
```

The `<project>` path is derived from your **git repository root** — not the specific subdirectory you're working in. This means:
- All worktrees of the same repo share one auto memory directory
- All subdirectories within the same repo share one auto memory directory
- Memory is machine-local — not shared across machines or cloud environments

**To store memory in a custom location** (user or local settings only):
```json
{
  "autoMemoryDirectory": "~/my-custom-memory-dir"
}
```

> **Note:** `autoMemoryDirectory` is intentionally not accepted in project-level `.claude/settings.json`. This prevents a shared project from redirecting memory writes to sensitive locations on team members' machines.

---

## The 200-Line Architecture

This is the most important design constraint in auto memory. Understanding it shapes how you and Claude should manage memory files.

**`MEMORY.md` — the index:**
- The **first 200 lines** are loaded into every session automatically
- Content beyond line 200 is **not loaded** at session start
- Claude is instructed to keep `MEMORY.md` concise by moving detailed notes into separate topic files

**Topic files (`debugging.md`, `patterns.md`, etc.):**
- Are **not loaded at startup** — they have no automatic 200-line constraint
- Claude reads them **on demand** using its standard file tools when it needs the information
- Can grow as large as needed without affecting session startup

**CLAUDE.md files:**
- Are loaded **in full** regardless of length
- But: target under 200 lines for best adherence (longer files consume more context and Claude follows them less consistently)

**What this means in practice:** `MEMORY.md` should be a curated index — pointers and short summaries — not a content store. The content lives in topic files.

---

## Memory Hygiene

Sonnet's question: *Is there a memory hygiene practice worth recommending?* Yes — and the 200-line limit makes it necessary, not optional.

### What to Prioritize in MEMORY.md (the 200-Line Budget)

Think of `MEMORY.md` as prime real estate. Every line consumed by low-value content is a line that could have carried something Claude acts on daily. Prioritize in this order:

**1. Corrections and preferences (highest value)**
Things Claude got wrong and you corrected. These prevent the same mistake from recurring.
```
User prefers pnpm over npm — always use pnpm
Tests must hit a real database — never mock the DB layer
```

**2. Project-specific commands and gotchas**
Things Claude can't discover from the code alone.
```
Build: `make build` not `npm run build`
Dev server requires Redis on port 6379 — run `docker-compose up redis` first
```

**3. Architecture pointers**
Short breadcrumbs that tell Claude where to look, not full explanations.
```
Auth logic: see debugging.md → Authentication section
API conventions: see api-conventions.md
```

**4. What NOT to put in MEMORY.md**
- Detailed explanations (→ move to a topic file)
- Things already in CLAUDE.md (duplication wastes budget)
- Stale entries for patterns that no longer exist
- One-time observations unlikely to recur

### Recommended Hygiene Practices

**Review memory after major refactors:**
When you rename modules, change architecture, or swap dependencies, old memory entries become wrong. Run `/memory`, open the auto memory folder, and delete or update stale entries.

**Ask Claude to curate proactively:**
Include this in a session when memory is getting long:
```
Review your auto memory files. Archive or delete anything that's stale,
consolidate duplicates, and make sure MEMORY.md stays under 200 lines
with the most important entries at the top.
```

**Move detail out of the index:**
If Claude puts a multi-paragraph explanation in `MEMORY.md`, ask it to move the detail to a topic file and leave only a pointer in `MEMORY.md`.

**Periodically delete the whole directory and start fresh:**
For long-running projects, old memory can accumulate contradictions. Starting clean is sometimes better than pruning.
```bash
rm -rf ~/.claude/projects/<project>/memory/
```
Claude will rebuild from scratch in subsequent sessions.

---

## How Claude Decides What to Save

Claude doesn't save something every session. It looks for:
- Things you corrected it on
- Commands or patterns you use repeatedly
- Architecture or workflow knowledge that isn't obvious from the code
- Preferences it discovered through your feedback

When you see **"Writing memory"** or **"Recalled memory"** in the interface, Claude is actively updating or reading from the memory directory.

**You can also ask Claude directly:**
```
Remember that we always run integration tests before merging
Remember that the staging environment uses a different auth provider
Forget what you saved about the old webpack config — we've moved to Vite
```

Claude saves to auto memory, not CLAUDE.md, unless you specify otherwise:
```
Add this to CLAUDE.md: always use the team's ESLint config, never override it
```

---

## Auditing Your Memory

**From inside a session:**
```bash
/memory    # lists all memory files, lets you open any of them
```

**From the filesystem directly:**
Auto memory files are plain markdown — open, edit, or delete them in any text editor or file explorer. There's no proprietary format.

```bash
# View what's in memory for the current project
cat ~/.claude/projects/$(basename $(git rev-parse --show-toplevel))/memory/MEMORY.md

# List all topic files
ls ~/.claude/projects/$(basename $(git rev-parse --show-toplevel))/memory/
```

---

## Subagent Memory

Subagents can maintain their own separate memory directories — independent of the main session's auto memory. This is configured per-subagent in its markdown frontmatter:

```yaml
---
name: code-reviewer
description: Reviews code for quality and best practices
memory: project
---
```

**Three scopes for subagent memory:**

| Scope | Location | Use when |
|-------|----------|----------|
| `user` | `~/.claude/agent-memory/<agent-name>/` | Knowledge applies across all projects |
| `project` | `.claude/agent-memory/<agent-name>/` | Knowledge is project-specific; share via version control |
| `local` | `.claude/agent-memory-local/<agent-name>/` | Project-specific but should NOT be committed |

**`project` is the recommended default.** It keeps subagent knowledge in version control alongside your code, so the whole team benefits.

**The same 200-line MEMORY.md limit applies to subagent memory.** The same hygiene practices apply.

**To make a subagent proactively maintain its memory**, include instructions directly in its system prompt:

```markdown
Update your agent memory as you discover codepaths, patterns, library
locations, and key architectural decisions. This builds up institutional
knowledge across conversations. Write concise notes about what you found
and where.
```

**To make a subagent use its accumulated memory**, prompt it explicitly:
```
Review this PR, and check your memory for patterns you've seen before.
```

---

## What NOT to Do

- **Don't let `MEMORY.md` exceed 200 lines without curation.** Content beyond line 200 is invisible to Claude at session start. If your index is bloated, the most important entries may be getting buried below the cutoff.
- **Don't duplicate content between CLAUDE.md and auto memory.** They're different layers. If you want Claude to reliably follow a rule, put it in CLAUDE.md. Auto memory is for learned patterns, not enforced rules.
- **Don't assume auto memory survives across machines.** It's machine-local. If you work on multiple machines, you'll have separate memory stores.
- **Don't set `autoMemoryDirectory` in project-level settings.** It's intentionally blocked there — setting it at the project level could redirect all team members' memory writes to a location you control.
- **Don't ignore stale memory after major refactors.** Wrong memory is worse than no memory — Claude may act confidently on outdated information.

---

## Environment Variable Reference

| Variable | Effect |
|----------|--------|
| `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1` | Disables auto memory entirely |

**Settings keys** (`~/.claude/settings.json` or `.claude/settings.json`):

| Key | Type | Default | Notes |
|-----|------|---------|-------|
| `autoMemoryEnabled` | boolean | `true` | Toggle auto memory on/off |
| `autoMemoryDirectory` | string | `~/.claude/projects/<project>/memory/` | Custom memory path (user/local settings only) |

---

## Official Docs

- [Memory Overview](https://code.claude.com/docs/en/memory)
- [Subagent Memory](https://code.claude.com/docs/en/sub-agents#enable-persistent-memory)

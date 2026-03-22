# Memory

Claude Code has two complementary memory systems. Both load at the start of every session. Understanding how they differ — and who writes each one — determines how you use them.

| | CLAUDE.md files | Auto memory |
|--|----------------|-------------|
| **Who writes it** | You | Claude |
| **What it contains** | Instructions and rules | Learnings and patterns |
| **Scope** | Project, user, or org | Per git repository (machine-local) |
| **Loaded into** | Every session (in full) | Every session (first 200 lines of `MEMORY.md`) |
| **Use for** | Coding standards, workflows, project architecture | Build commands, debugging insights, preferences Claude discovers |

**The one-sentence version:**
- **CLAUDE.md** — you tell Claude how to work
- **Auto memory** — Claude tells itself what it learned

These are not competing systems. They are complementary layers. Use both.

> **Already have CLAUDE.md templates?** The repo's [CLAUDE_md_templates/](../CLAUDE_md_templates/) folder covers how to write effective CLAUDE.md files. This guide focuses on auto memory and how the two systems interact.

---

## Which System Should I Use?

```
Do I want Claude to remember this permanently and act on it reliably?
├── Yes, and I want to write it myself → CLAUDE.md
└── Yes, but I want Claude to figure it out from our work → Auto memory
    └── Is this something Claude discovered mid-session?
        ├── Yes → Auto memory (Claude saves it automatically)
        └── No, I want to tell Claude something now → Ask Claude to save it:
            "Remember that we use pnpm, not npm"
```

---

## The `/memory` Command

`/memory` is your control panel for both systems:

- Lists all CLAUDE.md and rules files loaded in your current session
- Toggles auto memory on or off
- Provides a link to open the auto memory folder
- Select any file to open it in your editor for direct editing

Run `/memory` any time you want to see exactly what Claude is working from, or to audit what auto memory has saved.

---

## A Note on "Bring Your Own Memory"

Anthropic recently released an **Import memory** feature on claude.ai that lets you export memory from other AI tools (ChatGPT, Gemini, Copilot) and import it into Claude. The flow is intentionally simple: copy a prompt, paste it into your other AI, paste the result into Claude.ai.

This is a **claude.ai feature**, not a Claude Code feature. It populates the conversational memory on claude.ai and does not directly interact with CLAUDE.md or auto memory files on your machine.

If you're migrating from another AI coding agent and want that context in Claude Code, the right place for it is your `~/.claude/CLAUDE.md` — your personal instructions file that applies across all projects.

---

## Related Guides

- [Auto Memory](auto_memory.md) — how Claude saves learnings, the 200-line architecture, memory hygiene, and subagent memory
- [CLAUDE.md Templates](../CLAUDE_md_templates/) — ready-to-use templates for generic, Python, and web projects
- [Subagents](../sub_agents/) — how subagents maintain their own separate memory directories

# CLAUDE.md at Scale

In a single project, one CLAUDE.md file at the root is usually enough. In a large codebase — a monorepo with dozens of services, a legacy system with no conventional structure, or a distributed architecture across many repositories — that pattern breaks down. The root file becomes bloated, subdirectory conventions get lost, and Claude navigates blind in the parts of the codebase it needs most.

The solution is a layered approach: root file for the big picture, subdirectory files for local conventions, loaded additively as Claude moves through the codebase.

---

## The layered hierarchy

Claude loads CLAUDE.md files additively: it reads the root file first, then any subdirectory CLAUDE.md it encounters as it traverses the tree. Root-level context is never lost when working in subdirectories — Claude accumulates it.

**Root CLAUDE.md — pointers and critical gotchas only**

The root file should answer: what is this codebase, what are the top-level pieces, and what would trip up someone new? Keep it short. Every line loads in every session regardless of what Claude is working on. Content that only applies to one service doesn't belong here.

Good root file contents:
- High-level architecture overview (3–5 sentences)
- How to find things: where services live, naming conventions for directories
- Build and test commands at the repo level
- Non-obvious gotchas that apply everywhere (auth quirks, shared config patterns, things that burned previous engineers)
- Pointers to subdirectory CLAUDE.md files for deeper detail

**Subdirectory CLAUDE.md — local conventions, loaded on demand**

Each subdirectory file covers only what's true in that part of the codebase. Claude loads these as it moves into the relevant directories, so they add context without burdening sessions that don't touch those areas.

Good subdirectory file contents:
- Local build and test commands
- Service-specific conventions that differ from the root
- Key files and their purpose
- Known landmines and workarounds specific to this module

---

## Starting in subdirectories, not at the root

In a monorepo, starting Claude at the repository root and asking it to work on a single service forces it to hold unnecessary context and search a much larger space. Start Claude in the directory most relevant to the task.

```bash
# Instead of:
cd /repo && claude

# Start where the work is:
cd /repo/services/payments && claude
```

Claude automatically walks up the directory tree and loads every CLAUDE.md it finds along the way, so root-level context is still available. You get subdirectory focus without losing the big picture.

---

## Scoping test and lint commands

Running the full test suite when Claude changes one service wastes context on irrelevant output and often times out. Subdirectory CLAUDE.md files should specify the commands that apply locally.

```markdown
## Build and test

Test this service only:
```bash
cd services/payments && npm test
```

Lint:
```bash
npm run lint -- --filter=payments
```

Do not run `npm test` from the repo root — it runs all services and takes 20+ minutes.
```

This pattern works well for service-oriented monorepos. In compiled-language monorepos with deep cross-directory dependencies, per-subdirectory scoping is harder and may require project-specific build configurations.

---

## Excluding noise with .claudeignore and deny rules

Generated files, build artifacts, and vendored third-party code produce false matches that waste context. Two tools for reducing this noise:

**`.claudeignore` file** — same syntax as `.gitignore`, excludes paths from Claude's file search:

```
# Build artifacts
dist/
build/
.next/
target/

# Generated code
src/generated/
**/*.pb.go
prisma/generated/

# Dependencies
node_modules/
vendor/
```

**`permissions.deny` in `.claude/settings.json`** — version-controlled exclusions that apply for every developer on the team:

```json
{
  "permissions": {
    "deny": [
      "Read(**/node_modules/**)",
      "Read(**/dist/**)",
      "Read(**/*.pb.go)"
    ]
  }
}
```

Committing deny rules to `.claude/settings.json` means every developer gets the same noise reduction without configuring it themselves. Developers who need to work on generated files (code generator authors, for example) can override project-level exclusions in their `settings.local.json`.

---

## Building a codebase map

When the directory structure doesn't clearly signal what lives where — hundreds of top-level folders, legacy naming, or accumulated reorganizations — a lightweight markdown map gives Claude a table of contents it can scan before opening files.

Place it at the repo root and reference it in the root CLAUDE.md:

```markdown
## Finding things

See [CODEBASE_MAP.md](CODEBASE_MAP.md) for a directory-by-directory overview.
```

The map itself should be a simple flat list:

```markdown
# Codebase Map

| Directory | What lives here |
|:---|:---|
| `services/auth` | Authentication and session management |
| `services/payments` | Payment processing, Stripe integration |
| `services/notifications` | Email, SMS, push notification dispatch |
| `libs/shared` | Shared types and utilities used across services |
| `libs/design-system` | Component library |
| `infra/` | Terraform and deployment configuration |
| `scripts/` | One-off migration and maintenance scripts |
| `docs/` | Architecture decision records and runbooks |
```

For codebases with hundreds of top-level folders, use a layered approach: the root map covers only the top level, and each subdirectory CLAUDE.md provides the next level of detail, loading on demand as Claude moves through the tree.

---

## Edge cases where this approach breaks down

The layered CLAUDE.md hierarchy works well for conventional git repositories with standard directory structures. It has limits:

- **Codebases with hundreds of thousands of folders and millions of files** — the hierarchy itself becomes hard to navigate
- **Legacy systems on non-git version control** — Claude's directory traversal assumes git conventions
- **Non-standard directory layouts** — some inherited codebases predate conventions that make directory structure meaningful

For these cases, a codebase map (see above) combined with explicit `@`-mentions of key files or directories at the start of sessions is often more reliable than relying on CLAUDE.md discovery alone.

---

## Related

- [README.md](README.md) — The full harness overview and build sequence
- [skills_and_plugins.md](skills_and_plugins.md) — Moving procedures out of CLAUDE.md and into skills
- [maintenance_and_governance.md](maintenance_and_governance.md) — Keeping CLAUDE.md current as models evolve
- [../CLAUDE_md_templates/](../CLAUDE_md_templates/) — Starting templates
- [../hooks/README.md](../hooks/README.md) — Using stop hooks to propose CLAUDE.md updates automatically

# Maintenance and Governance

A harness built for one model version can work against a newer one. Instructions that guided Claude through patterns it once struggled with may constrain a model that handles those patterns well. Organizations that treat their Claude Code configuration as a living artifact — rather than a one-time setup — consistently see better results over time.

---

## CLAUDE.md maintenance cadence

**Review every three to six months**, and also after major model releases when performance seems to plateau.

The review question is: does this instruction still reflect a real limitation, or is Claude now handling it correctly without the instruction?

Common things that become unnecessary over time:
- Rules telling Claude to break work into single-file changes at a time (newer models coordinate cross-file changes reliably)
- Explicit tool-use instructions the model now infers from context
- Compensations for reasoning patterns that have improved
- Hooks that intercepted behavior now handled natively (example: a hook that enforced `p4 edit` before every file write became redundant once Claude Code added native Perforce mode)

Instructions that no longer reflect model behavior don't just become neutral — they actively constrain Claude in ways that make it less useful. A CLAUDE.md file that accumulates without review becomes a list of rules for a model that no longer exists.

### What to look for in a review

- Instructions that start with "make sure to" or "always" — are these still necessary?
- Multi-step procedures Claude now handles correctly without guidance
- Skill content compensating for model limitations rather than codifying genuine workflow
- Hooks that block or intercept behavior Claude now handles correctly on its own

---

## Ownership models

Technical configuration alone doesn't drive adoption. Organizations that spread Claude Code fastest invested in organizational structure before broad access — a small team wired up the tooling so Claude already fit developer workflows when engineers first touched it.

### The DRI model

For teams without a dedicated AI tooling function, the minimum viable version is a **Directly Responsible Individual (DRI)**: one person with clear ownership over the Claude Code configuration.

The DRI's responsibilities:
- Owns the CLAUDE.md hierarchy and keeps it current
- Makes calls on settings, permissions policy, and plugin marketplace contents
- Reviews and approves new skills and plugins before org-wide distribution
- Tracks model releases and schedules configuration reviews
- Centralizes what works from bottom-up adoption and distributes it to everyone

Without a DRI, bottom-up adoption generates enthusiasm but fragments. Every team reinvents the same skills and hooks. Knowledge stays tribal and adoption plateaus.

### The agent manager role

An emerging role in larger engineering organizations is the **agent manager**: a hybrid PM/engineer function dedicated to managing the Claude Code ecosystem full-time.

This role makes sense when:
- Hundreds or thousands of developers are using Claude Code
- Plugin and skill creation is happening independently across many teams
- Governance questions require dedicated attention (regulated industries, security review requirements)
- The ROI on configuration quality is high enough to justify full-time ownership

The agent manager function typically sits under developer experience or developer productivity — the function already responsible for onboarding and developer tooling.

---

## Governance patterns

### Starting locked down

For regulated industries and large organizations, governance questions come up early: who controls which skills and plugins are available, how do you prevent independent reinvention, how does AI-generated code go through the same review process as human-written code?

A pattern that works: start locked down, expand as confidence builds.

**Initial rollout:**
- [ ] Defined set of approved skills and plugins in a managed marketplace
- [ ] Plugin installation restricted to the approved marketplace
- [ ] AI-generated code subject to the same review requirements as human-written code
- [ ] Limited initial access, expanded to new teams as they complete onboarding

**As confidence builds:**
- [ ] Teams can propose new skills for review and addition to the marketplace
- [ ] Access expands to additional teams and use cases
- [ ] Restrictions loosen based on observed behavior rather than assumption

### Cross-functional working groups

Regulated industries and security-sensitive organizations benefit from establishing a cross-functional working group early — engineering, information security, and governance representatives together, defining requirements and building a rollout roadmap before broad access goes out.

This avoids the pattern where Claude Code reaches developers first, creates strong expectations, and then hits a compliance wall requiring rollback. Front-loading that friction with a working group is cheaper than handling it after the fact.

The working group shouldn't dissolve at launch. Post-deployment realities require ongoing representation from roles that pre-rollout planning groups typically overlook:

| Role | What they bring |
|:---|:---|
| **Support engineer** | First to see failure patterns at scale — what's confusing, what's breaking, what workarounds engineers are inventing on their own |
| **Change manager / L&D** | Owns adoption and training; without this role, engineers use Claude Code as a cargo-cult without understanding why it works |
| **Security operations analyst** | Watches the live environment for anomalies, prompt injection attempts, and unusual code patterns — distinct from InfoSec, which sets policy |
| **Working developer representative** | A practitioner using Claude Code daily who brings ground truth about what's actually happening versus what governance assumes is happening |

Including these roles from the start gives the working group a direct line to the development floor, closer ties to decision makers, and early warning on constraints that only emerge after deployment. Enough enterprise AI rollouts have happened that all four roles can now speak from evidence, not just theory.

### AI-generated code review

AI-generated code should go through the same review process as human-generated code. The author of record is the developer who accepted the change, not Claude. A few practices that help enforce this consistently:

- **No bypassing CI.** Claude should not use `--no-verify` or skip linting hooks. Add a hook in `.claude/settings.json` that blocks these flags deterministically — instructions alone aren't reliable enough for a policy requirement.
- **PR reviews apply.** All code Claude writes goes through the same PR review as code humans write. Committing directly to main is not an exception.
- **Audit logging.** For regulated environments, hook-based logging of what Claude changed, when, and in which session satisfies audit requirements that manual tracking cannot. A `PostToolUse` hook on Write and Edit events captures this automatically.

---

## Related

- [README.md](README.md) — The full harness overview and build sequence
- [claude_md_at_scale.md](claude_md_at_scale.md) — CLAUDE.md hierarchy and what goes where
- [skills_and_plugins.md](skills_and_plugins.md) — Managing plugin marketplaces for distribution and governance
- [../hooks/README.md](../hooks/README.md) — Hooks for audit logging and policy enforcement

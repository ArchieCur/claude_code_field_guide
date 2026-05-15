# Code Review + Auto-fix

Two complementary features for keeping PRs clean without manual effort — Code Review analyzes every PR with a fleet of agents before merge, Auto-fix watches a live PR and responds to CI failures and reviewer comments as they come in.

---

## Code Review

> Research preview — Team and Enterprise plans only. Not available with Zero Data Retention enabled.

### How it works

When a PR opens (or on every push, depending on configuration), multiple agents analyze the diff and surrounding code in parallel on Anthropic infrastructure. Each agent targets a different class of issue. A verification step filters out false positives before results are posted as inline comments on the specific lines where issues were found.

**Severity levels:**

| Marker | Severity | Meaning |
|:---|:---|:---|
| 🔴 | Important | A bug that should be fixed before merging |
| 🟡 | Nit | Minor issue — worth fixing, not blocking |
| 🟣 | Pre-existing | Bug in the codebase not introduced by this PR |

Each finding includes a collapsible reasoning section explaining why Claude flagged it and how it verified the problem. Findings never approve or block a PR — existing review workflows stay intact.

Reviews average 20 minutes and cost $15–25, scaling with PR size and codebase complexity.

### Setup (admin required)

1. Go to [claude.ai/admin-settings/claude-code](https://claude.ai/admin-settings/claude-code) → Code Review section
2. Install the Claude GitHub App on your GitHub organization
   - Permissions required: Contents (read/write), Issues (read/write), Pull requests (read/write)
3. Select repositories to enable
4. Set **Review Behavior** per repo:
   - **Once after PR creation** — runs once when a PR opens
   - **After every push** — runs on every push, auto-resolves threads when issues are fixed
   - **Manual** — only runs when someone explicitly requests it

### Manual triggers

Post these as top-level PR comments (not inline on a diff line):

| Command | What it does |
|:---|:---|
| `@claude review` | Starts a review + subscribes the PR to push-triggered reviews going forward |
| `@claude review once` | Starts a single review without subscribing to future pushes |

Requirements: open PR, owner/member/collaborator access.

### Customizing what gets flagged

**`CLAUDE.md`** — Code Review reads your repo's CLAUDE.md files. Newly introduced violations are flagged as nits. Works at every directory level.

**`REVIEW.md`** — Review-only instructions injected into every agent as highest-priority. Use this to:
- Redefine what 🔴 Important means for your repo
- Cap nit volume (`"report at most five nits"`)
- Skip generated files, lockfiles, or linting categories CI already covers
- Add repo-specific checks (`"new API routes must have an integration test"`)
- Set re-review convergence rules (`"after the first review, suppress new nits"`)

**Example `REVIEW.md`:**

```markdown
# Review instructions

## What Important means here
Reserve Important for findings that would break behavior, leak data,
or block a rollback: incorrect logic, unscoped database queries, PII
in logs or error messages, migrations that aren't backward compatible.
Style, naming, and refactoring suggestions are Nit at most.

## Cap the nits
Report at most five Nits per review. If you found more, say "plus N
similar items" in the summary. If everything is a Nit, lead with
"No blocking issues."

## Do not report
- Anything CI already enforces: lint, formatting, type errors
- Generated files under `src/gen/` and any `*.lock` file

## Always check
- New API routes have an integration test
- Log lines don't include email addresses or user IDs
- Database queries are scoped to the caller's tenant
```

Keep `REVIEW.md` short — length dilutes the rules that matter most. General project context belongs in `CLAUDE.md`.

### Rating findings

Each review comment arrives with 👍 and 👎 already attached. Use them — Anthropic collects reaction counts after the PR merges and uses them to tune the reviewer. Reactions don't trigger a re-review.

### Parsing severity programmatically

The check run's last line is machine-readable:

```bash
gh api repos/OWNER/REPO/check-runs/CHECK_RUN_ID \
  --jq '.output.text | split("bughunter-severity: ")[1] | split(" -->")[0] | fromjson'
# returns: {"normal": 2, "nit": 1, "pre_existing": 0}
```

`normal` = Important findings count. Gate merges on a non-zero value if you want branch protection on Code Review results.

---

## Auto-fix

Auto-fix monitors a live PR and responds automatically to CI failures and review comments. Claude investigates each event and pushes a fix if one is clear.

Requires the Claude GitHub App installed on the repository.

### Activating auto-fix

| Surface | How |
|:---|:---|
| PRs created in Claude Code on the web | Open the CI status bar → select **Auto-fix** |
| Terminal | Run `/autofix-pr` on the PR's branch — Claude detects the open PR, spawns a web session, enables auto-fix |
| Mobile app | Tell Claude: "watch this PR and fix any CI failures or review comments" |
| Any existing PR | Paste the PR URL into a session and tell Claude to auto-fix it |

Auto-fix is a **per-PR toggle**. To stop monitoring: open the CI status bar and clear the Auto-fix toggle, or tell Claude to stop watching the PR.

### How Claude responds

| Event | Claude's response |
|:---|:---|
| Clear fix | Makes the change, pushes it, explains what was done in the session |
| Ambiguous request | Asks you before acting |
| Duplicate or no-action | Notes it in the session and moves on |

Claude may reply to review comment threads on GitHub. Replies appear under your username but are labeled as coming from Claude Code.

> **Warning:** If your repo uses comment-triggered automation (Atlantis, Terraform Cloud, custom Actions on `issue_comment` events), Claude's replies can trigger those workflows. Review your repo's automation before enabling auto-fix on repos where a PR comment can deploy infrastructure or run privileged operations.

---

## Related resources

- [Claude Code on the web](https://code.claude.com/docs/en/claude-code-on-the-web.md) — cloud sessions, environment config
- [GitHub Actions](https://code.claude.com/docs/en/github-actions.md) — self-hosted CI alternative to Code Review
- [Memory](https://code.claude.com/docs/en/memory.md) — how CLAUDE.md works across Claude Code
- [Analytics](https://code.claude.com/docs/en/analytics.md) — track Code Review usage and spend

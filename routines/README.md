# Routines

> Research preview — behavior, limits, and API surface may change.

Put Claude Code on autopilot. A routine is a saved configuration — prompt, repositories, connectors — that runs automatically on Anthropic-managed cloud infrastructure. Your laptop can be closed. The routine keeps running.

Available on Pro, Max, Team, and Enterprise plans with Claude Code on the web enabled.
Manage at [claude.ai/code/routines](https://claude.ai/code/routines) or from the CLI with `/schedule`.

---

## When to use routines

Routines are best for work that is **unattended, repeatable, and tied to a clear outcome**:

- Nightly backlog grooming — label issues, assign owners, post a summary to Slack
- Alert triage — monitoring tool calls the routine when a threshold is crossed; Claude correlates the stack trace with recent commits and opens a draft PR
- Bespoke code review — GitHub trigger runs on `pull_request.opened`, applies your team's checklist, posts inline comments
- Deploy verification — CD pipeline calls the routine after each deploy; Claude runs smoke checks and posts a go/no-go
- Docs drift — weekly scan of merged PRs, flags outdated API references, opens update PRs
- Library port — when a PR merges in one SDK, the routine ports the change to a parallel SDK and opens a matching PR

---

## Create a routine

### From the CLI

```text
/schedule daily PR review at 9am
/schedule clean up feature flag in one week   # one-off run
/schedule list                                # see all routines
/schedule update                              # change an existing routine
/schedule run                                 # trigger immediately
```

`/schedule` creates scheduled routines only. Add API or GitHub triggers from the web at [claude.ai/code/routines](https://claude.ai/code/routines).

### From the web

1. Visit [claude.ai/code/routines](https://claude.ai/code/routines) → **New routine**
2. Name it and write the prompt — the routine runs autonomously, so the prompt must be **self-contained and explicit about what done looks like**
3. Select one or more GitHub repositories (cloned fresh on each run from the default branch)
4. Select a cloud environment (controls network access, env vars, setup scripts)
5. Add one or more triggers (see below)
6. Review connectors — all your MCP connectors are included by default; remove what the routine doesn't need
7. Click **Create**

### Key behavior

- Routines run **fully autonomously** — no permission prompts during a run
- Claude creates `claude/`-prefixed branches by default; enable **Allow unrestricted branch pushes** per-repo if you need Claude to push to existing branches
- Routines belong to your individual account — not shared with teammates
- Commits and PRs appear under your GitHub identity

---

## Trigger types

A routine can combine multiple triggers.

### Schedule trigger

| Preset | Cadence |
|:---|:---|
| Hourly | Every hour |
| Daily | Once per day |
| Weekdays | Monday–Friday |
| Weekly | Once per week |

Times are entered in your local zone and converted automatically.

For a custom interval (every 2 hours, first of each month), use the closest preset then run `/schedule update` in the CLI to set a cron expression. **Minimum interval: 1 hour.**

**One-off runs:** Schedule a routine to fire once at a specific future time. After it fires, the routine auto-disables. Create from the CLI:

```text
/schedule tomorrow at 9am, summarize yesterday's merged PRs
/schedule in 2 weeks, open a cleanup PR removing the feature flag
```

One-off runs don't count against the daily routine run cap.

### API trigger

Gives a routine a dedicated HTTP endpoint. POST to it with a bearer token to start a run on demand — from alerting systems, deploy pipelines, internal tools, or anywhere you can make an authenticated HTTP request.

**Setup:** Add an API trigger from the routine's edit form → copy the URL → click **Generate token** (shown once, store it securely).

**Call the endpoint:**

```bash
curl -X POST https://api.anthropic.com/v1/claude_code/routines/trig_01.../fire \
  -H "Authorization: Bearer sk-ant-oat01-xxxxx" \
  -H "anthropic-beta: experimental-cc-routine-2026-04-01" \
  -H "anthropic-version: 2023-06-01" \
  -H "Content-Type: application/json" \
  -d '{"text": "Sentry alert SEN-4521 fired in prod. Stack trace attached."}'
```

The `text` field is optional freeform context passed to the routine alongside its saved prompt.

**Response:**

```json
{
  "type": "routine_fire",
  "claude_code_session_id": "session_01...",
  "claude_code_session_url": "https://claude.ai/code/session_01..."
}
```

Open the session URL to watch the run in real time.

Each token is scoped to one routine. Rotate or revoke from the same modal.

### GitHub trigger

Starts a run automatically when a matching event occurs on a connected repository. Requires the Claude GitHub App installed on the repo.

**Supported events:**

| Event | Triggers when |
|:---|:---|
| Pull request | PR is opened, closed, assigned, labeled, synchronized, or updated |
| Release | Release is created, published, edited, or deleted |

**Filter pull requests** by: Author, Title, Body, Base branch, Head branch, Labels, Is draft, Is merged.

Filter operators: equals, contains, starts with, is one of, is not one of, matches regex.

> Note: `matches regex` tests the entire field value. To match any title containing `hotfix`, write `.*hotfix.*` — not just `hotfix`.

**Example filter combinations:**

- **Auth module review:** base branch `main` + head branch contains `auth-provider`
- **Ready-for-review only:** is draft = `false`
- **Label-gated backport:** labels include `needs-backport`

Each matching event starts its own independent session.

---

## Manage routines

From a routine's detail page you can:

- **Run now** — trigger immediately without waiting for the next scheduled time
- **Pause/resume** — toggle the schedule on or off without losing configuration
- **Edit** — change prompt, repos, environment, connectors, or any trigger
- **View past runs** — click any run to open it as a full session; review what Claude did, create a PR, or continue the conversation

> A green status means the session started and exited without an infrastructure error — **not** that the task succeeded. Open the run and read the transcript to confirm what actually happened.

---

## Usage and limits

- Routines draw down subscription usage the same way interactive sessions do
- There is a **daily cap** on routine runs per account — check current consumption at [claude.ai/code/routines](https://claude.ai/code/routines)
- One-off runs are exempt from the daily cap
- Organizations with extra usage enabled can continue running routines on metered overage after hitting the cap

---

## Relationship to scheduled_tasks/

The existing `scheduled_tasks/` folder in this repo covers **local** scheduled tasks — prompts that run on your machine via the Desktop app while it's open. Routines are the cloud-based evolution: they run on Anthropic infrastructure, support API and GitHub triggers in addition to schedules, and don't require your machine to be on. For long-running or production automation, routines are the right tool.

---

## Related resources

- [Routines docs](https://code.claude.com/docs/en/routines.md)
- [Desktop scheduled tasks](https://code.claude.com/docs/en/desktop-scheduled-tasks.md) — local alternative
- [Claude Code on the web](https://code.claude.com/docs/en/claude-code-on-the-web.md) — cloud environment config
- [MCP connectors](https://code.claude.com/docs/en/mcp.md) — connect Slack, Linear, etc. to routines

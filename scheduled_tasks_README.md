# Scheduled Tasks

Claude Code can run recurring tasks on a schedule — updating documentation, summarizing open PRs, running nightly tests, or anything you'd otherwise remember to trigger manually.

There are **two distinct systems**. Choosing the wrong one is the most common mistake practitioners make:

| | CLI (`/loop`) | Desktop Tasks |
|--|--------------|---------------|
| **Survives terminal close** | No | Yes |
| **Survives app restart** | No | Yes |
| **Runs unattended** | No | Yes (app must be open) |
| **Best for** | Active dev sessions | Recurring production workflows |
| **Setup** | One command | UI form or natural language |

> **Don't conflate these two systems.** A `/loop` task that seemed to work fine will silently vanish when you close your terminal. If you need a task to run tomorrow, use Desktop.

See the dedicated guides:
- [CLI Scheduled Tasks (session-scoped)](cli.md) — `/loop`, cron expressions, one-shot reminders
- [Desktop Scheduled Tasks (durable)](desktop.md) — persistent tasks, worktree isolation, catch-up behavior

---

## Practitioner Use Cases

These are the six workflows practitioners reach for most often. Each is mapped to the right system.

### 1. Daily PR Standup Prep (Desktop)
Every weekday morning before standup, Claude reviews open PRs and tells you what needs attention.

```
Name: standup-prep
Frequency: Weekdays at 8:30am
Prompt: Review all open pull requests in this repo. For each one, summarize:
        what it does, how long it's been open, and whether it's blocked.
        Format as a bulleted standup briefing.
```

### 2. CI Status Polling During Active Development (CLI)
You kicked off a long build. Instead of switching tabs every few minutes, let Claude poll and tell you when it's done.

```bash
/loop 5m check if the CI pipeline has finished and tell me the result
```
Disappears when you close the terminal — which is fine, because you only needed it for this session.

### 3. Nightly Test Suite (Desktop)
Run your full test suite every night. Claude executes the tests, reads the output, and surfaces any failures with a suggested fix.

```
Name: nightly-tests
Frequency: Daily at 11:00pm
Worktree: Enabled
Permission: Auto accept edits
Prompt: Run the full test suite. If any tests fail, identify the root cause
        and open a draft fix. If all pass, just log "All tests passed."
```

### 4. Weekly Dependency Audit (Desktop)
Every Monday, Claude checks for outdated or vulnerable packages and summarizes what needs updating.

```
Name: dependency-audit
Frequency: Weekly, Monday at 9:00am
Prompt: Check all dependencies for outdated versions and known CVEs.
        Summarize findings by severity. Flag anything critical.
```

### 5. Documentation Freshness Check (Desktop)
Docs drift. Run a weekly check to catch files referencing outdated APIs, removed functions, or stale examples.

```
Name: docs-freshness
Frequency: Weekly, Friday at 4:00pm
Prompt: Review all files in /docs. Flag any that reference functions,
        endpoints, or environment variables that no longer exist in the codebase.
        List specific files and line numbers.
```

### 6. Session-Level Release Checklist (CLI)
You're preparing a release. Have Claude run through a checklist every 30 minutes and tell you what's still incomplete.

```bash
/loop 30m check the release checklist: tests passing, CHANGELOG updated,
version bumped in package.json, no uncommitted changes, and staging deployed
```

---

## Choosing the Right System

```
Do you need this task to run after you close your terminal?
├── No  → Use CLI (/loop)
└── Yes → Use Desktop Tasks
           └── Does your computer need to sleep while this runs?
               ├── No  → Desktop Tasks are fine
               └── Yes → Consider GitHub Actions instead
```

---

## What NOT to Do

- **Don't use `/loop` for anything you need tomorrow.** It will not survive the session.
- **Don't schedule tasks in Ask permission mode without testing first.** The task will stall waiting for your approval, silently doing nothing until you notice.
- **Don't set both day-of-month and day-of-week in a cron expression unless you understand OR logic.** `0 9 15 * 1` fires on the 15th of any month **OR** every Monday — not just "the Monday closest to the 15th."
- **Don't expect exact timing.** Both systems add deterministic jitter (up to 10% of interval, max 15 min). Design prompts that are tolerant of slight timing variance.

---

## Disabling Scheduled Tasks

To disable all scheduling in a session or environment:

```bash
export CLAUDE_CODE_DISABLE_CRON=1
```

This disables `/loop`, all cron tools, and stops any already-scheduled tasks from firing.

---

## Official Docs

- [Scheduled Tasks Overview](https://code.claude.com/docs/en/scheduled-tasks)

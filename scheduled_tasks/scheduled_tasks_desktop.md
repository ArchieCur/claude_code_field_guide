# Desktop Scheduled Tasks (Durable)

Desktop scheduled tasks survive restarts and run independently of any terminal session. They are the right choice for recurring production workflows — daily code reviews, weekly audits, nightly test runs.

> **Requires:** Claude Desktop app (not CLI)

---

## The Core Trade-Off

**Desktop tasks are durable but app-dependent.** They persist across restarts and don't require an active terminal — but the Desktop app must be open and your computer must be awake when the scheduled time arrives.

If you need tasks that run unattended regardless of app state, consider GitHub Actions or a cron daemon instead.

For lightweight session-scoped polling during active development, see [CLI Scheduled Tasks](cli.md).

---

## Creating a Task

### Option 1: UI Form

1. Click **Schedule** in the Desktop app sidebar
2. Click **+ New task**
3. Fill in the fields:

| Field | Notes |
|-------|-------|
| **Name** | Becomes the folder name (auto-converted to `kebab-case`) |
| **Description** | Short summary shown in the task list |
| **Prompt** | Instructions sent to Claude each run — write it like any prompt |
| **Frequency** | Manual, Hourly, Daily, Weekdays, Weekly, or custom |
| **Model** | Select before first run — **locked after** |
| **Permission** | Ask / Auto accept edits / Plan / Bypass |
| **Worktree** | Toggle for Git isolation (each run gets its own worktree) |

### Option 2: Natural Language (in any Desktop session)

```
set up a daily code review that runs every morning at 9am

schedule a task to run all the tests every 6 hours

create a weekly dependency audit every Monday at 9am
```

Claude creates the task and confirms the schedule.

---

## Frequency Options

| Option | Behavior |
|--------|----------|
| Manual | Only runs when you click "Run now" — no automatic schedule |
| Hourly | Every hour (with deterministic offset up to 10 min) |
| Daily | Time picker — defaults to 9:00am local |
| Weekdays | Daily except Saturday and Sunday |
| Weekly | Time + day picker |
| Custom | Describe it in natural language in any Desktop session |

---

## Task Storage

Each task is stored as a `SKILL.md` file on disk:

```
~/.claude/scheduled-tasks/<task-name>/SKILL.md
```

If `CLAUDE_CONFIG_DIR` is set:
```
$CLAUDE_CONFIG_DIR/scheduled-tasks/<task-name>/SKILL.md
```

**File format:**
```yaml
---
name: daily-review
description: Review yesterday's commits each morning
---

Review all commits from the last 24 hours. Summarize what shipped,
flag anything that looks risky, and note any missing tests.
```

**You can edit `SKILL.md` directly.** Changes take effect on the next run. This means you can version-control your task prompts alongside your code.

**What's NOT stored in the file:** Schedule frequency, model selection, and enabled state are stored in the app database. Edit those through the UI or via natural language in a Desktop session.

---

## How Tasks Execute

### Each run is a fresh local session

When the scheduled time arrives, Desktop fires a new independent session. It doesn't interrupt any manual session you have open — it appears as a separate entry under **Scheduled** in the sidebar.

### Worktree Isolation

If you enable the **Worktree** toggle, each run gets its own Git worktree — completely isolated from your main working tree. This means:

- Task changes won't interfere with work you're doing in a manual session
- Multiple task runs can run concurrently without conflicts
- Each run starts from a clean state

Enable worktree for any task that makes code changes. Skip it for read-only tasks (audits, summaries, reviews).

### Deterministic Timing Offset

Each task has a fixed offset of up to 10 minutes after its scheduled time. The offset is derived from the task — so it's always the same. A task you schedule for 9:00am might always run at 9:04am. This is intentional: it staggers API traffic across many users.

**Design implication:** If your prompt references a specific time ("summarize today's standups"), allow for a few minutes of drift.

---

## What Happens When the Computer Sleeps

Tasks only run if the Desktop app is open **and** the computer is awake.

**Default behavior on wake:**
- Desktop checks the past 7 days for missed runs
- For each task with missed runs, it starts exactly **one catch-up run** for the most recent missed time
- Older missed runs are discarded

**Example:** A daily task at 9am that missed 6 days due to sleep will run once on wake — not six times. The catch-up fires for the most recent missed schedule.

**Timing warning:** If your computer sleeps from 10pm to 11pm and wakes at 11pm, a task scheduled for 9am that day will run at 11pm. If your prompt is time-sensitive, add a guard:

```
Only run this review if the current time is before 6pm.
If it's after 6pm, skip and log "Skipped — ran too late."
```

**To prevent sleep during scheduled runs:**
Enable **Keep computer awake** in Settings → Desktop app → General. Note: closing the laptop lid still puts it to sleep regardless of this setting.

---

## Permissions and Stall Prevention

This is one of the most common Desktop task failure modes.

Each task has its own permission mode. If the task is in **Ask** mode and encounters a tool it needs approval for, **the task stalls until you manually approve** — it doesn't fail gracefully, it just waits.

### Prevent Stalls Before They Happen

1. Create the task
2. Click **Run now** to trigger it immediately
3. Watch what permissions it requests
4. Select "Always allow" for each tool it needs
5. Future runs will auto-approve those tools

### View and Revoke Saved Approvals

On the task detail page, under **Always allowed**, you can see every saved tool approval and revoke any you no longer want.

### Recommended Permission Mode by Task Type

| Task Type | Recommended Permission Mode |
|-----------|-----------------------------|
| Read-only (audits, summaries, reviews) | Ask — runs without write access |
| Code changes | Auto accept edits |
| High-trust automation | Bypass (only if you've vetted the prompt fully) |

---

## Managing Tasks

### From the Detail Page

| Action | What It Does |
|--------|-------------|
| Run now | Execute immediately, don't wait for schedule |
| Toggle repeats | Pause or resume without deleting |
| Edit | Change prompt, frequency, folder, or settings |
| Review history | See all past runs, including skipped ones |
| Review always allowed | See and revoke saved tool approvals |
| Delete | Remove task and archive all its sessions |

### Via Natural Language

```
pause my dependency-audit task

delete the standup-prep task

show me my scheduled tasks

what tasks ran yesterday?
```

---

## Full Example: Nightly Test Suite

```
Name: nightly-tests
Description: Run full test suite and flag failures
Frequency: Daily at 11:00pm
Worktree: Enabled
Permission: Auto accept edits
```

**Prompt:**
```
Run the full test suite. Read the output carefully.

If all tests pass: log "All tests passed — [date]" and exit.

If any tests fail:
1. Identify which tests failed and why
2. Check if the failure is in code changed in the last 24 hours
3. Open a draft fix for any failures you're confident about
4. For ambiguous failures, create a GitHub issue with the failure details

Only modify files within the test scope. Do not touch unrelated code.
```

---

## What NOT to Do

- **Don't schedule a task in Ask mode without testing it first with "Run now."** It will silently stall the first time it needs a permission.
- **Don't close the laptop lid and expect tasks to run.** Closing the lid triggers sleep even if "Keep awake" is enabled.
- **Don't change the model after the first run.** The model is locked after first execution.
- **Don't write time-sensitive prompts without a guard clause.** Catch-up runs after sleep can fire hours late. Prompt defensively.
- **Don't assume one catch-up run means "all missed runs."** Only the most recent missed run fires on wake.
- **Don't let tasks accumulate saved permissions you no longer need.** Review the "Always allowed" list periodically.

---

## Official Docs

- [Scheduled Tasks Overview](https://code.claude.com/docs/en/scheduled-tasks)

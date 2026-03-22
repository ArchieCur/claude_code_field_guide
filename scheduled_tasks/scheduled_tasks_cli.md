# CLI Scheduled Tasks (Session-Scoped)

CLI scheduled tasks live inside your active Claude Code session. They are fast to set up and great for active development work. They disappear the moment your terminal closes.

> **Minimum version:** Claude Code v2.1.72+

---

## The Core Trade-Off

**CLI tasks are ephemeral by design.** Every task is tied to the session that created it. This makes them perfect for "watch this while I'm working" automation — and wrong for "run this every day" workflows.

If your task needs to survive a terminal close, see [Desktop Scheduled Tasks](desktop.md) instead.

---

## The `/loop` Skill

`/loop` is the primary way to create repeating tasks in a CLI session. It schedules Claude to re-run a prompt on an interval.

### Basic Syntax

```bash
/loop [interval] <prompt>
```

### Interval Formats

All of these work:

```bash
/loop 5m check if the CI pipeline has finished

/loop check the build every 2 hours

/loop check the build           # defaults to 10 minutes if no interval given
```

**Supported units:** `s` (seconds), `m` (minutes), `h` (hours), `d` (days)

**Note on seconds:** Seconds are rounded up to the nearest minute (cron granularity). `/loop 45s do something` becomes a 1-minute loop. Claude will tell you what interval it actually scheduled.

**Note on non-clean intervals:** Intervals like `7m` or `90m` may be rounded to the nearest clean value. Claude confirms what it picked.

### Invoking Another Slash Command

You can chain `/loop` with another command:

```bash
/loop 20m /review-pr 1234
```

Each time the loop fires, Claude runs `/review-pr 1234` as if you had typed it fresh.

---

## One-Shot Reminders

For one-time future tasks, use natural language:

```bash
remind me at 3pm to push the release branch

in 45 minutes, check whether the integration tests passed
```

These fire once and auto-delete. No management needed.

**Timing note:** One-shot tasks scheduled at `:00` or `:30` get up to 90 seconds of early jitter. If you need a task at exactly 3:00pm, expect it between 2:58:30 and 3:00.

---

## Managing Tasks

### List All Active Tasks

```bash
# Ask Claude directly
what scheduled tasks do I have running?
```

Claude uses `CronList` under the hood and returns a table of task IDs, schedules, and prompts.

### Cancel a Task

```bash
# Ask Claude by description
cancel the CI polling task

# Or by ID (Claude will show IDs when you list tasks)
delete task abc12345
```

### Max Concurrent Tasks

50 tasks per session. In practice you'll rarely need more than 3-5.

---

## Cron Expression Reference

When you use `/loop`, Claude creates the cron expression for you. But if you want direct control, you can give Claude a specific cron expression and it will use it exactly.

**Format:** Standard 5-field vixie-cron

```
minute  hour  day-of-month  month  day-of-week
```

### Common Patterns

```bash
*/5 * * * *       # Every 5 minutes
0 * * * *         # Every hour, on the hour
7 * * * *         # Every hour, at 7 minutes past
0 9 * * *         # Every day at 9am (local time)
0 9 * * 1-5       # Weekdays at 9am
30 14 15 3 *      # March 15 at 2:30pm
```

### Day-of-Week Values

```
0 or 7 = Sunday
1 = Monday
2 = Tuesday
3 = Wednesday
4 = Thursday
5 = Friday
6 = Saturday
```

### What's NOT Supported

```bash
# Name aliases — WRONG
0 9 * * MON       # ❌ Use 1 instead
0 9 * JAN *       # ❌ Use 1 instead

# Extended syntax — NOT SUPPORTED
0 9 L * *         # ❌ L (last day of month) not supported
0 9 15W * *       # ❌ W (nearest weekday) not supported
0 9 * * ?         # ❌ ? not supported
```

### The Day-of-Month + Day-of-Week Gotcha

When both fields are constrained, the expression matches if **either** condition is true (logical OR, not AND):

```bash
0 9 15 * 1        # Fires on the 15th of any month OR every Monday
                  # NOT "the Monday on or nearest the 15th"
```

This is standard vixie-cron behavior. If you want "first Monday of the month," you need a different approach.

### Timezone

All times are **local timezone** — wherever Claude Code is running. `0 9 * * *` means 9am local, not 9am UTC.

---

## Timing Behavior

### Jitter

Tasks don't fire at the exact scheduled time. A deterministic offset is added:

- **Recurring tasks:** fire up to 10% of interval late, capped at 15 minutes
  - Hourly job → fires somewhere between :00 and :06
  - Daily job → fires up to 2.4 hours late
- **One-shot tasks at :00 or :30** → up to 90 seconds early

The offset is derived from the task ID, so the **same task always fires at the same offset** within each interval. It's not random — it's consistent.

**Design implication:** If your prompt is time-sensitive ("check if standup has started"), build in tolerance. If you need the task at exactly 9:00am, don't use CLI tasks — use [Desktop Tasks](desktop.md) with a time picker.

### No Catch-Up

If Claude is busy responding to you when a task was due, the task fires once when Claude becomes idle. **It does not fire multiple times to "make up" for missed intervals.** One fire, then back to the normal schedule.

### 3-Day Expiry

All recurring CLI tasks auto-expire 3 days after creation. The task fires one final time, then deletes itself.

**Why:** Prevents forgotten loops from running (and accumulating API costs) indefinitely.

**To extend:** Cancel and recreate the task before the 3-day mark. Or switch to [Desktop Tasks](desktop.md) for longer-running schedules.

---

## Under the Hood: The Cron Tools

`/loop` is a skill that calls three underlying tools. You'll rarely use these directly, but they're available:

| Tool | What It Does |
|------|-------------|
| `CronCreate` | Creates a task with a 5-field cron expression, prompt, and recurring flag |
| `CronList` | Lists all tasks in the session with IDs, schedules, and prompts |
| `CronDelete` | Cancels a task by its 8-character ID |

---

## What NOT to Do

- **Don't close the terminal and expect the task to keep running.** It will not. All tasks are gone the moment the session ends.
- **Don't use seconds as your interval unit expecting minute precision.** Seconds are rounded up to the nearest minute.
- **Don't schedule 50+ tasks.** The cap is 50 per session and you'll hit diminishing returns well before that.
- **Don't use CLI tasks for overnight or unattended work.** Your laptop will sleep, your terminal will close, or your session will time out. Use [Desktop Tasks](desktop.md).
- **Don't set name aliases (`MON`, `JAN`) in cron expressions.** They're not supported — use numeric values.
- **Don't assume exact timing.** Jitter is real. Write prompts that work whether they fire at 9:00 or 9:05.

---

## Disabling CLI Scheduling

```bash
export CLAUDE_CODE_DISABLE_CRON=1
```

Disables `/loop`, all cron tools, and stops any already-scheduled tasks from firing. Useful in CI environments or when you want to lock down automation.

Can also be set persistently in `~/.claude/settings.json`:

```json
{
  "env": {
    "CLAUDE_CODE_DISABLE_CRON": "1"
  }
}
```

---

## Official Docs

- [Scheduled Tasks Overview](https://code.claude.com/docs/en/scheduled-tasks)

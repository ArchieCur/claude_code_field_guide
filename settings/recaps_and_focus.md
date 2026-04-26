# Recaps and Focus Mode

Two features for managing how much Claude surfaces during a session: **Recaps** summarize what happened after a task; **Focus mode** hides intermediate work while a task runs.

---

## Recaps

Recaps are short summaries Claude generates after completing a task. They capture:
- What the agent did
- What comes next

They are most useful when you step away during a long-running task and return minutes or hours later. Instead of re-reading the full conversation to reorient yourself, you get a concise catch-up at the top.

### Enabling and Disabling

Recaps are on by default. To disable:

```
/config
```

Find the Recaps setting and toggle it off.

### When Recaps Help Most

- Long background tasks (builds, test runs, deep research)
- Running multiple Claude sessions in parallel — a quick way to check the status of each one
- Returning to a session after extended context switching

---

## Focus Mode

Focus mode hides all intermediate work — tool calls, file edits, shell output, thinking — and shows only Claude's final response.

Toggle on or off with:

```
/focus
```

### When to Use Focus Mode

Use focus mode when you trust Claude to run the right commands and make the right edits, and you just want the result. At Opus 4.7's capability level, watching every intermediate step is often noise rather than useful signal.

Leave focus mode off when:
- You are working on something sensitive and want to review each step
- You are debugging a problem and need to follow what Claude is doing
- You are learning a new codebase and want to stay oriented

### Focus Mode vs. Recaps

These two features work at different points in time and work well together:

| Feature | When it applies |
|---|---|
| **Focus mode** | While the task is running — hides intermediate output |
| **Recaps** | After the task completes — summarizes what happened |

Turn on focus mode to remove the noise during execution, and let recaps give you the summary when Claude is done.

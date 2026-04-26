# /go

Prompt Claude to verify its work, clean it up, and open a pull request — in one shot.

## What /go Does

When you append `/go` to a prompt, Claude will:

1. **Test end to end** — runs the code using bash, browser automation, or computer use depending on the task
2. **Run /simplify** — reviews the changed code for quality, redundancy, and efficiency, then fixes what it finds
3. **Open a pull request** — commits the work and creates a PR with a clear title and description

## Usage

Append it to any task prompt:

```
Add a CSV export button to the reports page /go
Refactor the auth module to use the new session API /go
Fix the off-by-one error in the pagination logic /go
```

Claude treats `/go` as a signal that you want a complete, verified, production-ready result — not a draft to review.

## Why Verification Matters

Giving Claude a way to verify its own work consistently produces better output — roughly 2–3x improvement for complex tasks. This is especially true with Opus 4.7, which can run extended reasoning loops and catch its own mistakes before surfacing results.

For long-running work, verification also means that when you come back to a task, you know the code works. You do not have to wonder whether Claude finished cleanly or left something half-done.

Verification looks different depending on the task:

| Task type | How Claude verifies |
|---|---|
| Backend | Starts the server, hits the endpoint end to end |
| Frontend | Uses the Claude Chromium extension to control a browser |
| Desktop apps | Uses computer use to interact with the UI directly |
| CLI tools | Runs the tool with representative inputs via bash |

## Installation

Save this file to:
- `~/.claude/commands/go.md` — available in all projects
- `.claude/commands/go.md` — available in this project only

## The Prompt

```
Test this work end to end using bash, browser automation, or computer use as
appropriate for the task. Then run /simplify to review and clean up the changed
code. Then open a pull request with a clear title and description.
```

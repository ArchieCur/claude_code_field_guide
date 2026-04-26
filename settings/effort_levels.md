# Effort Levels

Opus 4.7 replaces fixed thinking budgets with **adaptive thinking** — the model decides how much reasoning a task needs. You influence this with the `/effort` command.

## Setting Your Effort Level

```
/effort [low | medium | high | xhigh | max]
```

The five levels trade speed and cost against intelligence and capability:

| Level | Speed | Cost | Best for |
|---|---|---|---|
| `low` | Fastest | Lowest | Simple edits, quick answers, renaming |
| `medium` | Fast | Low | Routine tasks |
| `high` | Moderate | Moderate | Most day-to-day work |
| `xhigh` | Slower | Higher | Complex features, refactors, debugging |
| `max` | Slowest | Highest | The hardest problems |

## Stickiness

Most effort levels are **sticky** — they persist across sessions until you change them. The exception is `max`, which applies only to your current session and resets afterward.

| Level | Persists across sessions? |
|---|---|
| low / medium / high / xhigh | Yes |
| max | No — current session only |

## Practical Guidance

- **xhigh** is a strong default for serious work. It gets you most of the capability of `max` without the cost, and it sticks so you do not have to reset it each session.
- **max** is for your hardest problems — architectural decisions, tricky bugs, complex refactors where you want every bit of reasoning the model can give.
- **low / medium** are worth using for lightweight tasks (simple edits, answering questions, generating boilerplate) to keep costs down.

## vs. Thinking Budgets

Earlier Claude models used explicit **thinking budgets** — a token limit on internal reasoning you set via the API. Opus 4.7 uses **adaptive thinking** instead: the model scales its reasoning to the task automatically. `/effort` steers how aggressively it does so. You get the benefits of extended thinking without managing token counts.

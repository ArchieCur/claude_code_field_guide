# Managed Agents API

> Research preview — requires the `managed-agents-2026-04-01` beta header on all requests. The SDK sets this automatically.

The Managed Agents API is Anthropic's programmatic layer for running agents in production. Where Claude Code CLI is optimized for interactive developer sessions, the Managed Agents API is optimized for **autonomous, long-running, programmatically controlled work** — the kind you'd build into a product or pipeline.

All four features below build on the same foundation: **sessions** (persistent, isolated agent runs you control via API).

---

## When to reach for the Managed Agents API

Use the Managed Agents API when you need:

- **Programmatic control** — trigger agents from your own code, not a terminal
- **Production pipelines** — agents embedded in products, not dev workflows
- **Multi-agent orchestration at scale** — coordinator/worker patterns via API
- **Defined quality bars** — agents that self-evaluate and iterate until a rubric is met
- **Memory hygiene at scale** — clean up and consolidate agent memory across many sessions
- **Event-driven integration** — webhooks instead of polling for agent state changes

For interactive development work, Claude Code CLI (and Routines for automation) is the right tool. The Managed Agents API is what you build *on top of* when you're shipping agent capabilities to others.

---

## Multi-agent sessions

Coordinate multiple agents within a single session. One agent acts as the **coordinator**; it delegates to agents in its roster via a shared tool (`agent_toolset_20260401`). Each agent runs in its own **session thread** with an isolated context window.

All agents share the same container and filesystem. The coordinator reports activity on the **primary thread**; sub-agent threads are spawned at runtime.

**Configure a coordinator:**

```python
coordinator = client.beta.agents.create(
    name="Engineering Lead",
    model="claude-opus-4-7",
    system="Coordinate engineering work. Delegate code review to the reviewer agent.",
    tools=[{"type": "agent_toolset_20260401"}],
    multiagent={
        "type": "coordinator",
        "agents": [
            {"type": "agent", "id": reviewer_agent.id},
            {"type": "agent", "id": test_writer_agent.id},
        ],
    },
)
```

**Patterns that work well:**

- **Parallelization** — fan out independent subtasks, coordinator synthesizes
- **Specialization** — route to agents with domain-focused system prompts (security agent, docs agent)
- **Escalation** — consult a more capable model for a subset of complex subtasks (→ Advisor strategy)

Max 20 unique agents in a coordinator's roster. Max 25 concurrent threads per session.

Full docs: [Multiagent sessions](https://code.claude.com/docs/en/managed-agents/multi-agent)

---

## Outcomes

Tell the agent what "done" looks like. The agent works toward that target, self-evaluating and iterating until the outcome is met or max iterations is reached.

When you define an outcome, the harness provisions a **grader** in a separate context window — independent from the main agent's implementation choices — which evaluates the artifact against a rubric and returns a per-criterion breakdown.

**Create a session with an outcome:**

```python
session = client.beta.sessions.create(
    agent=agent.id,
    environment_id=environment.id,
    title="Financial analysis on Costco",
)

client.beta.sessions.events.send(
    session_id=session.id,
    events=[{
        "type": "user.define_outcome",
        "description": "Build a DCF model for Costco in .xlsx",
        "rubric": {"type": "text", "content": RUBRIC},
        "max_iterations": 5,  # default 3, max 20
    }],
)
```

**Grader results:**

| Result | What happens next |
|:---|:---|
| `satisfied` | Session transitions to idle |
| `needs_revision` | Agent starts a new iteration |
| `max_iterations_reached` | Agent may run one final revision, then idles |
| `failed` | Rubric fundamentally doesn't match the task |
| `interrupted` | User sent an interrupt event |

**Writing effective rubrics:** Use explicit, gradeable criteria — "The CSV contains a price column with numeric values" not "The data looks good." Structure as markdown with per-criterion sections. If you don't have a rubric, give Claude a known-good example artifact and ask it to analyze what makes it good, then turn that into a rubric.

Outcomes can be chained: send a new `user.define_outcome` event after the terminal event of the previous outcome. Only one outcome runs at a time.

Full docs: [Define outcomes](https://code.claude.com/docs/en/managed-agents/define-outcomes)

---

## Dreams

Let Claude clean up and consolidate an agent's memory store using past session transcripts.

Over many sessions, a memory store accumulates duplicates, contradictions, and stale entries. A **dream** reads an existing memory store alongside past session transcripts and produces a new, reorganized store: duplicates merged, stale entries replaced, new insights surfaced.

The input store is never modified — you review the output and decide whether to use it or discard it.

Requires an additional beta header: `dreaming-2026-04-21`

**Create a dream:**

```python
dream = client.beta.dreams.create(
    inputs=[
        {"type": "memory_store", "memory_store_id": store_id},
        {"type": "sessions", "session_ids": [session_a, session_b]},
    ],
    model="claude-opus-4-7",
    instructions="Focus on coding-style preferences; ignore one-off debugging notes.",
)
```

Dreams run asynchronously — poll for status:

```python
while dream.status in ("pending", "running"):
    time.sleep(10)
    dream = client.beta.dreams.retrieve(dream.id)

# When completed, outputs[] contains the new memory store
output_store_id = next(
    o.memory_store_id for o in dream.outputs if o.type == "memory_store"
)
```

**Supported models:** `claude-opus-4-7`, `claude-sonnet-4-6`
**Max sessions per dream:** 100
**Billing:** Standard token rates for the selected model

Full docs: [Dreams](https://code.claude.com/docs/en/managed-agents/dreams)

---

## Webhooks

Get notified when major session events happen without polling the API.

Register an endpoint at **Manage > Webhooks** in [Console](https://platform.claude.com/settings/workspaces/default/webhooks). Each delivery carries an `X-Webhook-Signature` header — use the SDK's `unwrap()` helper to verify and parse in one step.

**Session events:**

| Event | Trigger |
|:---|:---|
| `session.status_run_started` | Agent execution kicked off |
| `session.status_idled` | Agent awaiting input |
| `session.status_rescheduled` | Transient error, session retrying |
| `session.status_terminated` | Session hit a terminal error |
| `session.thread_created` | New multiagent thread opened |
| `session.outcome_evaluation_ended` | One iteration of outcome evaluation completed |

**Verify and handle (Python example):**

```python
from flask import Flask, request
import anthropic

client = anthropic.Anthropic()  # reads ANTHROPIC_WEBHOOK_SIGNING_KEY from env
app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        event = client.beta.webhooks.unwrap(
            request.get_data(as_text=True),
            headers=dict(request.headers),
        )
    except Exception:
        return "invalid signature", 400

    if event.data.type == "session.status_idled":
        session = client.beta.sessions.retrieve(event.data.id)
        # handle the idled session

    return "", 200
```

**Delivery behavior:**
- Ordering is not guaranteed — use `created_at` to sort if it matters
- Anthropic retries at least once; same `event.id` = retry, safe to discard
- Redirects (`3xx`) are treated as failures
- Endpoint auto-disables after ~20 consecutive failed deliveries

Full docs: [Subscribe to webhooks](https://code.claude.com/docs/en/managed-agents/subscribe-to-webhooks)

---

## Coming to the claude_api_cookbook

The Managed Agents API features above — multi-agent sessions, outcomes, dreams, and webhooks — will be documented with full working code examples in the [claude_api_cookbook](https://github.com/ArchieCur/claude_api_cookbook/tree/main/managed_agents) repo. This file is an orientation guide; the cookbook is where the deep implementation patterns live.

---

## Required headers

Every Managed Agents API request needs:

```
anthropic-beta: managed-agents-2026-04-01
```

Dreams additionally require:

```
anthropic-beta: managed-agents-2026-04-01,dreaming-2026-04-21
```

The SDK sets these automatically when using the `client.beta.*` namespace.

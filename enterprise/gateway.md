# Gateway Setup for Enterprise

A gateway is a proxy your organization runs between Claude Code and a model provider. Developers authenticate to the gateway rather than holding provider credentials directly. Authentication, usage tracking, budgets, and audit logging happen in one controlled place. In regulated industries or multi-team deployments, the gateway is infrastructure — not optional.

---

## Choose your gateway

Present both options neutrally — neither is a default recommendation over the other.

**Claude apps gateway** — Anthropic's self-hosted gateway, built into the `claude` binary. No separate product to deploy or maintain. Routes to Amazon Bedrock, Google Cloud, Microsoft Foundry, or the Anthropic API. Developers sign in via browser SSO through `/login`; the gateway enforces model access and managed settings by IdP group. Emits OpenTelemetry Protocol (OTLP) usage metrics to your own observability stack. Releases with the CLI so forwarding rules stay current automatically.
Reference: https://code.claude.com/docs/en/claude-apps-gateway

**Other LLM gateways** — If your org already runs an LLM or API gateway, Claude Code works with it. Forwarding rules must be kept current as Claude Code releases new headers and request fields with each version. Anthropic does not endorse, maintain, or audit third-party gateway products.
Reference: https://code.claude.com/docs/en/llm-gateway

---

## How credentials work

Two credential types:

- **Developer credential** — each developer holds their own, issued by the gateway. Authenticates them to the gateway and identifies them in usage tracking.
- **Provider credential** — the gateway holds one credential for the org's provider account, shared across all forwarded traffic. Developers never touch provider credentials directly.

---

## CI pipelines and remote machines

Claude apps gateway authentication is browser SSO only. CI pipelines have no developer to approve a sign-in and cannot authenticate through the gateway. Configure CI pipelines to authenticate directly to your provider.

Agent SDK sessions and `claude -p` runs on a machine where a developer has already signed in use that machine's gateway session and are governed by its policies.

---

## Subscription billing behavior

When developers connect through a gateway with a gateway credential, usage is billed to the org's provider account at API rates. Their personal claude.ai subscriptions are not used or charged. Gateway credential turns off subscription login for that session. Communicate this to developers before rollout — it is a common source of confusion.

**Exception:** If only `ANTHROPIC_BASE_URL` is set with no gateway credential, requests route through the gateway but the saved claude.ai login stays active and subscription billing applies.

---

## What the gateway does not control

- **Model selection** — developers pick the model with `/model` or model environment variables. Claude apps gateway can bound the choice with a per-group `availableModels` allowlist, but the developer selects within it.
- **Corporate HTTP proxies** — an `HTTPS_PROXY` sits between Claude Code and every server including the gateway. Configure the proxy separately. For Claude apps gateway, sign-in checks that the proxy host is on a private network — if it isn't, add the gateway host to `NO_PROXY`.
- **Non-API traffic** — Claude Code sends version checks and downloads directly to Anthropic, separate from the gateway path.

---

## Checklist

- [ ] Decide: Claude apps gateway or existing LLM gateway
- [ ] Deploy gateway and connect to your IdP
- [ ] Configure per-group model allowlists and managed settings
- [ ] Set up OTLP telemetry export to your observability stack
- [ ] Verify required domains are reachable or set `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC`
- [ ] Configure CI pipelines to authenticate directly to your provider — not through the gateway
- [ ] Brief developers on credential and billing behavior before rollout
- [ ] Add gateway host to `NO_PROXY` if your corporate proxy is not on a private network

---

## Related

- [README.md](README.md) — The full harness overview and build sequence
- [maintenance_and_governance.md](maintenance_and_governance.md) — Governance patterns for regulated industries
- [../hooks/README.md](../hooks/README.md) — Hook scripts for automation and enforcement
- https://code.claude.com/docs/en/claude-apps-gateway
- https://code.claude.com/docs/en/llm-gateway
- https://code.claude.com/docs/en/admin-setup

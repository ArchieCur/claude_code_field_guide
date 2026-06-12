# Workflow Recipes

Copy-paste prompts for common workflow scenarios. Each triggers Claude to write and run an appropriate workflow script for the task. Once a run does what you want, press `s` in `/workflows` to save it as a reusable `/<name>` command.

---

## Codebase audits

**Security — missing auth checks**
```text
ultracode: audit every API endpoint under src/routes/ for missing authentication and authorization checks. Flag endpoints that are publicly accessible but should require auth, and ones where the auth check can be bypassed. Have independent agents verify each finding before it's included. Group final findings by severity.
```

**Dependency audit**
```text
ultracode: scan every package imported across the codebase for known vulnerabilities, outdated major versions, and packages with better-maintained alternatives. Cross-check findings across agents before reporting.
```

**Dead code sweep**
```text
ultracode: find all functions, classes, and exports in src/ that are defined but never referenced anywhere in the project. Exclude test files and type declarations. Have agents verify each finding independently before including it in the report.
```

**Error handling gaps**
```text
ultracode: audit every async function in src/ for missing error handling — unhandled promise rejections, missing try/catch around awaited calls, and errors silently swallowed in catch blocks. Group by file and flag the highest-risk gaps first.
```

---

## Large migrations

**Test framework migration**
```text
ultracode: migrate all test files in tests/ from Jest to Vitest. Assign each subdirectory to a separate agent. Each agent changes only the imports, configuration, and Jest-specific APIs (jest.fn → vi.fn, jest.mock → vi.mock, jest.spyOn → vi.spyOn) without touching any test logic.
```

**TypeScript strict mode**
```text
ultracode: enable TypeScript strict mode across the codebase. Assign each top-level directory to a separate agent. Each agent fixes only the strict-mode errors in its assigned directory without touching unrelated code.
```

**CSS-in-JS to CSS modules**
```text
ultracode: migrate all styled-components in src/components/ to CSS modules. Each agent handles a separate component directory. Preserve all existing class names and styles exactly — change only the import mechanism and syntax.
```

---

## Cross-checked research

**Architectural decision**
```text
ultracode: research the tradeoffs between [Option A] and [Option B] for [our use case]. Have independent agents investigate each option in depth, then a cross-checking agent review both sets of findings for contradictions or gaps before synthesizing a final recommendation.
```

**Library evaluation**
```text
/deep-research Compare [library A] and [library B] for [use case]. Cover: API ergonomics, bundle size, TypeScript support, maintenance activity in the last 12 months, and known limitations with [our tech stack]. Cross-check claims across sources.
```

**Breaking change impact**
```text
ultracode: assess the full impact of removing [API or feature]. Fan out across every consumer in the codebase, identify all call sites and their callers, then cross-check findings before producing a migration guide with effort estimates.
```

---

## Multi-angle planning

**Refactor from several angles**
```text
ultracode: draft a plan to refactor [module or system] to [goal]. Have three agents each produce an independent plan, then a fourth agent critique all three for risks and blind spots. Synthesize the strongest elements into a final recommendation.
```

**Pre-mortem on a proposed change**
```text
ultracode: run a pre-mortem on the proposed change in [PR/branch/description]. Have one agent argue for the change, one against, and one focused exclusively on what could go wrong in production. Synthesize the risks into a prioritized list.
```

---

## Saving a recipe as a command

After a run completes:

1. Run `/workflows`
2. Select the completed run
3. Press `s`
4. `Tab` to choose save location:
   - `.claude/workflows/` — shared with your team (committed to the repo)
   - `~/.claude/workflows/` — personal, available in every project
5. Press Enter

The workflow becomes available as `/<name>` in any future session from that location. Project workflows take precedence over personal ones with the same name.

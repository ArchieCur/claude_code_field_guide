Review the current branch diff against main (or master) as a thorough senior engineer would.

Run: `git diff main...HEAD` (or `git diff master...HEAD` if main doesn't exist)

Evaluate the changes across these dimensions:

**Correctness**
- Are there logical errors or edge cases not handled?
- Could any of these changes cause regressions?

**Security**
- Any SQL injection, XSS, command injection, or path traversal risks?
- Are secrets or credentials handled safely?
- Are inputs validated at system boundaries?

**Code Quality**
- Is anything unnecessarily complex that could be simplified?
- Is there duplicated logic that should be extracted?
- Are error cases handled appropriately?

**Tests**
- Are new features covered by tests?
- Do the tests actually verify behavior, or just that the code runs?

**Documentation**
- Would a new team member understand what changed and why?

Format your response as a prioritized list:
- **Must fix** — issues that should block this PR
- **Should fix** — important but not blocking
- **Consider** — suggestions for improvement

If $ARGUMENTS is provided, focus the review on that specific area: $ARGUMENTS

Generate a standup update based on recent git activity.

Run: `git log --oneline --since="yesterday" --author="$(git config user.name)"`

If that returns nothing, try: `git log --oneline -10`

Format the output as a standup update:

**Yesterday / Recent:**
[Summarize the commits in plain language — what was actually accomplished, not just the commit messages verbatim]

**Today:**
[Based on any open work visible in `git status` or recent incomplete commits, suggest what the logical next steps are]

**Blockers:**
[Note anything that looks stuck, broken, or in an incomplete state — uncommitted changes, failing tests, merge conflicts]

Keep it concise. This should take 60 seconds to read aloud.

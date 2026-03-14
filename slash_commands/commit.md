Look at the current git diff (staged and unstaged changes). Then:

1. Stage all modified and new files that are relevant to the current work (use `git add` for specific files — do not `git add -A` blindly)
2. Write a commit message following the Conventional Commits format:
   - `feat:` for new features
   - `fix:` for bug fixes
   - `refactor:` for code changes that don't add features or fix bugs
   - `docs:` for documentation only
   - `test:` for adding or updating tests
   - `chore:` for tooling, config, dependencies
3. Keep the subject line under 72 characters
4. If the change is non-trivial, add a short body paragraph explaining *why*, not just *what*
5. Create the commit

Do not push. Do not amend previous commits. If there is nothing to commit, say so.

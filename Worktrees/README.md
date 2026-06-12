# Worktrees

A git worktree is a separate working directory with its own files and branch, sharing the same repository history as your main checkout. Running each Claude Code session in its own worktree means edits in one session never touch files in another until you commit.

Worktrees handle file isolation. [Agent teams](../agent_teams/), [dynamic workflows](../Dynamic_Workflows/), and [Desktop parallel sessions](../Claude_Code_Desktop/) each use them for different coordination styles. See [Run Agents in Parallel](../README.md#run-agents-in-parallel) to compare all approaches.

---

## Start Claude in a worktree

Pass `--worktree` or `-w` to create an isolated worktree and start Claude in it. A new branch named `worktree-<value>` is created under `.claude/worktrees/<value>/` at your repo root:

```bash
claude --worktree feature-auth
```

Run the command again with a different name in a second terminal for a second isolated session:

```bash
claude --worktree bugfix-123
```

Omit the name and Claude generates one:

```bash
claude --worktree
```

Add `.claude/worktrees/` to your `.gitignore` so worktree contents don't appear as untracked files in your main checkout:

```text
.claude/worktrees/
```

You can also ask Claude to "work in a worktree" mid-session — it creates one with the `EnterWorktree` tool. Once in a worktree, Claude can switch directly to another one under `.claude/worktrees/` without exiting.

> Before using `--worktree` for the first time in a directory, accept the workspace trust dialog by running `claude` once in that directory. Non-interactive runs with `-p` skip the trust check.

---

## Choose the base branch

Worktrees branch from your repository's default branch (`origin/HEAD`) by default — a clean tree matching the remote. To always branch from your current local `HEAD` instead (useful when subagents need in-progress work), set `worktree.baseRef` in your settings:

```json
{
  "worktree": {
    "baseRef": "head"
  }
}
```

To branch from a specific pull request, pass the PR number or full GitHub URL:

```bash
claude --worktree "#1234"
```

For full control over how worktrees are created, configure a `WorktreeCreate` hook, which replaces the default `git worktree` logic entirely.

---

## Copy gitignored files into worktrees

Worktrees are fresh checkouts, so untracked files like `.env` aren't present. To copy them automatically when a worktree is created, add a `.worktreeinclude` file to your project root using `.gitignore` syntax. Only files that match and are also gitignored are copied — tracked files are never duplicated.

```text .worktreeinclude
.env
.env.local
config/secrets.json
```

This applies to `--worktree` sessions, subagent worktrees, and Desktop parallel sessions.

---

## Isolate subagents with worktrees

Ask Claude to "use worktrees for your agents" for one-off isolation, or set it permanently on a custom subagent by adding `isolation: worktree` to its frontmatter:

```markdown
---
name: feature-builder
isolation: worktree
---
```

Each subagent gets a temporary worktree removed automatically when it finishes without changes. Subagent worktrees use the same `baseRef` setting as `--worktree`.

---

## Clean up

| Situation | What happens |
|:---|:---|
| No uncommitted changes, no untracked files, no new commits | Worktree and branch removed automatically on exit |
| Uncommitted changes or new commits exist | Claude prompts to keep or remove |
| Named session with no changes | Claude prompts instead of auto-removing, so you can return later |
| Non-interactive runs (`-p`) | Not cleaned up automatically — remove with `git worktree remove` |

Subagent worktrees older than your `cleanupPeriodDays` setting are swept automatically, provided they have no uncommitted changes or unpushed commits. Worktrees created with `--worktree` are never removed by the sweep.

To clean up a worktree manually:

```bash
git worktree remove .claude/worktrees/feature-auth
# add --force if uncommitted changes or untracked files exist
```

---

## Manage worktrees manually

For full control over location and branch configuration, create worktrees directly with Git. Useful when you need an existing branch or a location outside the repository:

```bash
# Create on a new branch
git worktree add ../project-feature-a -b feature-a

# Create from an existing branch
git worktree add ../project-bugfix bugfix-123

# Start Claude in the worktree
cd ../project-feature-a && claude

# List all worktrees
git worktree list

# Remove when done
git worktree remove ../project-feature-a
```

Remember to initialize your development environment in each new worktree: install dependencies, set up virtual environments, or run your project's setup script.

---

## Non-git version control

For SVN, Perforce, Mercurial, or other systems, configure `WorktreeCreate` and `WorktreeRemove` hooks to replace the default git behavior. The hook reads the worktree name from stdin and prints the directory path so Claude Code uses it as the session's working directory:

```json
{
  "hooks": {
    "WorktreeCreate": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "bash -c 'NAME=$(jq -r .name); DIR=\"$HOME/.claude/worktrees/$NAME\"; svn checkout https://svn.example.com/repo/trunk \"$DIR\" >&2 && echo \"$DIR\"'"
          }
        ]
      }
    ]
  }
}
```

Pair with a `WorktreeRemove` hook for cleanup. Because the hook replaces the default git logic, `.worktreeinclude` is not processed — copy local config files inside your hook script instead.

---

## Related resources

- [Worktrees docs](https://code.claude.com/docs/en/worktrees.md)
- [Run agents in parallel](../README.md#run-agents-in-parallel) — compare all parallel approaches
- [Agent teams](../agent_teams/) — worktrees + peer session coordination
- [Dynamic workflows](../Dynamic_Workflows/) — worktrees + script-driven orchestration at scale
- [Desktop parallel sessions](../Claude_Code_Desktop/) — automatic worktrees per session in the desktop app

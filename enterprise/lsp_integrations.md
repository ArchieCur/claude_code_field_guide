# LSP Integrations

Language Server Protocol (LSP) integrations give Claude the same code navigation a developer has in their IDE: go to definition, find all references, rename symbol. Without LSP, Claude pattern-matches on text. With LSP, it navigates by symbol.

The difference matters most in large codebases where common names appear thousands of times. Grep for a method called `process` in a million-line codebase returns noise. LSP returns only the references that actually point to the same symbol.

---

## What LSP gives Claude

| Without LSP | With LSP |
|:---|:---|
| Text search returns all string matches | Symbol lookup returns only matching references |
| Can't distinguish `process` in Python from `process` in Go | Understands language and type boundaries |
| Opens many files to determine which match is relevant | Filters before reading |
| Burns context on false positives | Uses context only on actual references |

This matters most for:
- **Large codebases** where common names produce thousands of text matches
- **Compiled languages** (C, C++, Go, Java) where symbol resolution requires understanding types, not just strings
- **Multi-language codebases** where the same name exists in different language files with different meanings

One deployment pattern that works well: installing LSP integrations org-wide before a broad Claude Code rollout, specifically to make navigation reliable from day one rather than discovering search quality problems later.

---

## Setup

All official LSP plugins are Anthropic-verified and available in the built-in marketplace. Browse them at [claude.com/plugins](https://claude.com/plugins) (filter for Claude Code, search "LSP") or from within Claude Code via `/plugin` → Discover tab.

The install pattern is:

```bash
/plugin install <name>@claude-plugins-official
```

As of May 2026, the following LSP plugins are available from the official marketplace:

| Plugin | Language(s) |
|:---|:---|
| TypeScript LSP | TypeScript, JavaScript |
| Pyright LSP | Python |
| C# LSP | C# |
| Go LSP (gopls) | Go |
| Rust Analyzer LSP | Rust |
| Java LSP (Eclipse JDT.LS) | Java |
| PHP LSP | PHP |
| Clangd LSP | C, C++ |
| Swift LSP | Swift |
| Kotlin LSP | Kotlin |
| Lua LSP | Lua |
| Ruby LSP | Ruby |
| liquid-lsp | Shopify Liquid |

Browse the marketplace for the exact install slug for each plugin — display names and install identifiers may differ. If a plugin install fails with "not found," run `/plugin marketplace update claude-plugins-official` to refresh the index, then retry.

Each plugin requires the corresponding language server binary to be installed on your machine. The plugin connects Claude to the binary you already have — it doesn't bundle the server itself.

Most large-codebase IDEs already have an LSP running for "go to definition" and "find all references." Surfacing that same server to Claude requires only the plugin install and confirming the binary is on your PATH.

---

## Custom LSP plugins for unsupported languages

For languages not covered by official plugins, add an `.lsp.json` file to a custom plugin:

```json
{
  "go": {
    "command": "gopls",
    "args": ["serve"],
    "extensionToLanguage": {
      ".go": "go"
    }
  }
}
```

Place `.lsp.json` at the plugin root alongside your `plugin.json` manifest. Users installing the plugin must have the language server binary installed on their machine.

See the [Plugins docs](https://code.claude.com/docs/en/plugins) for the complete `.lsp.json` schema.

---

## When to prioritize LSP

**Prioritize immediately:**
- C and C++ codebases — text search is particularly unreliable for these languages due to preprocessor macros, namespacing, and overloading
- Codebases over ~500K lines where grep output volumes become unmanageable
- Multi-language repositories where the same symbol name appears in different languages with different meanings
- Any codebase where Claude consistently opens wrong files or mistakes identically-named symbols

**Can wait:**
- Small to medium codebases in dynamic languages where text search is usually precise enough
- Prototypes and single-developer projects where context window pressure is low

---

## Verifying it's working

Once a language server plugin is installed, ask Claude to navigate by definition rather than by string:

```
Find all call sites of the `processPayment` function — use go-to-definition, not grep.
```

If Claude traces references through the symbol graph and reports a specific count, LSP is working. If it falls back to searching by filename or grep pattern, the language server binary may not be on your PATH or the plugin may not be loading.

Run `/doctor` to diagnose plugin load issues after an upgrade or new install.

---

## Related

- [README.md](README.md) — The full harness overview and build sequence
- [skills_and_plugins.md](skills_and_plugins.md) — Creating custom plugins, including custom LSP plugins
- [Official plugin marketplace](https://claude.com/plugins) — Browse and install all Anthropic-verified LSP plugins (filter: Claude Code, search: LSP)

# LibSkills — Best Practices

## For AI Agents: Always follow this workflow

```
Step 1: Identify library → Step 2: libskills find <library> → Step 3: libskills get <key>
→ Step 4: Read pitfalls.md + safety.md → Step 5: Generate code
```

## Use `find` over `search`

`find` searches the actual skill content (TF-IDF), not just metadata. It gives better results for natural language queries.

## Cache skills you use often

```bash
libskills get cpp/gabime/spdlog
libskills get rust/tokio-rs/tokio
# These are now available offline
```

## Run `lint --fix` before `validate`

```bash
libskills lint --fix .libskills/  # auto-repair first
libskills validate .libskills/    # then check compliance
```

## Use the MCP server for AI IDE integration

The CLI is for humans. The MCP server is for AI IDEs. Both use the same skill data.

```json
{
  "mcpServers": {
    "libskills": {
      "command": "libskills-mcp"
    }
  }
}
```

## Check skill freshness before relying on it

```bash
libskills info cpp/gabime/spdlog | grep Updated
# → Updated: 2026-04-28  (fresh)
# → Updated: 2025-01-15  (stale — library may have changed)
```

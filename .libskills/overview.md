# LibSkills — Overview

**LibSkills** is a standard and CLI tool that gives AI agents pre-compiled knowledge about open-source libraries — specifically, *where each library will break*. Libraries ship a `.libskills/` directory. AI agents read it before generating code.

## What This Skill Teaches You

This is a **meta-skill** — it teaches AI agents how to use LibSkills itself to discover skills for other libraries.

**Core loop:** `install → update → find → get → read → generate correct code`

## When to Use LibSkills

- You (the AI agent) are about to generate code that uses a library you're unfamiliar with
- You want to avoid hallucinating APIs, misusing thread safety, or ignoring lifecycle constraints
- You need to know the *pitfalls* of a library, not just its API documentation

## How It Works

```
1. Install:   curl -fsSL https://raw.githubusercontent.com/LibSkills/LibSkills/main/install.sh | bash
2. Update:    libskills update
3. Find:      libskills find "fast C++ logging"
4. Get:       libskills get cpp/gabime/spdlog
5. Read:      cat ~/.libskills/cache/cpp/gabime/spdlog/pitfalls.md
6. Generate:  Write code that avoids the documented pitfalls
```

## Available Skills (6)

| Library | Language | Category |
|---------|----------|----------|
| spdlog | C++ | Logging |
| {fmt} | C++ | Formatting |
| serde | Rust | Serialization |
| tokio | Rust | Async Runtime |
| requests | Python | HTTP Client |
| fastapi | Python | Web Framework |

## MCP Server (Direct AI Integration)

Instead of running CLI commands, AI IDEs (Claude, Cursor) can use the MCP server:

```json
{
  "mcpServers": {
    "libskills": {
      "command": "libskills-mcp"
    }
  }
}
```

Available tools: `get_skill`, `search_skills`, `find_skills`, `get_section`

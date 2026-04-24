# LibSkills

**A Knowledge Package Manager for Open-Source Libraries — Reduce AI Hallucinations, Eliminate Token Waste, Ship Best Practices Out of the Box.**

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)

<p align="center">
  <img src="https://avatars.githubusercontent.com/u/279074625?s=200" alt="LibSkills logo" width="100">
</p>

---

## What Is LibSkills?

LibSkills is a **Knowledge Package Manager**. It installs **knowledge**, not code.

Every time an LLM encounters an unfamiliar library, it either guesses (hallucination), reads the source (token waste), or searches the web (outdated info). LibSkills solves this by packaging the library's operational knowledge — best practices, pitfalls, threading constraints, performance characteristics, and safety red lines — into a structured, cacheable, versioned format.

This is not a documentation mirror, not a README collector, and not a package manager. It is a **Library Operational Knowledge Layer** — a protocol for distributing, discovering, and consuming library knowledge at the AI agent level.

---

## The Problem

| Approach               | Hallucination Risk | Token Cost | Time to Correct Code |
|------------------------|-------------------|------------|----------------------|
| LLM guesses            | High              | Low        | Unknown (iterations) |
| LLM reads source       | Low               | Very High  | Slow                 |
| Web search + retrieval | Medium            | High       | Variable             |
| **LibSkills**          | **Very Low**      | **Low**    | **First try**        |

---

## Architecture Overview

```
                    ┌─────────────────────────┐
                    │      AI Agent / LLM      │
                    └────────┬────┬────────────┘
                             │    │
                    ┌────────▼────▼────────────┐
                    │    LibSkills CLI (Rust)    │
                    │  search │ get │ info │ ... │
                    └────────┬────────┬─────────┘
                             │        │
              ┌──────────────▼──┐  ┌──▼──────────────┐
              │  Local Cache    │  │  Registry Index  │
              │ ~/.libskills/   │  │  (index.json)    │
              └──────────────┬──┘  └──┬──────────────┘
                             │        │
              ┌──────────────▼────────▼──────────────┐
              │      LibSkills Registry (GitHub)      │
              │    Tier 1 / Tier 2 Skills per lang    │
              └───────────────────────────────────────┘
                                         │
                    ┌────────────────────▼────────────────────┐
                    │       MCP / HTTP Server (Future)        │
                    │    localhost:8701  │  Enterprise Proxy  │
                    └────────────────────┬────────────────────┘
                                         │
            ┌────────────────────────────┼────────────────────────────┐
            │                            │                            │
            ▼                            ▼                            ▼
     ┌──────────────┐          ┌──────────────────┐       ┌──────────────────┐
     │  Cursor      │          │  Claude Code      │       │  VSCode Agent    │
     └──────────────┘          └──────────────────┘       └──────────────────┘
```

---

## How It Works

```bash
# AI searches for a library
$ libskills search cpp logging
  cpp/gabime/spdlog              Tier 1  Main  Fast C++ logging library
  cpp/odyg/quill                Tier 2  Contr Low-latency async logger

# AI downloads the skill
$ libskills get cpp/gabime/spdlog
  ✓ Downloaded spdlog — 1.14.2 to ~/.libskills/cpp/gabime/spdlog/

# AI reads skill files in order:
#   1. skill.json        → metadata, version, trust score
#   2. overview.md       → what the library does and when to use it
#   3. api.md            → core API usage patterns
#   4. pitfalls.md       → what NOT to do
#   5. threading.md      → thread safety and concurrency constraints
#   6. lifecycle.md      → initialization and shutdown
#   7. memory.md         → resource management and leak patterns
#   8. safety.md         → red lines — must never do
#   9. performance.md    → characteristics and limits
#   10. examples/        → minimal working examples

# AI writes correct, idiomatic code on the first try.
```

---

## Full Project Structure

```
LibSkills/
│
├── cli/                            # Rust CLI
│   └── src/
│       ├── main.rs                 # Entry point
│       ├── cli/
│       │   ├── search.rs           # Fuzzy search
│       │   ├── get.rs              # Download skill
│       │   ├── info.rs             # Show metadata
│       │   ├── update.rs           # Refresh index
│       │   ├── cache.rs            # Cache management
│       │   ├── list.rs             # List local skills
│       │   ├── doctor.rs           # Validate local skill
│       │   ├── find.rs             # Semantic search (future)
│       │   └── serve.rs            # MCP/HTTP server (future)
│       ├── registry/               # Registry client logic
│       ├── schema/                 # Schema parsing + validation
│       ├── cache/                  # Local cache management
│       └── index/                  # Index building + search
│
├── registry/                       # Registry — all skills live here
│   ├── index.json                  # Master index (used by CLI)
│   ├── cpp/
│   │   └── gabime/
│   │       └── spdlog/
│   │           ├── skill.json      # Metadata only (no knowledge)
│   │           ├── tier1/          # Official, curated knowledge
│   │           │   ├── overview.md
│   │           │   ├── api.md
│   │           │   ├── pitfalls.md
│   │           │   ├── threading.md
│   │           │   ├── lifecycle.md
│   │           │   ├── memory.md
│   │           │   ├── safety.md
│   │           │   ├── performance.md
│   │           │   └── examples/
│   │           │       └── basic.cpp
│   │           └── tier2/          # Community-submitted knowledge
│   │               ├── community-a/
│   │               └── community-b/
│   ├── rust/
│   │   └── tokio-rs/
│   │       └── tokio/
│   │           └── ...
│   ├── python/
│   │   └── psf/
│   │       └── requests/
│   │           └── ...
│   ├── go/
│   │   └── gin-gonic/
│   │       └── gin/
│   │           └── ...
│   └── js/
│       └── vercel/
│           └── next.js/
│               └── ...
│
├── SPEC.md                         # LibSkills Protocol specification
├── CONTRIBUTING.md                 # Contribution guidelines
├── GOVERNANCE.md                   # Tier + group governance rules
├── LICENSE                         # Apache 2.0
└── README.md
```

## Local Cache Structure

```
~/.libskills/
├── cache/                          # Raw downloaded data
│   ├── index.json                  # Cached registry index
│   └── embeddings/                 # Pre-computed embeddings (future)
├── skills/                         # Installed skills by path
│   ├── cpp/
│   │   └── gabime/
│   │       └── spdlog/             # Same layout as registry
│   │           ├── skill.json
│   │           ├── tier1/
│   │           ├── tier2/
│   │           └── ...
│   └── ...
├── index.db                        # Local search index (SQLite)
├── config.toml                     # User configuration
└── logs/                           # Operation logs
```

---

## Governance

|                | Main (de facto standard)       | Contrib (niche / newer)        |
|----------------|--------------------------------|--------------------------------|
| **Tier 1**     | Official, curated by maintainers | Official, accepted on merit    |
| **Tier 2**     | Community-submitted on popular libs | Community-submitted, any repo |

### Tier 1 — Official
- Accuracy verified against library API
- At least 6 of 9 knowledge files populated
- Updated within 60 days of library release
- Maintained by LibSkills team

### Tier 2 — Community
- Schema-validated (JSON format check)
- No harmful or misleading content
- pitfalls.md (3+ entries) + safety.md (2+ entries) + 1 example minimum

---

## CLI Reference

| Command | Description | Status |
|---------|-------------|--------|
| `libskills search <keyword>` | Fuzzy search registry by name/tags/summary | 🚧 MVP |
| `libskills get <path>[@version]` | Download skill to local cache | 🚧 MVP |
| `libskills info <path>` | Show skill metadata | 🚧 MVP |
| `libskills update` | Refresh registry index | 🚧 MVP |
| `libskills list` | List locally cached skills | 🚧 MVP |
| `libskills cache` | Manage local cache (clear, prune) | 🚧 MVP |
| `libskills doctor <path>` | Validate a local skill file | 📅 Phase 2 |
| `libskills find <intent>` | Semantic / vector search | 📅 Phase 2 |
| `libskills generate <path>` | Auto-generate skill from README/docs | 📅 Phase 3 |
| `libskills lint <path>` | Validate skill format and completeness | 📅 Phase 3 |
| `libskills serve` | Start MCP / HTTP API server on :8701 | 📅 Phase 3 |

---

## AI Skill Reading Protocol

When consuming a skill, AI agents MUST read files in this exact order:

| Step | File | Purpose | Token Budget |
|------|------|---------|-------------|
| 1 | `skill.json` | Understand metadata, version, trust | ~200 |
| 2 | `overview.md` | What the library is and when to use it | 500-1500 |
| 3 | `api.md` | Core API patterns | 500-1500 |
| 4 | `pitfalls.md` | What NOT to do — **most critical** | 500-1500 |
| 5 | `threading.md` | Thread safety, async, concurrency | 500-1500 |
| 6 | `lifecycle.md` | Init, shutdown, static ordering | 500-1500 |
| 7 | `memory.md` | Allocation, ownership, leaks | 500-1500 |
| 8 | `safety.md` | Red lines — must never do | 500-1500 |
| 9 | `performance.md` | Throughput, latency, blocking | 500-1500 |
| 10 | `examples/` | Runnable full examples | Variable |

This reading order ensures the AI learns **what to avoid** before it starts generating code.

---

## Trust Score

Every skill includes a trust score (0–100):

| Score | Meaning | Source |
|-------|---------|--------|
| 95-100 | Official Tier 1 | Verified by LibSkills maintainers |
| 80-94 | Community Tier 1 | High-quality community contribution |
| 50-79 | Tier 2, verified | Passes schema + safety check |
| <50 | Tier 2, unverified | New submission, low trust |

### Score Breakdown

| Component | Max | Source |
|-----------|-----|--------|
| Official Review | 40 | Tier 1 maintainer audit |
| GitHub Stars | 20 | Stars tier |
| Community Votes | 20 | User ratings |
| Update Freshness | 15 | Updated within 60 days of release |
| Issue Health | 5 | Low open-issue ratio |

---

## Skill Types

| Type | Example | AI Consumption Strategy |
|------|---------|------------------------|
| `library` | spdlog, fmt | Full API + pitfalls |
| `framework` | React, FastAPI | Lifecycle + routing patterns |
| `sdk` | AWS SDK, Stripe | Auth + error handling |
| `runtime` | Node.js, Deno | Event loop + async patterns |
| `tooling` | CMake, Docker | Config patterns |
| `middleware` | Express middleware | Chain pattern |
| `database` | PostgreSQL driver | Connection + query patterns |
| `network` | Boost.Asio, libcurl | Async + error handling |
| `ui` | Dear ImGui, Qt | Event loop + rendering |
| `compiler` | Clang plugins | Plugin lifecycle |

---

## Skill Inheritance

Skills can inherit knowledge from parent skills to avoid duplication.

```
react-router@6.20
  inherits: react@18
```

When AI reads `react-router`, it also loads `react`'s skill first, then applies overrides.

### Dependency Graph

If library A depends on library B, AI SHOULD load B's skill before A's:

```json
{
  "dependencies": {
    "required": ["fmt"],
    "skills": ["cpp/fmtlib/fmt"]
  }
}
```

---

## Enterprise Private Registry

LibSkills supports private registries for organizations:

```bash
libskills registry add company-internal https://registry.internal.company.com
libskills get internal/sdk/auth
```

Use cases:
- Internal SDKs and RPC frameworks
- Company-specific component libraries
- Proprietary tooling and runtimes

---

## Roadmap

### Phase 1 — MVP (Week 1)
- [x] Repository structure
- [x] Protocol specification
- [x] Governance rules
- [x] Contribution guidelines
- [ ] CLI: `search`, `get`, `info`, `update`, `cache`, `list`
- [ ] 3-5 core skills (spdlog, fmt, nlohmann/json)
- [ ] Registry index mechanism with snapshots
- [ ] CI for index auto-build

### Phase 2 — Discovery (Month 1-2)
- [ ] Semantic search with embeddings
- [ ] Version binding (`libskills get spdlog@1.14.2`)
- [ ] Trust score calculation automation
- [ ] Completness score
- [ ] Skill linting (`libskills lint`)
- [ ] 20+ curated Tier 1 skills across 3 languages

### Phase 3 — Expand (Month 2-4)
- [ ] MCP / HTTP API (`libskills serve` on :8701)
- [ ] Enterprise private registry
- [ ] Skill generator (`libskills generate`)
- [ ] Skill inheritance support
- [ ] Registry mirrors

### Phase 4 — Ecosystem (Month 4+)
- [ ] Protocol standardization
- [ ] IDE integration (Cursor, VSCode, Claude Code)
- [ ] Community ratings system
- [ ] Benchmark data in skills
- [ ] AI-native ecosystem adoption

---

## What LibSkills Is NOT

- **Not** a documentation mirror — we don't copy API references
- **Not** a README collector — we don't mirror repos
- **Not** a package manager — we manage knowledge, not code
- **Not** an encyclopedia — we focus on high-density experiential knowledge
- **Not** a tutorial platform — we don't teach "hello world"
- **Not** a search engine — we serve pre-compiled, curated knowledge

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

---

## License

[Apache 2.0](LICENSE) — LibSkills by [LibSkills Org](https://github.com/LibSkills).

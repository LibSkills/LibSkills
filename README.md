# LibSkills

**A Knowledge Package Manager for Open-Source Libraries — Reduce AI Hallucinations, Eliminate Token Waste, Ship Best Practices Out of the Box.**

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)

---

## What Is LibSkills?

LibSkills is a **Knowledge Package Manager**. It installs **knowledge**, not code.

Every time an LLM encounters an unfamiliar library, it either guesses (hallucination), reads the source (token waste), or searches the web (outdated info). LibSkills solves this by packaging the library's operational knowledge — best practices, pitfalls, threading constraints, performance characteristics, and safety red lines — into a structured, cacheable, versioned format.

This is not a documentation mirror, not a README collector, and not a package manager. It is a **Library Operational Knowledge Layer** built on the **LibSkills Protocol**.

---

## The Problem

| Approach               | Hallucination Risk | Token Cost | Time to Correct Code |
|------------------------|-------------------|------------|----------------------|
| LLM guesses            | High              | Low        | Unknown (iterations) |
| LLM reads source       | Low               | Very High  | Slow                 |
| Web search + retrieval | Medium            | High       | Variable             |
| **LibSkills**          | **Very Low**      | **Low**    | **First try**        |

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

## Project Structure

```
LibSkills/
├── cli/                    # Rust CLI
│   └── src/
│       ├── main.rs
│       ├── cli/
│       │   ├── search.rs
│       │   ├── get.rs
│       │   ├── info.rs
│       │   └── cache.rs
│       ├── registry/
│       ├── schema/
│       ├── cache/
│       └── index/
│
├── registry/
│   ├── index.json           # Master index of all skills
│   ├── cpp/
│   │   └── gabime/
│   │       └── spdlog/
│   │           ├── skill.json      # Metadata only
│   │           ├── tier1/
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
│   │           └── tier2/
│   │               ├── community-a/
│   │               └── community-b/
│   ├── rust/
│   ├── python/
│   ├── go/
│   └── js/
│
├── SPEC.md                 # LibSkills Protocol specification
├── CONTRIBUTING.md         # Contribution guidelines
├── GOVERNANCE.md           # Tier + group governance
├── LICENSE                 # Apache 2.0
└── README.md
```

---

## Governance

|                | Main (de facto standard)       | Contrib (niche / newer)        |
|----------------|--------------------------------|--------------------------------|
| **Tier 1**     | Official, curated by maintainers | Official, accepted on merit    |
| **Tier 2**     | Community-submitted on popular libs | Community-submitted, any repo |

- **Tier 1** skills are reviewed and maintained by the LibSkills team.
- **Tier 2** skills are community-contributed and merged after CI validation.
- **Main** group: libraries that are the de-facto standard in their ecosystem.
- **Contrib** group: smaller, newer, or alternative libraries.

---

## CLI Reference

```bash
libskills search <keyword>       # Fuzzy search the registry index
libskills get <path>[@version]   # Download a skill to local cache
libskills info <path>            # Show skill metadata
libskills update                 # Refresh the registry index
libskills list                   # List locally cached skills
libskills cache                  # Manage local cache
libskills doctor <path>          # Validate a local skill
libskills find <intent>          # Semantic / vector search (future)
libskills serve                  # Start MCP / HTTP API server (future)
```

### Local Cache

```
~/.libskills/
├── cache/
├── skills/
├── index/
├── embeddings/
├── config.toml
└── logs/
```

---

## AI Skill Reading Order

When an AI agent uses a skill, it should read files in this order:

1. `skill.json` — metadata, version, trust score, tags
2. `overview.md` — what this library is and when to use it
3. `api.md` — core API usage with minimal examples
4. `pitfalls.md` — what NOT to do (most important for reducing errors)
5. `threading.md` — thread safety, async behavior, concurrency constraints
6. `lifecycle.md` — initialization, shutdown, static destructor ordering
7. `memory.md` — allocation, ownership, leak prevention
8. `safety.md` — red lines: conditions that must NEVER occur
9. `performance.md` — throughput, latency, blocking behavior
10. `examples/` — full runnable examples

**Each file should be 500–1500 tokens** — small enough to fit in context without pollution.

---

## Trust Score

Every skill includes a trust score (0–100) to help AI agents gauge reliability:

| Score  | Meaning              | Source                              |
|--------|----------------------|-------------------------------------|
| 95-100 | Official Tier 1      | Verified by LibSkills maintainers    |
| 80-94  | Community Tier 1     | High-quality community contribution  |
| 50-79  | Tier 2, Verified     | Passes schema validation, no review  |
| <50    | Tier 2, Unverified   | New submission, low community trust |

---

## Roadmap

### Phase 1 — MVP (Week 1)
- [x] Registry structure
- [x] Specification
- [ ] CLI: `search`, `get`, `info`, `update`, `cache`
- [ ] 3-5 core skills (spdlog, fmt, nlohmann_json)
- [ ] Registry index mechanism
- [ ] CI for index auto-build

### Phase 2 — Discovery (Month 1-2)
- [ ] Semantic search with embeddings
- [ ] Version binding (`libskills get spdlog@1.14.2`)
- [ ] Trust score system
- [ ] 20+ curated Tier 1 skills

### Phase 3 — Expand (Month 2-4)
- [ ] MCP / HTTP API (`libskills serve`)
- [ ] Enterprise private registry
- [ ] Skill generator (`libskills generate`)
- [ ] Skill linting (`libskills lint`)
- [ ] Raw file access (devcontainer, offline bundles)

### Phase 4 — Ecosystem (Month 4+)
- [ ] Protocol standard
- [ ] IDE integration (Cursor, VSCode, Claude Code)
- [ ] Registry mirrors
- [ ] AI-native ecosystem adoption

---

## What LibSkills Is NOT

- **Not** a documentation mirror — we don't copy API references
- **Not** a README collector — we don't mirror repos
- **Not** a package manager — we manage knowledge, not dependencies
- **Not** an encyclopedia — we focus on high-density experiential knowledge
- **Not** a tutorial platform — we don't teach "hello world"

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

---

## License

Apache 2.0. See [LICENSE](LICENSE).

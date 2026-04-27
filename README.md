# LibSkills

<p align="center">
  <img src="./media/logo.jpg" alt="LibSkills logo" width="120">
</p>

**Behavioral Knowledge Layer for Open-Source Libraries.**

Reduce AI hallucinations. Eliminate token waste. Ship best practices out of the box.

LibSkills is a **standard** — a universal way for any GitHub repository to ship operational knowledge that AI agents, IDEs, and CI systems can consume to use the library safely.

It answers one question: *"What must an AI agent know to use this library safely?"*

---

## The Standard

Every library repository can place a `.libskills/` directory at its root, containing structured knowledge files following the [LibSkills Specification](https://github.com/LibSkills/libskills-docs).

```
your-library/
├── .libskills/
│   ├── skill.json          # Metadata
│   ├── overview.md          # What the library is
│   ├── pitfalls.md          # What NOT to do
│   ├── safety.md            # Red lines
│   ├── lifecycle.md         # Init/shutdown
│   ├── threading.md         # Concurrency
│   ├── best-practices.md    # Recommended patterns
│   ├── performance.md       # Perf characteristics
│   └── examples/
└── src/
```

---

## Repositories

| Repository | Role |
|------------|------|
| [libskills-docs](https://github.com/LibSkills/libskills-docs) | Canonical specification, philosophy, roadmap, governance |
| [libskills-schema](https://github.com/LibSkills/libskills-schema) | JSON Schema definitions for `skill.json` and `index.json` |
| [libskills-registry](https://github.com/LibSkills/libskills-registry) | Aggregated index of skills from repos across GitHub |
| [libskills-cli](https://github.com/LibSkills/libskills-cli) | Rust CLI — search, get, init, validate, lint |
| [libskills-protocol](https://github.com/LibSkills/libskills-protocol) | MCP and HTTP protocol definitions (future) |

---

## Protocol First, Platform Second

LibSkills is a **protocol**, not a platform. A skill is valid whether it lives in:

- A library's own repository (`.libskills/`) — *self-hosted, decentralized*
- The official LibSkills registry — *curated aggregation*
- An enterprise private registry — *internal use*

The CLI acts as a **resolver**: given a library name, it discovers the best available skill.

---

## Quickstart

```bash
# Place a .libskills/ directory in your library's repo
# AI agents discover it automatically
```

Or use the CLI:

```bash
# Install CLI
cargo install libskills

# Update registry index
libskills update

# Search for a skill
libskills search cpp logging

# Download a skill
libskills get cpp/gabime/spdlog
```

---

## Governance

| | Main | Contrib |
|--|------|---------|
| **Tier 1** | Official, curated | Official, accepted on merit |
| **Tier 2** | Community-submitted | Community-submitted, any repo |

See [libskills-docs/GOVERNANCE.md](https://github.com/LibSkills/libskills-docs/blob/main/GOVERNANCE.md) for the full governance rules.

---

## License

[Apache 2.0](LICENSE) — LibSkills by [LibSkills Org](https://github.com/LibSkills)

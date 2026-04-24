# LibSkills

**Knowledge Package Manager for Open-Source Libraries.**

Reduce AI hallucinations. Eliminate token waste. Ship best practices out of the box.

---

## Repositories

| Repository | Description |
|------------|-------------|
| [libskills-cli](https://github.com/LibSkills/libskills-cli) | Rust CLI — search, get, update, doctor, and manage skills |
| [libskills-registry](https://github.com/LibSkills/libskills-registry) | Official skill registry — Tier 1 & Tier 2 knowledge files |
| [libskills-schema](https://github.com/LibSkills/libskills-schema) | JSON Schema definitions for skill files |
| [libskills-protocol](https://github.com/LibSkills/libskills-protocol) | MCP and HTTP protocol definitions |

## Specification

The full LibSkills Protocol specification is in [SPEC.md](./SPEC.md).

## Quickstart

```bash
# Install CLI
cargo install libskills

# Update registry index
libskills update

# Search for a library
libskills search cpp logging

# Download a skill
libskills get cpp/gabime/spdlog

# AI reads and writes correct code on the first try
```

## Governance

| | Main | Contrib |
|--|------|---------|
| **Tier 1** | Official, curated | Official, accepted on merit |
| **Tier 2** | Community-submitted | Community-submitted, any repo |

See [GOVERNANCE.md](./GOVERNANCE.md) for full details.

## License

[Apache 2.0](LICENSE) — LibSkills by [LibSkills Org](https://github.com/LibSkills).

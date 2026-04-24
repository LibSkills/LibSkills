# LibSkills

**A centralized skill registry for open-source libraries — reduce AI hallucinations, eliminate redundant token waste, ship with best practices out of the box.**

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)

---

## The Problem

Every time an LLM encounters an unfamiliar library, it either:

1. **Guesses** — producing plausible-sounding but incorrect API calls (hallucination)
2. **Reads the source** — consuming thousands of tokens to infer usage patterns
3. **Searches the web** — relying on StackOverflow posts that may be outdated

None of these are reliable. The result: wasted tokens, broken code, and wasted time.

## The Solution

LibSkills provides **curated skill files** for open-source libraries. Each skill file encodes everything an AI agent needs to use a library correctly:

- Minimal working examples and anti-patterns
- Thread safety and concurrency constraints
- Known crash/leak patterns and their fixes
- Performance characteristics and resource management
- Classic issue resolutions from the community
- Safety red lines — what you must never do

### One agent's setup flow

```
$ libskills search cpp json
  cpp/nlohmann/json              Tier 1  Main  JSON for Modern C++
  cpp/tao/json                   Tier 2  Contr Lightweight, header-only
  cpp/pfr                        Tier 2  Contr Reflection-based serialization

$ libskills get cpp/nlohmann/json
  ✓ Downloaded skills/nlohmann/json — 3.x

$ ai reads ~/.libskills/cpp/nlohmann/json/skill.json
  → Writes correct, idiomatic code. No guesswork. No wasted tokens.
```

---

## Project Structure

```
LibSkills/
├── cli/                    # Rust CLI (includes index)
│   └── src/main.rs
├── index.json              # Master index, versioned with CLI
├── registry/
│   ├── main/               # Foundational, widely-adopted libraries
│   │   ├── cpp/
│   │   ├── rust/
│   │   ├── python/
│   │   ├── go/
│   │   └── js/
│   └── contrib/            # Smaller or niche community libraries
│       ├── cpp/
│       ├── rust/
│       ├── python/
│       ├── go/
│       └── js/
├── SPEC.md                 # Skill file format specification
├── CONTRIBUTING.md         # Contribution guidelines
└── GOVERNANCE.md           # Tier + group governance rules
```

---

## Governance

|                | main (de facto standard libs)   | contrib (niche / newer libs)   |
|----------------|----------------------------------|--------------------------------|
| **Tier 1**     | Official, curated by maintainers | Official, accepted on merit    |
| **Tier 2**     | Community-submitted on popular libs | Community-submitted, any repo |

- **Tier 1** skills are reviewed and maintained by the LibSkills team.
- **Tier 2** skills are community-contributed and merged after CI validation.
- **main** group includes libraries that are the de-facto standard in their ecosystem.
- **contrib** group is for smaller, newer, or alternative libraries.

---

## CLI Quickstart (Coming Soon)

```bash
# Install
curl -fsSL https://github.com/LibSkills/LibSkills/releases/latest/download/libskills-x86_64-linux.tar.gz | tar xz
sudo mv libskills /usr/local/bin

# Search
libskills search cpp logging
libskills search rust http

# Download a skill to the local cache
libskills get cpp/spdlog

# Find by intent (semantic/vector search)
libskills find "fast json parser"
libskills find "async http client"

# Update the index
libskills update

# List locally cached skills
libskills list
```

---

## Why LibSkills?

| Approach               | Hallucination Risk | Token Cost | Time to Correct Code |
|------------------------|-------------------|------------|----------------------|
| LLM guesses            | High              | Low        | Unknown (iterations) |
| LLM reads source       | Low               | Very High  | Slow                 |
| Web search + retrieval | Medium            | High       | Variable             |
| **LibSkills**          | **Very Low**      | **Low**    | **First try**        |

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for how to submit a skill for your favorite library.

---

## License

Apache 2.0. See [LICENSE](LICENSE).

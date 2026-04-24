# Contributing to LibSkills

Thank you for contributing to the Library Knowledge Layer.

---

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How to Submit a Skill](#how-to-submit-a-skill)
- [Skill Requirements](#skill-requirements)
- [Tier 1 vs Tier 2](#tier-1-vs-tier-2)
- [Main vs Contrib](#main-vs-contrib)
- [File Naming](#file-naming)
- [Writing Guidelines](#writing-guidelines)
- [Pull Request Process](#pull-request-process)
- [Getting Help](#getting-help)

---

## Code of Conduct

We follow the [Contributor Covenant](https://www.contributor-covenant.org/) Code of Conduct. Be respectful, constructive, and inclusive.

## How to Submit a Skill

1. Read [SPEC.md](SPEC.md) thoroughly.
2. Fork this repository.
3. Create your skill directory:

   ```
   registry/{language}/{author}/{name}/
   ├── skill.json
   ├── tier1/  (or tier2/)
   │   ├── overview.md
   │   ├── api.md
   │   ├── pitfalls.md          ← REQUIRED
   │   ├── threading.md
   │   ├── lifecycle.md
   │   ├── memory.md
   │   ├── safety.md            ← REQUIRED
   │   ├── performance.md
   │   └── examples/
   │       └── basic.{cpp,rs,py,go,js}
   ```

4. Update `index.json` with your entry.
5. Open a pull request.

## Skill Requirements

### Required for ALL submissions

- `skill.json` with complete metadata
- `overview.md` — brief description
- `pitfalls.md` — what NOT to do (at least 3 entries)
- `safety.md` — red lines (at least 2 entries)
- At least one example in `examples/`
- All files between 500–1500 tokens

### Strongly encouraged

- `api.md` — core API patterns
- `threading.md` — concurrency constraints
- `lifecycle.md` — init/shutdown
- `memory.md` — resource management
- `performance.md` — perf characteristics

## Tier 1 vs Tier 2

| Aspect | Tier 1 | Tier 2 |
|--------|--------|--------|
| Who | LibSkills maintainers | Anyone |
| Review | Full accuracy audit | Format + safety check |
| Trust | 90–100 | 50–89 |
| Update cadence | Within 60 days of release | Best effort |
| READ order | AI reads first | AI falls back if no Tier 1 |

Submit your skill to `tier2/` initially. If it receives community recognition, it can be upgraded to `tier1/` via pull request review.

## Main vs Contrib

**Main**: Libraries that are the de-facto standard in their category (spdlog, tokio, serde, requests, fmt, nlohmann/json).

**Contrib**: Smaller, niche, or newer libraries. No barriers to entry — any library qualifies.

## File Naming

- All directory and file names MUST be **lowercase**
- Use **kebab-case** for multi-word names
- File extensions: `.json`, `.md`
- Example file extensions: `.cpp`, `.rs`, `.py`, `.go`, `.js`

## Writing Guidelines

### DO

- Write for an **AI agent**, not a human developer
- Be precise and unambiguous
- Include code snippets that actually compile
- Focus on the 20% of APIs used 80% of the time
- Highlight what CAN go wrong more than what can go right

### DO NOT

- Copy full API reference documentation
- Mirror README content
- Include general programming tutorials
- Use vague language ("may", "might", "sometimes")
- Exceed 1500 tokens per file

## Pull Request Process

1. Ensure your skill passes schema validation.
2. Ensure all required files exist and are non-empty.
3. Ensure your `index.json` entry is correct.
4. Tier 2 PRs: reviewed within 3–5 business days.
5. Tier 1 PRs: require 2 maintainer approvals.

## Getting Help

- Open a [GitHub Discussion](https://github.com/LibSkills/LibSkills/discussions)
- Check [SPEC.md](SPEC.md) for format specifics
- Join the community (link TBD)

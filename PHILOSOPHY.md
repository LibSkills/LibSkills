# LibSkills Philosophy

**The constitution of the LibSkills project.**

---

## What LibSkills Is

LibSkills is a **Behavioral Knowledge Layer** for open-source libraries.

It exists to answer one question: *"What must an AI agent know to use this library safely?"*

## What LibSkills Is NOT

- **Not** a documentation mirror — we don't copy API references
- **Not** a README collector — we don't mirror repos
- **Not** a package manager — we manage *knowledge*, not code
- **Not** an encyclopedia — we focus on high-density experiential knowledge
- **Not** a tutorial platform — we don't teach fundamentals
- **Not** a search engine — we serve pre-compiled, curated knowledge
- **Not** a StackOverflow replacement — we capture behavioral contracts, not opinions

---

## The Seven Rules

### Rule 1: No documentation copying

A skill must never duplicate content that already exists in the library's official documentation. If the user needs API reference, they should read the docs. The skill captures what the docs *don't* say: constraints, pitfalls, lifecycle, hidden behaviors.

### Rule 2: Only high-value behavioral knowledge

Every piece of knowledge in a skill must answer at least one of:
- "Where is this library most likely to crash?"
- "What hidden constraints exist?"
- "What is the most expensive mistake an AI can make?"
- "What is invisible from reading the API signature?"

If a piece of knowledge doesn't reduce error probability, it doesn't belong in the skill.

### Rule 3: Error reduction > knowledge accumulation

A skill with 5 carefully chosen pitfalls is more valuable than a skill with 50 facts. The primary metric of a skill's quality is: *how many AI mistakes does it prevent?* Not: *how much does it cover?*

### Rule 4: Machine-readable constraints

Every constraint in a skill must be representable in a structured format (`constraints.json`, `lifecycle.json`, `hazards.json`). Free-form prose is supplementary, not primary. AI agents must be able to derive actionable rules without parsing natural language.

### Rule 5: Chunked and partial-read compatible

No file in a skill should exceed 1500 tokens. Every file must be independently useful — an AI agent should be able to read `threading.md` without reading `overview.md`. The reading order is a recommendation, not a requirement.

### Rule 6: Version-bound

Every skill must declare which library version(s) it targets. A skill for spdlog 1.5 is a different artifact from a skill for spdlog 1.14. Skills must include version ranges (`introduced_in`, `deprecated_in`) for API-level knowledge.

### Rule 7: Trust-graded

Every skill must carry a trust score (0–100) and declare its tier (tier1 or tier2), author type (official, community, enterprise, ai_generated), and stability level (experimental, stable, deprecated). AI agents use these signals to decide how much to trust the knowledge.

---

## Skill as Protocol, Not Repository

LibSkills defines a **format and a contract**, not a storage location.

A skill file is valid whether it lives in:
- The official LibSkills registry
- The library's own repository (`.libskills/`)
- An enterprise private registry
- A local directory (`~/.libskills/private/`)

The CLI (`libskills`) acts as a **resolver**: given a library name, it discovers the best available skill by checking local cache → registry → upstream repository → mirrors.

This means LibSkills is a **protocol first, platform second**. The registry is a convenience, not a monopoly.

---

## The Knowledge Primitive

Knowledge in LibSkills is organized in three layers:

```
Library          →  spdlog
Capability       →  async logging
Constraint       →  must flush before destroy
```

The atomic unit is the **knowledge atom**:

```json
{
  "type": "constraint",
  "layer": "lifecycle",
  "content": "must flush before destroy",
  "kind": "fact",
  "language": ["cpp"],
  "introduced_in": "1.0",
  "deprecated_in": null
}
```

This structure allows:
- Cross-language patterns (async shutdown is the same problem in C++, Rust, Python)
- Machine-readable enforcement
- Composition across skills
- Downstream tooling (static analysis, linting, CI checks)

---

## Success Metrics

LibSkills measures success not by stars or downloads, but by:

1. **AI hallucination rate**: How many fewer incorrect API calls occur after skill consumption?
2. **First-compile success rate**: Can the AI generate code that compiles on the first try?
3. **Iteration count**: How many fewer rounds of "fix this" does the AI need?
4. **Integration time**: How much faster does a new library become usable?
5. **Skill corpus quality**: What percentage of skills meet the completeness threshold?

---

## What This Makes Possible

- **AI agents** that never guess a library API
- **IDEs** that surface constraints during autocomplete
- **CI systems** that check for misuse patterns
- **Enterprise teams** that standardize library usage across thousands of developers
- **A new software layer**: source code → package manager → runtime → **knowledge layer** → docs

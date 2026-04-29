# LibSkills

<p align="center">
  <img src="./media/logo.jpg" alt="LibSkills logo" width="120">
</p>

**Behavioral Knowledge Layer for Open-Source Libraries.**

AI coding assistants hallucinate library APIs, misuse thread safety, ignore lifecycle constraints. LibSkills fixes this: a `.libskills/` directory in any repo tells AI agents *where the library breaks* before they generate code.

---

## Who Are You?

### 📦 I'm a Library Author

Add one directory to your repo. AI tools will read it before generating code that uses your library.

```bash
# Install (one line)
curl -fsSL https://raw.githubusercontent.com/LibSkills/LibSkills/main/install.sh | bash

# Scaffold your skill
cd your-library/
libskills init -n yourlib -r you/yourlib -l python -t "api,client"

# Fill in the pitfalls and safety sections, then validate
libskills lint --fix .libskills/
libskills validate .libskills/

# Commit. Done.
git add .libskills/ && git commit -m "Add LibSkills skill"
```

**That's it.** No registration. No PR. No approval. Add the `libskills` GitHub topic to your repo and the aggregation registry auto-discovers it.

### 🤖 I Use AI to Write Code

```bash
# One line install
curl -fsSL https://raw.githubusercontent.com/LibSkills/LibSkills/main/install.sh | bash

# Get started
libskills update
libskills find "fast C++ logger with async support"
libskills search http
libskills get cpp/gabime/spdlog
```

### 🖥️ I Use an AI IDE (Claude, Cursor, etc.)

Configure the MCP server. Your AI automatically queries LibSkills before generating library code:

```json
{
  "mcpServers": {
    "libskills": {
      "command": "libskills-mcp"
    }
  }
}
```

Or start the HTTP API:

```bash
libskills serve --port 8701
curl "http://localhost:8701/v1/find?q=async+runtime"
```

---

## The Problem LibSkills Solves

```
Without LibSkills:
  AI: "I'll use spdlog for logging"
  → Uses std::endl (flush every write)
  → Shares non-thread-safe sinks across threads
  → Calls shutdown() in a static destructor
  → 3 bugs, 2 crashes, 15 minutes debugging

With LibSkills:
  AI reads .libskills/pitfalls.md first
  → Uses \n instead of std::endl
  → Uses _mt sinks in multi-threaded code
  → Calls shutdown() in main()
  → Works on first try
```

---

## The Standard

Every repo can self-host a `.libskills/` directory. No central server required.

```
your-library/
├── .libskills/
│   ├── skill.json          # Metadata (language, tier, trust, tags)
│   ├── overview.md          # [P0] What it is, when to use it
│   ├── pitfalls.md          # [P0] What NOT to do (≥3 entries)
│   ├── safety.md            # [P0] Red lines — NEVER do these
│   ├── lifecycle.md         # [P1] Init / shutdown ordering
│   ├── threading.md         # [P1] Thread safety guarantees
│   ├── best-practices.md    # [P1] Recommended patterns
│   ├── performance.md       # [P2] Throughput / latency / memory
│   └── examples/            # [P3] Working code
└── src/
```

[Full Specification →](https://github.com/LibSkills/libskills-docs/blob/main/SPEC.md)

---

## What We Ship

| Layer | What | Where |
|-------|------|-------|
| **Standard** | `.libskills/` convention, JSON schema v1, reading protocol | [libskills-docs](https://github.com/LibSkills/libskills-docs) |
| **Schema** | `skill.json` and `index.json` formal definitions | [libskills-schema](https://github.com/LibSkills/libskills-schema) |
| **Skills** | 6 Tier 1 skills: spdlog, fmt, serde, tokio, requests, fastapi | [libskills-registry](https://github.com/LibSkills/libskills-registry) |
| **CLI** | 11 commands: init, validate, lint, update, search, find, get, info, list, cache, serve | [libskills-cli](https://github.com/LibSkills/libskills-cli) |
| **HTTP API** | 6 REST endpoints for AI tool integration | `libskills serve` |
| **MCP Server** | 4 tools for Claude/Cursor native integration | [libskills-protocol](https://github.com/LibSkills/libskills-protocol) |
| **Docs** | Specification, philosophy, quickstart, authoring guide, API reference | [libskills-docs](https://github.com/LibSkills/libskills-docs) |

---

## Validation Status

LibSkills is currently in **Phase 4: Value Validation**. We're running controlled experiments to prove that skills reduce AI errors.

| Metric | Control (No Skills) | Treatment (With Skills) | Improvement |
|--------|---------------------|------------------------|-------------|
| Hallucination Rate | TBD | TBD | TBD |
| First-Compile Rate | TBD | TBD | TBD |
| Runtime Error Rate | TBD | TBD | TBD |

**Status**: Experiment in progress. Results expected soon.

[Read the full experiment design →](experiments/phase4-design.md)

### Security Notice

⚠️ **Never commit API keys or `.env` files!** The experiments use API keys for AI services. These are stored in `.env` files which are ignored by `.gitignore`. See [experiments/README.md](experiments/README.md#security-notice) for setup instructions.

---

## Protocol First

LibSkills is a **standard**, not a platform. A skill is valid whether it lives in:

- A library's own repo (`.libskills/`) — *primary, decentralized*
- The LibSkills aggregation registry — *discovery convenience*
- An enterprise private registry — *internal adoption*

Like `.editorconfig` or `package.json`, the convention is the product.

---

## License

[Apache 2.0](LICENSE) — [LibSkills Org](https://github.com/LibSkills)

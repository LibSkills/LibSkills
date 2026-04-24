# LibSkills Governance

How Tier 1 / Tier 2 and main / contrib decisions are made.

---

## Tier Classification

### Tier 1 — Official

Criteria for a skill to qualify as Tier 1:

1. **Accuracy**: Every field in the skill file is verified against the library's actual API.
2. **Completeness**: At minimum, `minimal_example`, `anti_patterns`, `red_lines`, `common_issues`, and `performance` sections are populated.
3. **Freshness**: The skill is updated within 60 days of the library's last release.
4. **Maintainers**: At least one LibSkills team member actively maintains the skill.

Tier 1 skills are **trusted**. AI agents reading a Tier 1 skill should be confident the information is correct.

### Tier 2 — Community

Criteria:

1. **Format compliance**: The JSON file passes schema validation.
2. **No harmful content**: The skill does not contain malicious, misleading, or intentionally incorrect instructions.
3. **Minimal completeness**: At minimum, `minimal_example`, `red_lines`, and one `common_issue` must be provided.

Tier 2 skills are **useful but unverified**. AI agents should use them with caution — ideally cross-referencing with the library's official documentation.

### Upgrading Tier 2 → Tier 1

1. Open an issue requesting tier upgrade.
2. A LibSkills maintainer reviews the skill for accuracy and completeness.
3. If accepted, the skill is relabeled Tier 1 and moved to the official maintenance roster.

---

## Group Classification

### main

Libraries in `main` must meet **at least one** of:

- **Market dominance**: The library is the most widely used in its category (e.g., fmt for C++ formatting, serde for Rust serialization).
- **Community adoption**: 10,000+ GitHub stars OR the library is a dependency of at least 5 other main-group libraries.
- **Platform standard**: The library is officially recommended or bundled by the language's foundation or package manager (e.g., `tokio` for Rust async, `requests` for Python HTTP).

### contrib

Any library not in `main`. No barriers to entry.

---

## Decision Process

- **Tier 1 → main**: Requires 2 maintainer approvals.
- **Tier 1 → contrib**: Requires 1 maintainer approval.
- **Tier 2 → main**: Merged after CI validation (automated).
- **Tier 2 → contrib**: Merged after CI validation (automated).

---

## Maintainer Roles

| Role | Responsibilities |
|------|-----------------|
| **Core Maintainer** | Approve Tier 1 skills, manage governance, resolve disputes |
| **Tier 1 Maintainer** | Review and maintain Tier 1 skills in specific languages |
| **Community Reviewer** | Review Tier 2 PRs, validate format compliance |

---

## Conflict Resolution

If a skill's accuracy is disputed:

1. The disputing party opens an issue with evidence (code snippets, documentation links).
2. The skill's last maintainer responds within 7 days.
3. If unresolved, a Core Maintainer makes the final decision.
4. If the skill is found to be incorrect, it is either fixed or moved to Tier 2.

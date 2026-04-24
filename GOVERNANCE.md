# LibSkills Governance

Rules for Tier 1 / Tier 2 and Main / Contrib classification.

---

## Tier Classification

### Tier 1 — Official Criteria

1. **Accuracy**: Every field is verified against the library's actual API.
2. **Completeness**: At minimum, 6 of 9 knowledge files are populated (including pitfalls.md and safety.md).
3. **Freshness**: Updated within 60 days of the library's last release.
4. **Maintained**: At least one LibSkills team member actively maintains it.

### Tier 2 — Community Criteria

1. **Format compliance**: Passes schema validation.
2. **No harmful content**: No malicious, misleading, or intentionally incorrect instructions.
3. **Minimal completeness**: pitfalls.md (3+ entries), safety.md (2+ entries), and one example.

### Upgrading Tier 2 → Tier 1

1. Open a pull request with the upgrade proposal.
2. A maintainer reviews the skill for accuracy and completeness.
3. If accepted, the skill directory is reorganized (tier2/ → tier1/).

## Group Classification

### Main

Must meet **at least one** of:

- **Market dominance**: Most widely used library in its category.
- **Community adoption**: 10,000+ GitHub stars OR dependency of 5+ other main-group libraries.
- **Ecosystem standard**: Officially recommended or bundled by the language's foundation.

### Contrib

Any library not in main. No barriers to entry.

## Decision Process

| Action | Approvals Required |
|--------|-------------------|
| New Tier 1 skill | 2 maintainers |
| Tier 2 → Tier 1 upgrade | 2 maintainers |
| New Tier 2 skill | CI validation only |
| Main → Contrib demotion | 1 maintainer |
| Trust score change > 10 | Requires issue + vote |

## Maintainer Roles

| Role | Responsibilities |
|------|-----------------|
| Core Maintainer | Approve Tier 1, manage governance, resolve disputes |
| Tier 1 Maintainer | Review and maintain Tier 1 skills per language |
| Community Reviewer | Review Tier 2 PRs, validate format compliance |

## Conflict Resolution

1. Dispute is opened as a GitHub issue with evidence.
2. The skill's last maintainer responds within 7 days.
3. If unresolved, a Core Maintainer makes the final decision.
4. If the skill is found to be incorrect, it is either fixed or moved to Tier 2.

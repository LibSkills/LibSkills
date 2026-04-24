# Contributing to LibSkills

Thank you for considering contributing to LibSkills! This document outlines the process for submitting skills, reporting issues, and improving the project.

---

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How to Submit a Skill](#how-to-submit-a-skill)
- [Skill Requirements](#skill-requirements)
- [Where Does My Skill Go?](#where-does-my-skill-go)
- [Pull Request Process](#pull-request-process)
- [Style Guide](#style-guide)
- [Getting Help](#getting-help)

---

## Code of Conduct

We follow the [Contributor Covenant](https://www.contributor-covenant.org/) Code of Conduct. Be respectful, constructive, and inclusive.

## How to Submit a Skill

1. **Read [SPEC.md](SPEC.md)** thoroughly — your skill file must conform to the skill format specification.
2. **Fork this repository** (or the `registry` subdirectory if we split later).
3. **Create your skill file** at the correct path:

   ```
   registry/{group}/{language}/{author}/{name}.json
   ```

   Example: `registry/main/cpp/nlohmann/json.json`

4. **Validate your skill** by running the CLI validator (when available) or manually checking against SPEC.md.
5. **Update `index.json`** to include your new skill entry.
6. **Open a pull request**.

## Skill Requirements

Every skill submission must include:

- A complete skill file in the [format specified in SPEC.md](SPEC.md).
- A commitment to keep the skill up-to-date as the library evolves (LibSkills will flag outdated skills).
- For Tier 1 submissions: proof that the library is the de-facto standard in its category.

### What makes a good skill

A well-written skill answers these questions for an AI agent:

1. **What is the minimal working example?**
2. **What are the common pitfalls?**
3. **What are the performance characteristics?**
4. **What are the thread-safety guarantees?**
5. **What are the known crash/leak patterns?**
6. **What are the error handling patterns?**
7. **What are the configuration best practices?**
8. **What are the API deprecations to watch out for?**

## Where Does My Skill Go?

|                      | main                         | contrib                            |
|----------------------|------------------------------|------------------------------------|
| **Tier 1** (official) | De-facto standard libraries  | Accepted by maintainers on merit   |
| **Tier 2** (community)| Popular libs, community-sourced | Any library, any author         |

**Tier 1 / main** — for libraries that are the undeniable standard (e.g., `fmtlib/fmt`, `nlohmann/json`, `spdlog`). These are reviewed and maintained by the LibSkills team.

**Tier 2 / main** — for standard libraries where the skill is community-contributed. Merged after CI validation.

**Tier 2 / contrib** — for any library. Open to everyone. Merged after CI validation.

## Pull Request Process

1. Ensure your skill file passes the JSON schema validation.
2. Ensure your entry in `index.json` is correct (path, tier, group, versions).
3. Your PR will be reviewed within 3-5 business days.
4. Tier 1 PRs require 2 approvals. Tier 2 PRs require 1 approval.
5. Once merged, the index is rebuilt automatically via GitHub Actions.

## Style Guide

- All skill files must be in **English**.
- Use **JSON** format (`.json` extension).
- Follow the schema defined in `SPEC.md`.
- Use consistent field ordering as shown in the schema.
- Keep descriptions concise but informative.

## Getting Help

- Open a [GitHub Discussion](https://github.com/LibSkills/LibSkills/discussions)
- Join our community (link TBD)
- Check [SPEC.md](SPEC.md) for format specifics

# LibSkills Skill Format Specification v1

This document defines the schema and semantics of a LibSkills skill file. Every skill must conform to this specification.

---

## 1. File Format

Skills are stored as JSON files with a `.json` extension. The file name should match the library name (e.g., `fmt.json`, `spdlog.json`).

## 2. File Location

```
registry/{group}/{language}/{author}/{name}.json
```

- `group`: `main` or `contrib`
- `language`: `cpp`, `rust`, `python`, `go`, `js` (matching the library's primary API language)
- `author`: GitHub username or organization that maintains the library
- `name`: the library name

**Examples:**
- `registry/main/cpp/nlohmann/json.json`
- `registry/main/rust/serde/serde.json`
- `registry/contrib/python/tiangolo/fastapi.json`

## 3. Schema

### 3.1 Top-level Structure

```jsonc
{
  "$schema": "https://libskills.dev/schemas/v1/skill.json",
  "libskills": "1.0",

  "skill": {
    "name": "<string>",
    "version": "<semver>",
    "tier": 1 | 2,
    "group": "main" | "contrib"
  },

  "library": {
    "name": "<string>",
    "language": "<string>",
    "repo": "<string>",
    "homepage": "<string>",
    "license": "<string>",
    "versions": ["<string>"],
    "description": "<string>"
  },

  "usage": {
    "minimal_example": "<code block or description>",
    "configuration": "<string>",
    "anti_patterns": ["<string>"]
  },

  "risks": {
    "crash_prone_patterns": ["<string>"],
    "leaks": ["<string>"],
    "thread_unsafe": ["<string>"],
    "exception_paths": ["<string>"]
  },

  "performance": {
    "blocking": true | false,
    "async_support": true | false,
    "allocation_pattern": "<string>",
    "known_limits": ["<string>"]
  },

  "errors": {
    "common_issues": [
      {
        "title": "<string>",
        "symptoms": "<string>",
        "cause": "<string>",
        "solution": "<string>"
      }
    ],
    "edge_cases": ["<string>"]
  },

  "safety": {
    "red_lines": ["<string>"],
    "deprecated_apis": ["<string>"],
    "version_breaking_changes": [
      {
        "from": "<version>",
        "to": "<version>",
        "changes": ["<string>"]
      }
    ]
  },

  "dependencies": {
    "required": ["<string>"],
    "optional": ["<string>"],
    "platform_specific": ["<string>"]
  },

  "maintainers": ["<string>"],
  "updated": "<ISO 8601 timestamp>"
}
```

### 3.2 Required Fields

Only these fields are **required**:

- `libskills` (version of this spec the skill targets)
- `skill.name`
- `skill.version`
- `skill.tier`
- `skill.group`
- `library.name`
- `library.language`
- `library.repo`
- `library.versions`
- `usage.minimal_example`
- `safety.red_lines`
- `updated`

All other fields are optional but **strongly encouraged**. The more complete a skill is, the better an AI agent can use it.

### 3.3 Field Semantics

#### `skill.version`
The version of this *skill file*, not the library version. Follows semver. Increment when:
- **Major**: Breaking change to the skill format or when the library has a breaking API change
- **Minor**: Adding new sections, examples, or patterns
- **Patch**: Fixing typos, adding edge cases, minor corrections

#### `tier`
- `1`: Officially curated by LibSkills maintainers. Every field is verified.
- `2`: Community-contributed. Verified for format compliance only.

#### `group`
- `main`: The library is a de-facto standard. Example: `fmtlib/fmt` for C++ formatting.
- `contrib`: Smaller, niche, or alternative libraries.

#### `library.versions`
An array of supported library version ranges. Use semver range syntax:
```jsonc
"versions": ["1.x", "2.0-2.5"]
```

#### `usage.minimal_example`
The shortest possible working code snippet. Should compile/run without additional setup.

#### `usage.anti_patterns`
Common mistakes developers and AI agents make with this library.

#### `safety.red_lines`
Conditions or patterns that must NEVER be used. If an AI agent encounters these in its generation, it should stop and warn the user.

## 4. Index File (`index.json`)

The index file is the entry point for the CLI.

```jsonc
{
  "version": 1,
  "spec_version": "1.0",
  "updated": "2026-04-25T00:00:00Z",
  "skills": {
    "cpp/nlohmann/json": {
      "group": "main",
      "tier": 1,
      "repo": "nlohmann/json",
      "description": "JSON for Modern C++",
      "versions": ["3.x"],
      "languages": ["cpp"],
      "path": "registry/main/cpp/nlohmann/json.json",
      "skill_version": "1.0.0"
    },
    "cpp/spdlog": {
      "group": "main",
      "tier": 1,
      "repo": "gabime/spdlog",
      "description": "Fast C++ logging library",
      "versions": ["1.x"],
      "languages": ["cpp"],
      "path": "registry/main/cpp/spdlog/spdlog.json",
      "skill_version": "1.0.0"
    }
  }
}
```

The index is sorted alphabetically by the full key (`language/name`).

## 5. Full Example

```jsonc
{
  "libskills": "1.0",
  "skill": {
    "name": "json",
    "version": "1.0.0",
    "tier": 1,
    "group": "main"
  },
  "library": {
    "name": "nlohmann/json",
    "language": "cpp",
    "repo": "nlohmann/json",
    "homepage": "https://json.nlohmann.me",
    "license": "MIT",
    "versions": ["3.x"],
    "description": "JSON for Modern C++ — header-only, intuitive syntax, full JSON support."
  },
  "usage": {
    "minimal_example": "```cpp\n#include <nlohmann/json.hpp>\nusing json = nlohmann::json;\n\nauto j = json::parse(R\"({\"pi\":3.14})\");\ndouble pi = j[\"pi\"];\n```",
    "configuration": "Header-only. No build config needed. Add `#include <nlohmann/json.hpp>`.",
    "anti_patterns": [
      "Using `j[\"key\"]` without checking if the key exists (throws `json::out_of_range`). Prefer `.value(\"key\", default)` or `.contains(\"key\")`.",
      "Copying large JSON objects. Use `std::move` or reference semantics."
    ]
  },
  "risks": {
    "crash_prone_patterns": [
      "Accessing a non-existent key with `operator[]` on a `const` object (compilation error on const, throws on non-const)."
    ],
    "leaks": [
      "No known leak patterns when using standard constructors/destructors."
    ],
    "thread_unsafe": [
      "Individual `json` objects are not thread-safe. Use external synchronization when sharing across threads."
    ],
    "exception_paths": [
      "`json::parse()` throws `json::parse_error` on invalid input. Use the `std::nothrow` overload or catch by reference."
    ]
  },
  "performance": {
    "blocking": false,
    "async_support": false,
    "allocation_pattern": "Dynamic allocation per object/array. May cause fragmentation on large documents.",
    "known_limits": [
      "Very deep nesting (> 1024 levels) may cause stack overflow during recursive operations.",
      "Parsing untrusted input with the default parser may be slow on pathological inputs. Consider SAX parser for streaming."
    ]
  },
  "errors": {
    "common_issues": [
      {
        "title": "Missing key access throws exception",
        "symptoms": "Unhandled `json::out_of_range` at runtime",
        "cause": "Using `operator[]` on a key that doesn't exist",
        "solution": "Use `.value(\"key\", default_value)` or check `.contains(\"key\")` first"
      },
      {
        "title": "Parsing failure on malformed JSON",
        "symptoms": "`json::parse_error` exception",
        "cause": "Invalid JSON input",
        "solution": "Validate input first, or use `json::parse(json_string, nullptr, false)` which returns `nullptr` on failure instead of throwing"
      }
    ],
    "edge_cases": [
      "JSON numbers beyond `double` precision may lose precision. Use `j.get<long double>()` if needed.",
      "Comments are not supported in standard JSON. Use a preprocessor if needed."
    ]
  },
  "safety": {
    "red_lines": [
      "Do NOT use `json::accept()` alone for security-critical validation — it only checks syntax, not semantics.",
      "Do NOT use `dump(-1)` without limiting depth — may cause stack overflow on deeply nested objects."
    ],
    "deprecated_apis": [],
    "version_breaking_changes": []
  },
  "dependencies": {
    "required": ["C++11 or later"],
    "optional": [],
    "platform_specific": []
  },
  "maintainers": ["nlohmann"],
  "updated": "2026-04-25T00:00:00Z"
}
```

## 6. Validation Rules

- `skill.version` must follow semantic versioning (`MAJOR.MINOR.PATCH`).
- `library.versions` must use valid semver range syntax.
- `tier` must be `1` or `2`.
- `group` must be `main` or `contrib`.
- `updated` must be a valid ISO 8601 timestamp.
- All required fields must be present and non-empty.
- `safety.red_lines` must contain at least one entry.

## 7. Future Extensions

- **Multi-language libraries**: A single skill may include multiple language sections via an optional `bindings` field.
- **Macros**: Macro-heavy C/C++ libraries may include a `macros` section.
- **Testing**: Testing patterns and test doubles may be added as a `testing` section.

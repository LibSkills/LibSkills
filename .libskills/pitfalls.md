# LibSkills — Pitfalls

Common mistakes AI agents make when using LibSkills.

### Do NOT skip `libskills update` before searching

The local registry index must be refreshed to find skills. Without `update`, `search` and `find` return nothing.

```bash
# BAD: no results
libskills search logging
# → No local index found. Run 'libskills update' first.

# GOOD: update then search
libskills update
libskills search logging
```

### Do NOT forget `--registry` when auto-detection fails

libskills auto-detects the registry from sibling directories. If it can't find it, pass `--registry` explicitly.

```bash
# BAD: silent failure
libskills get cpp/gabime/spdlog
# → Could not find libskills-registry.

# GOOD: explicit path
libskills get cpp/gabime/spdlog --registry /path/to/libskills-registry
```

### Do NOT assume `search` searches skill file contents

`search` matches name, tags, and summary. For content-based search, use `find`.

```bash
# BAD: searching for a pitfall description
libskills search "static destructor crash"
# → No results (searches metadata, not content)

# GOOD: use find for content
libskills find "static destructor crash"
# → cpp/gabime/spdlog (100%)
```

### Do NOT skip `validate` before committing .libskills/

If you create a skill for your own library, always validate and lint before committing.

```bash
# BAD: commit without checking
git add .libskills/ && git commit -m "add skill"

# GOOD: validate first
libskills validate .libskills/
libskills lint --fix .libskills/
git add .libskills/ && git commit -m "add skill"
```

### Do NOT use the CLI as root

The CLI stores data in `~/.libskills/`. Running as root writes to `/root/.libskills/` — different cache, confusing behavior.

### Do NOT assume all skills are cached after `update`

`update` only downloads the index. Skills are downloaded individually with `get` or auto-discovered by MCP.

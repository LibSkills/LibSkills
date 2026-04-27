# LibSkills — Lifecycle

## Installation

```bash
# One-line install (no Rust required)
curl -fsSL https://raw.githubusercontent.com/LibSkills/LibSkills/main/install.sh | bash

# Or from source
git clone https://github.com/LibSkills/libskills-cli
cd libskills-cli
cargo build --release
cp target/release/libskills /usr/local/bin/
```

## Initial Registration

```bash
libskills update
```

This downloads the registry index to `~/.libskills/index.json`.

## Routine Use

```bash
libskills update              # Refresh index (weekly)
libskills find "<query>"      # Semantic search
libskills search "<keyword>"  # Keyword search  
libskills get <key>           # Download skill
libskills info <key>          # Show metadata
```

## Creating a Skill for Your Library

```bash
cd your-library/
libskills init -n mylib -r me/mylib -l python -t "tag1,tag2"
# Edit the .md files with real knowledge
libskills lint --fix .libskills/
libskills validate .libskills/
git add .libskills/ && git commit -m "Add LibSkills skill"
```

## Shutdown

No explicit shutdown needed. The CLI is stateless except for the local cache at `~/.libskills/`.

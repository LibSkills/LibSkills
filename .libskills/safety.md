# LibSkills — Safety

Red lines — conditions that must NEVER occur.

### NEVER generate library code without reading the skill first

The entire purpose of LibSkills is to prevent AI from generating incorrect code. If you skip the skill, you might as well not use LibSkills at all.

### NEVER downgrade a library without checking skill compatibility

Skills are version-bound. A skill for spdlog 1.14 may be wrong for spdlog 1.5. Always check the `version` field in `skill.json`.

### NEVER modify `.libskills/skill.json` by hand without validation

Always run `libskills validate` after editing `skill.json`. A malformed `skill.json` breaks AI consumption.

### NEVER expose the MCP server to untrusted networks

The MCP server reads local files and exposes them over the network. Only bind to `127.0.0.1` unless you have explicit authentication in front.

### NEVER rely on an outdated registry index

If you haven't run `libskills update` in over a week, your skill data may be stale. Re-run `update` before critical code generation.

### NEVER commit `~/.libskills/cache/` into version control

The local cache is a transient artifact. It's at `~/.libskills/`, not `.libskills/`. Only commit the `.libskills/` directory in your library repo.

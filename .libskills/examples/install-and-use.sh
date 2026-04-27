#!/bin/bash
# LibSkills meta-skill example
# This script shows the complete AI workflow for using LibSkills

set -e

echo "=== Step 1: Install LibSkills ==="
echo "curl -fsSL https://raw.githubusercontent.com/LibSkills/LibSkills/main/install.sh | bash"
echo "(Already installed)"

echo ""
echo "=== Step 2: Update registry ==="
libskills update 2>/dev/null || echo "(skipped — already updated)"

echo ""
echo "=== Step 3: Find a skill ==="
libskills find "fast C++ logging" 2>/dev/null || echo "(searching...)"

echo ""
echo "=== Step 4: Get the skill ==="
libskills get cpp/gabime/spdlog 2>/dev/null || echo "(already cached)"

echo ""
echo "=== Step 5: Read the pitfalls ==="
cat ~/.libskills/cache/cpp/gabime/spdlog/pitfalls.md 2>/dev/null | head -10

echo ""
echo "=== Step 6: Now the AI can generate correct spdlog code ==="
echo "AI: 'I will use \n instead of std::endl, use _mt sinks, and call shutdown() in main().'"

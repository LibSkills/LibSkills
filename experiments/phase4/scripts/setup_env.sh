#!/bin/bash

# Phase 4 Experiment Environment Setup Script
# This script sets up the environment needed to run the experiments

set -e  # Exit on error

echo "=========================================="
echo "Phase 4: Value Validation Experiment Setup"
echo "=========================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[✓]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[!]${NC} $1"
}

print_error() {
    echo -e "${RED}[✗]${NC} $1"
}

# Check prerequisites
echo ""
echo "Checking prerequisites..."

# Check Python
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    print_status "Python 3 found: $PYTHON_VERSION"
else
    print_error "Python 3 is required but not installed."
    print_warning "Install from https://python.org"
    exit 1
fi

# Check pip
if command -v pip3 &> /dev/null; then
    print_status "pip3 found"
else
    print_error "pip3 is required but not installed."
    print_warning "Install with: python3 -m ensurepip --upgrade"
    exit 1
fi

# Check compiler based on platform
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux
    if command -v g++ &> /dev/null; then
        print_status "g++ found"
    else
        print_warning "g++ not found. Install with: sudo apt install g++"
    fi
elif [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    if command -v g++ &> /dev/null || command -v clang++ &> /dev/null; then
        print_status "C++ compiler found"
    else
        print_warning "C++ compiler not found. Install with: xcode-select --install"
    fi
elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    # Windows
    print_warning "Windows detected. Make sure you have g++ in PATH (MinGW or MSYS2)"
fi

# Check Rust
if command -v rustc &> /dev/null; then
    RUST_VERSION=$(rustc --version | cut -d' ' -f2)
    print_status "Rust found: $RUST_VERSION"
else
    print_warning "Rust not found. Install with: curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh"
fi

# Check Git
if command -v git &> /dev/null; then
    print_status "Git found"
else
    print_warning "Git not found. Some features may not work."
fi

echo ""
echo "Installing Python dependencies..."

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    print_status "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
print_status "Activating virtual environment..."
source venv/bin/activate

# Install requirements
print_status "Installing dependencies..."
pip install --upgrade pip
pip install requests openai anthropic python-dotenv

echo ""
echo "Setting up environment file..."

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    cat > .env << 'EOF'
# API Keys for AI services
# Get your keys from:
# - OpenAI: https://platform.openai.com/api-keys
# - Anthropic: https://console.anthropic.com/

# OpenAI API Key (for GPT-4)
OPENAI_API_KEY=your-openai-api-key-here

# Anthropic API Key (for Claude)
ANTHROPIC_API_KEY=your-anthropic-api-key-here

# Optional: Specify which model to use
# OPENAI_MODEL=gpt-4
# ANTHROPIC_MODEL=claude-3-opus-20240229
EOF
    print_status "Created .env file - please add your API keys"
else
    print_status ".env file already exists"
fi

echo ""
echo "Setting up data directory..."

# Create data directory structure
mkdir -p data/results
mkdir -p data/prompts
mkdir -p data/generated

print_status "Data directory structure created"

echo ""
echo "Checking experiment configuration..."

# Verify tasks file exists
if [ -f "tasks/experiment_tasks.json" ]; then
    TASK_COUNT=$(grep -c '"id"' tasks/experiment_tasks.json || true)
    print_status "Found $TASK_COUNT tasks in experiment_tasks.json"
else
    print_error "tasks/experiment_tasks.json not found!"
    exit 1
fi

# Verify skills directory
if [ -d "../../../libskills-registry/skills" ]; then
    SKILL_COUNT=$(find ../../../libskills-registry/skills -name "skill.json" | wc -l | tr -d ' ')
    print_status "Found $SKILL_COUNT skills in registry"
else
    print_warning "Skills registry not found at expected location"
    print_warning "You may need to adjust --skills path when running experiments"
fi

echo ""
echo "=========================================="
echo "Setup Complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Edit .env and add your API keys"
echo "2. Activate the virtual environment:"
echo "   source venv/bin/activate"
echo "3. Run a test:"
echo "   python scripts/run_experiment.py --tasks tasks/experiment_tasks.json --trials 1"
echo "4. Run full experiment:"
echo "   python scripts/run_experiment.py --tasks tasks/experiment_tasks.json --trials 10"
echo ""
echo "To deactivate virtual environment later:"
echo "   deactivate"
echo ""

# Check if .env has been configured
if grep -q "your-openai-api-key-here" .env || grep -q "your-anthropic-api-key-here" .env; then
    print_warning "Remember to update your API keys in .env before running experiments!"
fi
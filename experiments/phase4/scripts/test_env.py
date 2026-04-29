#!/usr/bin/env python3
"""
Test environment setup for Phase 4 experiments.
This script verifies that all dependencies are installed correctly.
"""

import sys
import os
from pathlib import Path

# ANSI colors
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'

def print_success(msg):
    print(f"{Colors.GREEN}[OK] {msg}{Colors.END}")

def print_error(msg):
    print(f"{Colors.RED}[ERROR] {msg}{Colors.END}")

def print_warning(msg):
    print(f"{Colors.YELLOW}[WARN] {msg}{Colors.END}")

def print_info(msg):
    print(f"{Colors.BLUE}[INFO] {msg}{Colors.END}")

def test_python_version():
    """Check Python version."""
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print_success(f"Python {version.major}.{version.minor}.{version.micro} (OK)")
        return True
    else:
        print_error(f"Python {version.major}.{version.minor}.{version.micro} (Need 3.8+)")
        return False

def test_imports():
    """Test required imports."""
    required = ['json', 'pathlib']
    optional = ['requests', 'openai', 'anthropic']
    
    all_ok = True
    
    # Test required imports
    for module in required:
        try:
            __import__(module)
            print_success(f"Module '{module}' available")
        except ImportError:
            print_error(f"Module '{module}' not available (required)")
            all_ok = False
    
    # Test optional imports
    for module in optional:
        try:
            __import__(module)
            print_success(f"Module '{module}' available")
        except ImportError:
            print_warning(f"Module '{module}' not available (optional)")
    
    return all_ok

def test_files():
    """Check that required files exist."""
    base_dir = Path(__file__).parent.parent
    required_files = [
        base_dir / 'tasks' / 'experiment_tasks.json',
        base_dir / 'REPORT.md',
        base_dir / '..' / 'phase4-design.md'
    ]
    
    all_ok = True
    for file_path in required_files:
        if file_path.exists():
            print_success(f"File exists: {file_path.name}")
        else:
            print_error(f"File missing: {file_path.name}")
            all_ok = False
    
    return all_ok

def test_skills_registry():
    """Check if skills registry is accessible."""
    base_dir = Path(__file__).parent.parent
    registry_path = base_dir / '..' / '..' / 'libskills-registry' / 'skills'
    
    if registry_path.exists():
        skills_count = len(list(registry_path.rglob('skill.json')))
        print_success(f"Skills registry found ({skills_count} skills)")
        return True
    else:
        print_warning(f"Skills registry not found at {registry_path}")
        print_info("You can still run experiments, but skills may not be available")
        return False

def test_env_file():
    """Check .env file."""
    base_dir = Path(__file__).parent.parent
    env_file = base_dir / '.env'
    
    if env_file.exists():
        content = env_file.read_text()
        has_openai = 'OPENAI_API_KEY' in content and 'your-openai-api-key' not in content
        has_anthropic = 'ANTHROPIC_API_KEY' in content and 'your-anthropic-api-key' not in content
        
        if has_openai:
            print_success("OpenAI API key configured")
        else:
            print_warning("OpenAI API key not configured")
        
        if has_anthropic:
            print_success("Anthropic API key configured")
        else:
            print_warning("Anthropic API key not configured")
        
        return has_openai or has_anthropic
    else:
        print_warning(".env file not found")
        print_info("Run setup_env.sh to create it")
        return False

def main():
    print("\n" + "=" * 60)
    print("Phase 4 Experiment Environment Test")
    print("=" * 60 + "\n")
    
    results = {
        'python': test_python_version(),
        'imports': test_imports(),
        'files': test_files(),
        'registry': test_skills_registry(),
        'env': test_env_file()
    }
    
    print("\n" + "=" * 60)
    print("Summary")
    print("=" * 60 + "\n")
    
    critical = ['python', 'imports', 'files']
    critical_ok = all(results[k] for k in critical if k in results)
    
    if critical_ok:
        print_success("Environment is ready for experiments!")
        if not results['registry']:
            print_warning("Skills registry not found - some features may be limited")
        if not results['env']:
            print_warning("API keys not configured - add them to .env file")
    else:
        print_error("Environment has critical issues. Please fix before running experiments.")
        return 1
    
    print("\nNext steps:")
    print("1. Activate virtual environment (if using):")
    print("   source venv/bin/activate")
    print("2. Run a test experiment:")
    print("   python scripts/run_experiment.py --tasks tasks/experiment_tasks.json --trials 1")
    print("3. Run full experiment:")
    print("   python scripts/run_experiment.py --tasks tasks/experiment_tasks.json --trials 10")
    
    return 0

if __name__ == '__main__':
    exit(main())
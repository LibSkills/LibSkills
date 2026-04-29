#!/usr/bin/env python3
"""
Test script for Xiaomi MiMo-V2.5 API integration.
"""

import sys
import os

# Add the scripts directory to path
sys.path.insert(0, os.path.dirname(__file__))

from xiaomi_api import test_xiaomi_api, XiaomiClient, load_config_from_env, create_system_prompt

def test_basic_generation():
    """Test basic code generation with MiMo-V2.5."""
    print("\n" + "=" * 60)
    print("Testing Basic Code Generation")
    print("=" * 60)
    
    try:
        config = load_config_from_env()
        client = XiaomiClient(config)
        
        # Simple test prompt
        prompt = "Write a simple Python function that calculates the factorial of a number."
        system_prompt = create_system_prompt("python", with_skill=False)
        
        print(f"Prompt: {prompt[:50]}...")
        print("Sending request to MiMo-V2.5...")
        
        result = client.generate_code(prompt, system_prompt)
        
        if result.get('success'):
            print("\n" + "-" * 60)
            print("SUCCESS!")
            print("-" * 60)
            print(f"Model: {result.get('model', 'unknown')}")
            print(f"Response time: {result.get('response_time', 0):.2f}s")
            print(f"Tokens used: {result.get('usage', {}).get('total_tokens', 'unknown')}")
            print("\nGenerated code:")
            print("-" * 40)
            
            # Extract and show code
            code = client.extract_code(result['content'], 'python')
            print(code[:500] + ("..." if len(code) > 500 else ""))
            
            return True
        else:
            print(f"Failed: {result.get('error', 'Unknown error')}")
            return False
            
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_with_skill():
    """Test code generation with skill documentation."""
    print("\n" + "=" * 60)
    print("Testing with Skill Documentation")
    print("=" * 60)
    
    try:
        config = load_config_from_env()
        client = XiaomiClient(config)
        
        # Test prompt with skill context
        prompt = """You are an expert Python developer.

Before writing code, read this library skill documentation carefully:

=== skill.json ===
{
  "name": "requests",
  "language": "python",
  "version": "2.31.0"
}

=== pitfalls.md ===
# requests - Pitfalls

## Always set timeout
Never make requests without a timeout. A default timeout of 30 seconds is recommended.

## Use session for multiple requests
For multiple requests to the same host, use a Session object for connection pooling.

## Handle exceptions properly
Always handle ConnectionError, Timeout, and HTTPError exceptions.

Now, complete this task:

Task: Make a GET request to https://api.github.com with proper error handling and timeout.

Language: python
Library: requests

Please write a complete, working implementation. Include:
1. All necessary imports
2. Error handling
3. Comments explaining the approach

The code should compile and run without errors.
"""
        
        system_prompt = create_system_prompt("python", with_skill=True)
        
        print("Testing with skill documentation...")
        print("Sending request to MiMo-V2.5...")
        
        result = client.generate_code(prompt, system_prompt)
        
        if result.get('success'):
            print("\n" + "-" * 60)
            print("SUCCESS!")
            print("-" * 60)
            print(f"Response time: {result.get('response_time', 0):.2f}s")
            print("\nGenerated code:")
            print("-" * 40)
            
            code = client.extract_code(result['content'], 'python')
            print(code[:500] + ("..." if len(code) > 500 else ""))
            
            # Check if skill guidelines were followed
            print("\nSkill compliance check:")
            if "timeout" in code.lower():
                print("  ✓ Timeout handling included")
            else:
                print("  ✗ Timeout handling missing")
            
            if "exception" in code.lower() or "error" in code.lower() or "try:" in code:
                print("  ✓ Error handling included")
            else:
                print("  ✗ Error handling missing")
            
            return True
        else:
            print(f"Failed: {result.get('error', 'Unknown error')}")
            return False
            
    except Exception as e:
        print(f"Error: {e}")
        return False

def main():
    print("=" * 60)
    print("Xiaomi MiMo-V2.5 API Test")
    print("=" * 60)
    
    # Test 1: Connection
    print("\n1. Testing API connection...")
    if not test_xiaomi_api():
        print("\nConnection test failed. Please check your API key and network.")
        return 1
    
    # Test 2: Basic generation
    print("\n2. Testing basic code generation...")
    if not test_basic_generation():
        print("\nBasic generation test failed.")
        return 1
    
    # Test 3: With skill documentation
    print("\n3. Testing with skill documentation...")
    if not test_with_skill():
        print("\nSkill generation test failed.")
        return 1
    
    print("\n" + "=" * 60)
    print("All tests passed! ✓")
    print("=" * 60)
    print("\nYou can now run the full experiment:")
    print("python run_xiaomi_experiment.py --tasks tasks/experiment_tasks.json --trials 1")
    
    return 0

if __name__ == '__main__':
    exit(main())
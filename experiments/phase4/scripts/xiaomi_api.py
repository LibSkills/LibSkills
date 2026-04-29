"""
Xiaomi MiMo-V2.5 API Client for LibSkills Experiments

This module provides a client for interacting with Xiaomi's MiMo-V2.5 model
for the Phase 4 value validation experiments.
"""

import os
import json
import requests
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime


@dataclass
class XiaomiConfig:
    """Configuration for Xiaomi API."""
    api_key: str
    base_url: str = "https://api.xiaoai.mi.com/v1"  # Default endpoint
    model: str = "mimo-v2.5"  # Default model
    max_tokens: int = 2000
    temperature: float = 0.7
    timeout: int = 120  # seconds


class XiaomiClient:
    """Client for Xiaomi MiMo-V2.5 API."""
    
    def __init__(self, config: XiaomiConfig):
        self.config = config
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {config.api_key}",
            "Content-Type": "application/json",
            "User-Agent": "LibSkills-Experiment/1.0"
        })
    
    def generate_code(self, prompt: str, system_prompt: Optional[str] = None) -> Dict[str, Any]:
        """
        Generate code using MiMo-V2.5 model.
        
        Args:
            prompt: The user prompt containing the task description
            system_prompt: Optional system prompt to guide the model
            
        Returns:
            Dictionary containing the generated code and metadata
        """
        messages = []
        
        if system_prompt:
            messages.append({
                "role": "system",
                "content": system_prompt
            })
        
        messages.append({
            "role": "user",
            "content": prompt
        })
        
        payload = {
            "model": self.config.model,
            "messages": messages,
            "max_tokens": self.config.max_tokens,
            "temperature": self.config.temperature,
            "stream": False
        }
        
        start_time = datetime.now()
        
        try:
            response = self.session.post(
                f"{self.config.base_url}/chat/completions",
                json=payload,
                timeout=self.config.timeout
            )
            response.raise_for_status()
            
            result = response.json()
            end_time = datetime.now()
            
            # Extract the response
            if "choices" in result and len(result["choices"]) > 0:
                content = result["choices"][0]["message"]["content"]
                
                return {
                    "success": True,
                    "content": content,
                    "model": result.get("model", self.config.model),
                    "usage": result.get("usage", {}),
                    "response_time": (end_time - start_time).total_seconds(),
                    "raw_response": result
                }
            else:
                return {
                    "success": False,
                    "error": "No response content",
                    "raw_response": result
                }
                
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "error": str(e),
                "response_time": (datetime.now() - start_time).total_seconds()
            }
    
    def extract_code(self, response: str, language: str) -> str:
        """
        Extract code from the model's response.
        
        Args:
            response: The full response from the model
            language: The programming language (cpp, rust, python)
            
        Returns:
            Extracted code string
        """
        # Try to find code blocks
        code_blocks = []
        in_code_block = False
        current_block = []
        
        for line in response.split('\n'):
            if '```' in line:
                if in_code_block:
                    # End of code block
                    code_blocks.append('\n'.join(current_block))
                    current_block = []
                    in_code_block = False
                else:
                    # Start of code block
                    in_code_block = True
            elif in_code_block:
                current_block.append(line)
        
        # If we found code blocks, return the first one
        if code_blocks:
            return code_blocks[0]
        
        # If no code blocks found, try to extract based on language
        if language == 'python':
            # Look for Python code patterns
            lines = response.split('\n')
            code_lines = []
            for line in lines:
                if any(keyword in line for keyword in ['import ', 'from ', 'def ', 'class ', 'if __name__']):
                    code_lines.append(line)
            if code_lines:
                return '\n'.join(code_lines)
        
        # Return the whole response as fallback
        return response
    
    def test_connection(self) -> Dict[str, Any]:
        """
        Test the API connection with a simple request.
        
        Returns:
            Dictionary with test results
        """
        test_prompt = "Hello, please respond with 'OK' to confirm connection."
        
        result = self.generate_code(test_prompt)
        
        return {
            "connected": result.get("success", False),
            "model": self.config.model,
            "response_time": result.get("response_time", 0),
            "error": result.get("error")
        }


def load_config_from_env() -> XiaomiConfig:
    """
    Load configuration from environment variables.
    
    Returns:
        XiaomiConfig object
    """
    api_key = os.getenv("XIAOMI_API_KEY")
    
    if not api_key:
        raise ValueError("XIAOMI_API_KEY environment variable is required")
    
    base_url = os.getenv("XIAOMI_BASE_URL", "https://api.xiaoai.mi.com/v1")
    model = os.getenv("XIAOMI_MODEL", "mimo-v2.5")
    
    return XiaomiConfig(
        api_key=api_key,
        base_url=base_url,
        model=model
    )


def create_system_prompt(language: str, with_skill: bool = False) -> str:
    """
    Create a system prompt for code generation.
    
    Args:
        language: Programming language (cpp, rust, python)
        with_skill: Whether skills are available
        
    Returns:
        System prompt string
    """
    language_names = {
        "cpp": "C++",
        "rust": "Rust",
        "python": "Python"
    }
    
    lang_name = language_names.get(language, language)
    
    base_prompt = f"""You are an expert {lang_name} developer. 
Generate clean, efficient, and well-documented code.
Always include error handling and follow best practices.
Provide complete, working implementations that compile/run successfully."""
    
    if with_skill:
        base_prompt += """
        
IMPORTANT: Read the provided library skill documentation carefully.
Follow all the guidelines, pitfalls, and best practices mentioned.
Your code MUST comply with the safety rules and avoid known pitfalls."""
    
    return base_prompt


def test_xiaomi_api():
    """Test the Xiaomi API connection."""
    print("Testing Xiaomi MiMo-V2.5 API connection...")
    
    try:
        config = load_config_from_env()
        client = XiaomiClient(config)
        
        print(f"Model: {config.model}")
        print(f"Base URL: {config.base_url}")
        
        result = client.test_connection()
        
        if result["connected"]:
            print(f"✓ Connection successful! Response time: {result['response_time']:.2f}s")
            return True
        else:
            print(f"✗ Connection failed: {result.get('error', 'Unknown error')}")
            return False
            
    except ValueError as e:
        print(f"✗ Configuration error: {e}")
        return False
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        return False


if __name__ == "__main__":
    # Test the API
    test_xiaomi_api()
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
from pathlib import Path

# Import API configuration
try:
    from api_config import get_api_config, load_env_file, APIConfig
except ImportError:
    # Fallback if api_config is not available
    APIConfig = None


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
        
        # Try multiple API endpoints
        endpoints = [
            f"{self.config.base_url}/chat/completions",
            f"{self.config.base_url}/completions",
            f"{self.config.base_url}/generate"
        ]
        
        for endpoint in endpoints:
            try:
                response = self.session.post(
                    endpoint,
                    json=payload,
                    timeout=self.config.timeout,
                    verify=True  # SSL verification
                )
                
                if response.status_code == 200:
                    result = response.json()
                    end_time = datetime.now()
                    
                    # Extract the response (handle different response formats)
                    if "choices" in result and len(result["choices"]) > 0:
                        content = result["choices"][0].get("message", {}).get("content", "")
                        if not content:
                            content = result["choices"][0].get("text", "")
                        
                        return {
                            "success": True,
                            "content": content,
                            "model": result.get("model", self.config.model),
                            "usage": result.get("usage", {}),
                            "response_time": (end_time - start_time).total_seconds(),
                            "raw_response": result
                        }
                    elif "text" in result:
                        return {
                            "success": True,
                            "content": result["text"],
                            "model": result.get("model", self.config.model),
                            "usage": result.get("usage", {}),
                            "response_time": (end_time - start_time).total_seconds(),
                            "raw_response": result
                        }
                    else:
                        continue  # Try next endpoint
                
            except requests.exceptions.RequestException as e:
                continue  # Try next endpoint
        
        # If all endpoints failed
        return {
            "success": False,
            "error": f"All API endpoints failed. Last error: {str(e) if 'e' in locals() else 'Unknown'}",
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


def load_config_from_env(backend: str = "xiaomi") -> XiaomiConfig:
    """
    Load configuration from environment variables and .env file.
    
    Args:
        backend: API backend name (xiaomi, openai, anthropic, mock)
        
    Returns:
        XiaomiConfig object
    """
    # Try to use api_config module if available
    if APIConfig is not None:
        try:
            config = get_api_config(backend)
            return XiaomiConfig(
                api_key=config.api_key,
                base_url=config.base_url,
                model=config.model,
                max_tokens=config.max_tokens,
                temperature=config.temperature,
                timeout=config.timeout
            )
        except Exception:
            pass  # Fall back to manual loading
    
    # Manual loading as fallback
    # Try to load from .env file first
    env_file = Path(__file__).parent.parent / '.env'
    if env_file.exists():
        with open(env_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    key = key.strip()
                    value = value.strip()
                    if key and value:
                        os.environ[key] = value
    
    # Get configuration based on backend
    env_prefix = backend.upper()
    api_key = os.getenv(f"{env_prefix}_API_KEY")
    
    if not api_key:
        raise ValueError(f"{env_prefix}_API_KEY environment variable is required")
    
    base_urls = {
        "xiaomi": "https://api.xiaoai.mi.com/v1",
        "openai": "https://api.openai.com/v1",
        "anthropic": "https://api.anthropic.com",
        "mock": "http://localhost:8000"
    }
    
    models = {
        "xiaomi": "mimo-v2.5",
        "openai": "gpt-4",
        "anthropic": "claude-3-opus-20240229",
        "mock": "mock-model"
    }
    
    base_url = os.getenv(f"{env_prefix}_BASE_URL", base_urls.get(backend, base_urls["xiaomi"]))
    model = os.getenv(f"{env_prefix}_MODEL", models.get(backend, models["xiaomi"]))
    
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
            print(f"[OK] Connection successful! Response time: {result['response_time']:.2f}s")
            return True
        else:
            print(f"[ERROR] Connection failed: {result.get('error', 'Unknown error')}")
            return False
            
    except ValueError as e:
        print(f"[ERROR] Configuration error: {e}")
        return False
    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}")
        return False


if __name__ == "__main__":
    # Test the API
    test_xiaomi_api()
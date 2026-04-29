"""
API Configuration for different AI backends.

This module provides configuration for multiple AI backends including:
- Xiaomi MiMo-V2.5
- OpenAI GPT-4
- Anthropic Claude
- Mock API for testing
"""

import os
from pathlib import Path
from typing import Dict, Optional
from dataclasses import dataclass


@dataclass
class APIConfig:
    """Generic API configuration."""
    name: str
    api_key: str
    base_url: str
    model: str
    max_tokens: int = 2000
    temperature: float = 0.7
    timeout: int = 120


# Known API configurations
KNOWN_APIS = {
    "xiaomi": APIConfig(
        name="Xiaomi MiMo-V2.5",
        api_key=os.getenv("XIAOMI_API_KEY", ""),
        base_url=os.getenv("XIAOMI_BASE_URL", "https://api.xiaoai.mi.com/v1"),
        model=os.getenv("XIAOMI_MODEL", "mimo-v2.5")
    ),
    "openai": APIConfig(
        name="OpenAI GPT-4",
        api_key=os.getenv("OPENAI_API_KEY", ""),
        base_url=os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1"),
        model=os.getenv("OPENAI_MODEL", "gpt-4")
    ),
    "anthropic": APIConfig(
        name="Anthropic Claude",
        api_key=os.getenv("ANTHROPIC_API_KEY", ""),
        base_url=os.getenv("ANTHROPIC_BASE_URL", "https://api.anthropic.com"),
        model=os.getenv("ANTHROPIC_MODEL", "claude-3-opus-20240229"),
        max_tokens=4000  # Claude has different token limits
    ),
    "mock": APIConfig(
        name="Mock API",
        api_key="mock-key",
        base_url="http://localhost:8000",
        model="mock-model"
    )
}


def load_env_file(env_path: Optional[Path] = None) -> None:
    """
    Load environment variables from .env file.
    
    Args:
        env_path: Path to .env file (default: parent directory of this script)
    """
    if env_path is None:
        env_path = Path(__file__).parent.parent / '.env'
    
    if env_path.exists():
        with open(env_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    key = key.strip()
                    value = value.strip()
                    if key and value and key not in os.environ:
                        os.environ[key] = value


def get_api_config(backend: str = "xiaomi") -> APIConfig:
    """
    Get API configuration for the specified backend.
    
    Args:
        backend: API backend name (xiaomi, openai, anthropic, mock)
        
    Returns:
        APIConfig object
    """
    # Load .env file first
    load_env_file()
    
    if backend not in KNOWN_APIS:
        raise ValueError(f"Unknown backend: {backend}. Available: {list(KNOWN_APIS.keys())}")
    
    config = KNOWN_APIS[backend]
    
    # Update with environment variables
    env_prefix = backend.upper()
    if f"{env_prefix}_API_KEY" in os.environ:
        config.api_key = os.environ[f"{env_prefix}_API_KEY"]
    if f"{env_prefix}_BASE_URL" in os.environ:
        config.base_url = os.environ[f"{env_prefix}_BASE_URL"]
    if f"{env_prefix}_MODEL" in os.environ:
        config.model = os.environ[f"{env_prefix}_MODEL"]
    
    return config


def list_available_backends() -> Dict[str, str]:
    """
    List available backends and their status.
    
    Returns:
        Dictionary of backend names and their status
    """
    load_env_file()
    
    status = {}
    for name, config in KNOWN_APIS.items():
        if name == "mock":
            status[name] = "Mock API (always available)"
        elif config.api_key:
            status[name] = f"Configured: {config.model}"
        else:
            status[name] = "Not configured (API key missing)"
    
    return status


if __name__ == "__main__":
    print("API Backend Status:")
    print("-" * 50)
    
    for backend, status in list_available_backends().items():
        print(f"  {backend:12} : {status}")
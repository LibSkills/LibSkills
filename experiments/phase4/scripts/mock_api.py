"""
Mock API Client for testing the experiment framework.

This module provides a mock API client that simulates AI responses
without requiring actual API calls. Useful for testing the experiment
framework and generating sample data.
"""

import random
import time
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime


@dataclass
class MockConfig:
    """Configuration for Mock API."""
    api_key: str = "mock-key"
    base_url: str = "http://localhost:8000"
    model: str = "mock-model"
    max_tokens: int = 2000
    temperature: float = 0.7
    timeout: int = 10  # seconds


class MockClient:
    """Mock client for testing experiment framework."""
    
    def __init__(self, config: MockConfig):
        self.config = config
        self.request_count = 0
    
    def generate_code(self, prompt: str, system_prompt: Optional[str] = None) -> Dict[str, Any]:
        """
        Generate mock code response.
        
        Args:
            prompt: The user prompt
            system_prompt: Optional system prompt
            
        Returns:
            Dictionary containing mock generated code
        """
        self.request_count += 1
        
        # Simulate API delay
        time.sleep(0.5 + random.random() * 1.5)
        
        # Determine language from prompt
        language = "python"
        if "cpp" in prompt.lower() or "c++" in prompt.lower():
            language = "cpp"
        elif "rust" in prompt.lower() and "requests" not in prompt.lower():
            # Avoid matching "requests" when looking for "rust"
            language = "rust"
        
        # Generate mock code based on language
        code = self._generate_mock_code(language, prompt)
        
        # Simulate token usage
        token_count = random.randint(500, 1500)
        
        return {
            "success": True,
            "content": code,
            "model": self.config.model,
            "usage": {
                "total_tokens": token_count,
                "prompt_tokens": random.randint(200, 600),
                "completion_tokens": random.randint(300, 900)
            },
            "response_time": 0.5 + random.random() * 1.5,
            "raw_response": {
                "id": f"mock-{self.request_count}",
                "object": "chat.completion",
                "created": int(datetime.now().timestamp()),
                "model": self.config.model,
                "choices": [{
                    "index": 0,
                    "message": {
                        "role": "assistant",
                        "content": code
                    },
                    "finish_reason": "stop"
                }],
                "usage": {
                    "prompt_tokens": random.randint(200, 600),
                    "completion_tokens": random.randint(300, 900),
                    "total_tokens": token_count
                }
            }
        }
    
    def _generate_mock_code(self, language: str, prompt: str) -> str:
        """Generate mock code based on language."""
        
        if language == "python":
            return '''import requests
import json

def make_api_call(url, timeout=30):
    """
    Make an API call with proper error handling.
    
    Args:
        url: The URL to call
        timeout: Request timeout in seconds
        
    Returns:
        Response data as dictionary
    """
    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.Timeout:
        print("Error: Request timed out")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    result = make_api_call("https://api.example.com/data")
    print(result)
'''
        
        elif language == "cpp":
            return '''#include <iostream>
#include <string>
#include <vector>

class Logger {
public:
    enum Level { DEBUG, INFO, WARN, ERROR };
    
    Logger(const std::string& name) : name_(name), level_(INFO) {}
    
    void set_level(Level level) { level_ = level; }
    
    void log(Level level, const std::string& message) {
        if (level >= level_) {
            std::cout << "[" << level_to_string(level) << "] " 
                      << name_ << ": " << message << std::endl;
        }
    }
    
private:
    std::string name_;
    Level level_;
    
    std::string level_to_string(Level level) {
        switch (level) {
            case DEBUG: return "DEBUG";
            case INFO: return "INFO";
            case WARN: return "WARN";
            case ERROR: return "ERROR";
            default: return "UNKNOWN";
        }
    }
};

int main() {
    Logger logger("MyApp");
    logger.log(Logger::INFO, "Application started");
    logger.log(Logger::ERROR, "An error occurred");
    return 0;
}
'''
        
        elif language == "rust":
            return '''use std::collections::HashMap;

struct Config {
    settings: HashMap<String, String>,
}

impl Config {
    fn new() -> Self {
        Config {
            settings: HashMap::new(),
        }
    }
    
    fn set(&mut self, key: &str, value: &str) {
        self.settings.insert(key.to_string(), value.to_string());
    }
    
    fn get(&self, key: &str) -> Option<&String> {
        self.settings.get(key)
    }
    
    fn load_defaults(&mut self) {
        self.set("host", "localhost");
        self.set("port", "8080");
        self.set("debug", "false");
    }
}

fn main() {
    let mut config = Config::new();
    config.load_defaults();
    
    if let Some(host) = config.get("host") {
        println!("Server will run on: {}", host);
    }
}
'''
        
        return "// Mock code generation" + "\n" + prompt[:100]
    
    def test_connection(self) -> Dict[str, Any]:
        """Test mock API connection."""
        time.sleep(0.2)
        return {
            "connected": True,
            "model": self.config.model,
            "response_time": 0.2
        }
    
    def extract_code(self, response: str, language: str) -> str:
        """Extract code from response (mock implementation)."""
        # For mock, just return the response as-is
        return response


def create_mock_client() -> MockClient:
    """Create a mock client for testing."""
    config = MockConfig()
    return MockClient(config)


if __name__ == "__main__":
    print("Testing Mock API...")
    client = create_mock_client()
    
    result = client.generate_code("Write a Python function to calculate factorial")
    
    if result["success"]:
        print("[OK] Mock API working!")
        print(f"Model: {result['model']}")
        print(f"Tokens: {result['usage']['total_tokens']}")
        print(f"Response time: {result['response_time']:.2f}s")
        print("\nGenerated code:")
        print("-" * 40)
        print(result["content"][:300] + "...")
    else:
        print("[ERROR] Mock API failed")
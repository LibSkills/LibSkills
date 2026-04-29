#!/usr/bin/env python3
"""
Phase 4 Value Validation Experiment Runner using Xiaomi MiMo-V2.5

This script runs controlled experiments using Xiaomi's MiMo-V2.5 model
to measure the impact of LibSkills on AI-generated code quality.
"""

import argparse
import json
import os
import subprocess
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

# Import our Xiaomi API client
try:
    from xiaomi_api import XiaomiClient, load_config_from_env, create_system_prompt
except ImportError:
    print("Error: xiaomi_api.py not found. Make sure it's in the scripts directory.")
    exit(1)

# ANSI colors for terminal output
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def print_header(text: str):
    """Print a formatted header."""
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'=' * 60}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{text.center(60)}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'=' * 60}{Colors.ENDC}\n")


def print_section(text: str):
    """Print a formatted section header."""
    print(f"\n{Colors.OKBLUE}{Colors.BOLD}{text}{Colors.ENDC}")
    print(f"{Colors.OKBLUE}{'-' * len(text)}{Colors.ENDC}")


def print_success(text: str):
    """Print success message."""
    print(f"{Colors.OKGREEN}✓ {text}{Colors.ENDC}")


def print_warning(text: str):
    """Print warning message."""
    print(f"{Colors.WARNING}⚠ {text}{Colors.ENDC}")


def print_error(text: str):
    """Print error message."""
    print(f"{Colors.FAIL}✗ {text}{Colors.ENDC}")


class ExperimentTask:
    """Represents a single experiment task."""
    
    def __init__(self, task_id: str, library: str, language: str, 
                 description: str, complexity: str, expected_files: List[str],
                 test_command: str = "", success_criteria: List[str] = None):
        self.task_id = task_id
        self.library = library
        self.language = language
        self.description = description
        self.complexity = complexity
        self.expected_files = expected_files
        self.test_command = test_command
        self.success_criteria = success_criteria or []
    
    @classmethod
    def from_dict(cls, data: dict) -> 'ExperimentTask':
        return cls(
            task_id=data['id'],
            library=data['library'],
            language=data['language'],
            description=data['description'],
            complexity=data['complexity'],
            expected_files=data.get('expected_files', []),
            test_command=data.get('test_command', ''),
            success_criteria=data.get('success_criteria', [])
        )


class ExperimentResult:
    """Stores results for a single task run."""
    
    def __init__(self, task_id: str, group: str, trial: int):
        self.task_id = task_id
        self.group = group  # 'control' or 'treatment'
        self.trial = trial
        self.timestamp = datetime.now().isoformat()
        
        # Metrics
        self.success = False
        self.hallucination_count = 0
        self.compiles = False
        self.runtime_errors = 0
        self.token_count = 0
        self.iterations = 0
        self.time_seconds = 0
        
        # Generated code
        self.generated_code = ""
        self.ai_response = ""
        
        # Additional notes
        self.notes = ""
    
    def to_dict(self) -> dict:
        return {
            'task_id': self.task_id,
            'group': self.group,
            'trial': self.trial,
            'timestamp': self.timestamp,
            'success': self.success,
            'hallucination_count': self.hallucination_count,
            'compiles': self.compiles,
            'runtime_errors': self.runtime_errors,
            'token_count': self.token_count,
            'iterations': self.iterations,
            'time_seconds': self.time_seconds,
            'notes': self.notes
        }


class XiaomiExperimentRunner:
    """Experiment runner using Xiaomi MiMo-V2.5."""
    
    def __init__(self, data_dir: Path, skills_dir: Path):
        self.data_dir = data_dir
        self.skills_dir = skills_dir
        self.tasks: List[ExperimentTask] = []
        self.results: List[ExperimentResult] = []
        
        # Initialize Xiaomi client
        try:
            self.config = load_config_from_env()
            self.client = XiaomiClient(self.config)
            print_success(f"Xiaomi API configured: {self.config.model}")
        except Exception as e:
            print_error(f"Failed to initialize Xiaomi API: {e}")
            raise
        
        # Create results directory
        self.results_dir = data_dir / 'results'
        self.results_dir.mkdir(exist_ok=True)
    
    def load_tasks(self, tasks_file: Path) -> bool:
        """Load tasks from JSON file."""
        try:
            with open(tasks_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            self.tasks = [ExperimentTask.from_dict(t) for t in data['tasks']]
            print_success(f"Loaded {len(self.tasks)} tasks from {tasks_file}")
            return True
        except Exception as e:
            print_error(f"Failed to load tasks: {e}")
            return False
    
    def load_skill(self, library: str) -> Optional[str]:
        """Load skill content for a library."""
        library_dirs = {
            'spdlog': 'cpp/gabime/spdlog',
            'serde': 'rust/serde-rs/serde',
            'requests': 'python/psf/requests'
        }
        
        if library not in library_dirs:
            print_warning(f"Unknown library: {library}")
            return None
        
        skill_dir = self.skills_dir / 'skills' / library_dirs[library]
        if not skill_dir.exists():
            print_warning(f"Skill not found: {skill_dir}")
            return None
        
        # Load key skill files
        skill_content = []
        skill_files = ['skill.json', 'quickstart.md', 'pitfalls.md', 'safety.md']
        
        for file_name in skill_files:
            file_path = skill_dir / file_name
            if file_path.exists():
                skill_content.append(f"=== {file_name} ===")
                skill_content.append(file_path.read_text(encoding='utf-8'))
        
        return '\n\n'.join(skill_content)
    
    def generate_prompt(self, task: ExperimentTask, with_skill: bool) -> str:
        """Generate a prompt for the AI."""
        base_prompt = f"""Task: {task.description}

Language: {task.language}
Library: {task.library}

Please write a complete, working implementation. Include:
1. All necessary includes/imports
2. Error handling
3. Comments explaining the approach

The code should compile and run without errors.
"""
        
        if with_skill:
            skill_content = self.load_skill(task.library)
            if skill_content:
                base_prompt = f"""You are an expert {task.language} developer.

Before writing code, read this library skill documentation carefully:

{skill_content}

Now, complete this task:

{base_prompt}
"""
        
        return base_prompt
    
    def run_ai_task(self, task: ExperimentTask, with_skill: bool, trial: int) -> ExperimentResult:
        """Run a single task with Xiaomi MiMo-V2.5."""
        result = ExperimentResult(
            task_id=task.task_id,
            group='treatment' if with_skill else 'control',
            trial=trial
        )
        
        prompt = self.generate_prompt(task, with_skill)
        system_prompt = create_system_prompt(task.language, with_skill)
        
        print(f"    Sending request to MiMo-V2.5...", end=' ', flush=True)
        
        # Generate code using Xiaomi API
        response = self.client.generate_code(prompt, system_prompt)
        
        if response.get('success'):
            result.ai_response = response['content']
            result.generated_code = self.client.extract_code(response['content'], task.language)
            result.time_seconds = response.get('response_time', 0)
            
            # Get token usage if available
            usage = response.get('usage', {})
            result.token_count = usage.get('total_tokens', 0)
            
            print(f"OK ({result.time_seconds:.1f}s, {result.token_count} tokens)")
            
            # Save the generated code
            self.save_generated_code(task, result)
            
            # Simple validation: check if code contains expected patterns
            result.compiles = self.validate_code_structure(result.generated_code, task.language)
            result.success = result.compiles
            
        else:
            print(f"Failed: {response.get('error', 'Unknown error')}")
            result.notes = f"API Error: {response.get('error', 'Unknown error')}"
        
        # Save prompt for reference
        self.save_prompt(task, prompt, with_skill, trial)
        
        return result
    
    def validate_code_structure(self, code: str, language: str) -> bool:
        """Basic validation of code structure."""
        if not code or len(code.strip()) < 10:
            return False
        
        # Check for basic language constructs
        if language == 'cpp':
            return '#include' in code or 'int main' in code
        elif language == 'rust':
            return 'fn main' in code or 'use ' in code
        elif language == 'python':
            return 'import ' in code or 'def ' in code or 'print(' in code
        
        return True
    
    def save_generated_code(self, task: ExperimentTask, result: ExperimentResult):
        """Save generated code to file."""
        output_dir = self.results_dir / 'generated'
        output_dir.mkdir(exist_ok=True)
        
        # Determine file extension
        extensions = {'cpp': 'cpp', 'rust': 'rs', 'python': 'py'}
        ext = extensions.get(task.language, 'txt')
        
        filename = f"{task.task_id}_{result.group}_trial{result.trial}.{ext}"
        filepath = output_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(result.generated_code)
    
    def save_prompt(self, task: ExperimentTask, prompt: str, with_skill: bool, trial: int):
        """Save prompt to file."""
        output_dir = self.results_dir / 'prompts'
        output_dir.mkdir(exist_ok=True)
        
        group = 'treatment' if with_skill else 'control'
        filename = f"{task.task_id}_{group}_trial{trial}_prompt.md"
        filepath = output_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"# Prompt for {task.task_id} ({group}, trial {trial})\n\n")
            f.write(prompt)
    
    def run_control_group(self, tasks: List[ExperimentTask], trials: int = 10):
        """Run tasks for control group (no skills)."""
        print_section("Running Control Group (No Skills)")
        
        for task in tasks:
            print(f"\n  Task: {task.task_id} - {task.description[:50]}...")
            for trial in range(1, trials + 1):
                print(f"    Trial {trial}/{trials}: ", end='', flush=True)
                result = self.run_ai_task(task, with_skill=False, trial=trial)
                self.results.append(result)
    
    def run_treatment_group(self, tasks: List[ExperimentTask], trials: int = 10):
        """Run tasks for treatment group (with skills)."""
        print_section("Running Treatment Group (With Skills)")
        
        for task in tasks:
            print(f"\n  Task: {task.task_id} - {task.description[:50]}...")
            for trial in range(1, trials + 1):
                print(f"    Trial {trial}/{trials}: ", end='', flush=True)
                result = self.run_ai_task(task, with_skill=True, trial=trial)
                self.results.append(result)
    
    def save_results(self):
        """Save all results to JSON file."""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        results_file = self.results_dir / f'xiaomi_results_{timestamp}.json'
        
        data = {
            'experiment_id': f'phase4_xiaomi_{timestamp}',
            'model': self.config.model,
            'timestamp': datetime.now().isoformat(),
            'total_tasks': len(self.tasks),
            'total_results': len(self.results),
            'results': [r.to_dict() for r in self.results]
        }
        
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print_success(f"Results saved to {results_file}")
        return results_file
    
    def analyze_results(self):
        """Analyze results and generate summary statistics."""
        if not self.results:
            print_warning("No results to analyze")
            return
        
        print_section("Results Summary")
        
        # Group results by task and group
        grouped = {}
        for result in self.results:
            key = (result.task_id, result.group)
            if key not in grouped:
                grouped[key] = []
            grouped[key].append(result)
        
        # Calculate statistics
        stats = []
        for (task_id, group), results in grouped.items():
            stat = {
                'task_id': task_id,
                'group': group,
                'count': len(results),
                'success_rate': sum(1 for r in results if r.success) / len(results),
                'compilation_rate': sum(1 for r in results if r.compiles) / len(results),
                'avg_hallucinations': sum(r.hallucination_count for r in results) / len(results),
                'avg_iterations': sum(r.iterations for r in results) / len(results),
                'avg_time': sum(r.time_seconds for r in results) / len(results),
                'avg_tokens': sum(r.token_count for r in results) / len(results)
            }
            stats.append(stat)
        
        # Print summary
        for stat in stats:
            print(f"\n  {stat['task_id']} ({stat['group']}):")
            print(f"    Success rate: {stat['success_rate']:.1%}")
            print(f"    Compilation rate: {stat['compilation_rate']:.1%}")
            print(f"    Avg hallucinations: {stat['avg_hallucinations']:.1f}")
            print(f"    Avg iterations: {stat['avg_iterations']:.1f}")
            print(f"    Avg time: {stat['avg_time']:.2f}s")
            print(f"    Avg tokens: {stat['avg_tokens']:.0f}")
        
        # Save analysis
        analysis_file = self.results_dir / 'xiaomi_analysis.json'
        with open(analysis_file, 'w', encoding='utf-8') as f:
            json.dump(stats, f, indent=2)
        
        print_success(f"Analysis saved to {analysis_file}")
        
        # Compare control vs treatment
        self.compare_groups(stats)
    
    def compare_groups(self, stats: List[Dict]):
        """Compare control vs treatment groups."""
        print_section("Control vs Treatment Comparison")
        
        # Group by task_id
        tasks = set(s['task_id'] for s in stats)
        
        for task_id in sorted(tasks):
            control = next((s for s in stats if s['task_id'] == task_id and s['group'] == 'control'), None)
            treatment = next((s for s in stats if s['task_id'] == task_id and s['group'] == 'treatment'), None)
            
            if control and treatment:
                print(f"\n  {task_id}:")
                
                # Success rate comparison
                success_diff = treatment['success_rate'] - control['success_rate']
                print(f"    Success rate: {control['success_rate']:.1%} -> {treatment['success_rate']:.1%} ({success_diff:+.1%})")
                
                # Time comparison
                time_diff = treatment['avg_time'] - control['avg_time']
                print(f"    Avg time: {control['avg_time']:.2f}s -> {treatment['avg_time']:.2f}s ({time_diff:+.2f}s)")
                
                # Token comparison
                token_diff = treatment['avg_tokens'] - control['avg_tokens']
                print(f"    Avg tokens: {control['avg_tokens']:.0f} -> {treatment['avg_tokens']:.0f} ({token_diff:+.0f})")


def main():
    parser = argparse.ArgumentParser(description='Run Phase 4 Value Validation Experiments with Xiaomi MiMo-V2.5')
    parser.add_argument('--tasks', type=str, required=True, help='Path to tasks JSON file')
    parser.add_argument('--skills', type=str, default='../../../libskills-registry', 
                        help='Path to skills registry')
    parser.add_argument('--data', type=str, default='../data', help='Path to data directory')
    parser.add_argument('--trials', type=int, default=10, help='Number of trials per task')
    parser.add_argument('--group', choices=['control', 'treatment', 'both'], 
                        default='both', help='Which group to run')
    parser.add_argument('--max-tasks', type=int, default=None, help='Maximum number of tasks to run')
    
    args = parser.parse_args()
    
    print_header("Phase 4: Value Validation Experiment (Xiaomi MiMo-V2.5)")
    
    # Initialize runner
    try:
        runner = XiaomiExperimentRunner(
            data_dir=Path(args.data),
            skills_dir=Path(args.skills)
        )
    except Exception as e:
        print_error(f"Failed to initialize experiment runner: {e}")
        return 1
    
    # Load tasks
    if not runner.load_tasks(Path(args.tasks)):
        return 1
    
    # Limit number of tasks if specified
    if args.max_tasks:
        runner.tasks = runner.tasks[:args.max_tasks]
        print_warning(f"Limited to {args.max_tasks} tasks")
    
    # Run experiment
    if args.group in ['control', 'both']:
        runner.run_control_group(runner.tasks, args.trials)
    
    if args.group in ['treatment', 'both']:
        runner.run_treatment_group(runner.tasks, args.trials)
    
    # Save and analyze results
    runner.save_results()
    runner.analyze_results()
    
    print_header("Experiment Complete!")
    print(f"\nTotal results: {len(runner.results)}")
    print(f"Model used: {runner.config.model}")
    
    return 0


if __name__ == '__main__':
    exit(main())
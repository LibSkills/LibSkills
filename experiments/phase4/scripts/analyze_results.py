#!/usr/bin/env python3
"""
Analyze experiment results from Phase 4 value validation experiments.
"""

import json
import os
from pathlib import Path
from typing import Dict, List
from collections import defaultdict

# ANSI colors
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'


def print_header(text: str):
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'=' * 60}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{text.center(60)}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'=' * 60}{Colors.ENDC}\n")


def print_section(text: str):
    print(f"\n{Colors.OKBLUE}{Colors.BOLD}{text}{Colors.ENDC}")
    print(f"{Colors.OKBLUE}{'-' * len(text)}{Colors.ENDC}")


def print_success(text: str):
    print(f"{Colors.OKGREEN}[OK] {text}{Colors.ENDC}")


def print_warning(text: str):
    print(f"{Colors.WARNING}[WARN] {text}{Colors.ENDC}")


def print_error(text: str):
    print(f"{Colors.FAIL}[ERROR] {text}{Colors.ENDC}")


def load_results(results_dir: Path) -> List[Dict]:
    """Load all result files from the results directory."""
    results = []
    
    for file_path in results_dir.glob("xiaomi_results_*.json"):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if 'results' in data:
                    results.extend(data['results'])
        except Exception as e:
            print_warning(f"Failed to load {file_path}: {e}")
    
    return results


def analyze_results(results: List[Dict]) -> Dict:
    """Analyze experiment results."""
    
    # Group by task_id and group
    grouped = defaultdict(list)
    for result in results:
        key = (result['task_id'], result['group'])
        grouped[key].append(result)
    
    # Calculate statistics
    stats = {}
    for (task_id, group), group_results in grouped.items():
        stat = {
            'task_id': task_id,
            'group': group,
            'count': len(group_results),
            'success_rate': sum(1 for r in group_results if r.get('success', False)) / len(group_results),
            'compilation_rate': sum(1 for r in group_results if r.get('compiles', False)) / len(group_results),
            'avg_hallucinations': sum(r.get('hallucination_count', 0) for r in group_results) / len(group_results),
            'avg_iterations': sum(r.get('iterations', 0) for r in group_results) / len(group_results),
            'avg_time': sum(r.get('time_seconds', 0) for r in group_results) / len(group_results),
            'avg_tokens': sum(r.get('token_count', 0) for r in group_results) / len(group_results)
        }
        stats[(task_id, group)] = stat
    
    return stats


def compare_groups(stats: Dict) -> Dict:
    """Compare control vs treatment groups."""
    
    # Group by task_id
    task_ids = set(task_id for (task_id, _) in stats.keys())
    
    comparisons = {}
    for task_id in sorted(task_ids):
        control = stats.get((task_id, 'control'))
        treatment = stats.get((task_id, 'treatment'))
        
        if control and treatment:
            comparison = {
                'task_id': task_id,
                'success_rate_diff': treatment['success_rate'] - control['success_rate'],
                'compilation_rate_diff': treatment['compilation_rate'] - control['compilation_rate'],
                'time_diff': treatment['avg_time'] - control['avg_time'],
                'tokens_diff': treatment['avg_tokens'] - control['avg_tokens'],
                'control': control,
                'treatment': treatment
            }
            comparisons[task_id] = comparison
    
    return comparisons


def print_analysis(stats: Dict, comparisons: Dict):
    """Print analysis results."""
    
    print_section("Overall Statistics")
    
    # Group by library
    libraries = defaultdict(lambda: {'control': [], 'treatment': []})
    for (task_id, group), stat in stats.items():
        library = task_id.split('-')[0]
        libraries[library][group].append(stat)
    
    # Print library-level statistics
    for library, groups in sorted(libraries.items()):
        print(f"\n{library.upper()}:")
        
        if groups['control']:
            avg_success = sum(s['success_rate'] for s in groups['control']) / len(groups['control'])
            avg_tokens = sum(s['avg_tokens'] for s in groups['control']) / len(groups['control'])
            avg_time = sum(s['avg_time'] for s in groups['control']) / len(groups['control'])
            print(f"  Control:   Success={avg_success:.1%}, Tokens={avg_tokens:.0f}, Time={avg_time:.2f}s")
        
        if groups['treatment']:
            avg_success = sum(s['success_rate'] for s in groups['treatment']) / len(groups['treatment'])
            avg_tokens = sum(s['avg_tokens'] for s in groups['treatment']) / len(groups['treatment'])
            avg_time = sum(s['avg_time'] for s in groups['treatment']) / len(groups['treatment'])
            print(f"  Treatment: Success={avg_success:.1%}, Tokens={avg_tokens:.0f}, Time={avg_time:.2f}s")
    
    print_section("Task-Level Comparison")
    
    for task_id, comparison in sorted(comparisons.items()):
        print(f"\n{task_id}:")
        
        # Success rate comparison
        success_diff = comparison['success_rate_diff']
        if success_diff > 0:
            print_success(f"Success rate improved by {success_diff:.1%}")
        elif success_diff < 0:
            print_warning(f"Success rate decreased by {abs(success_diff):.1%}")
        else:
            print(f"Success rate unchanged")
        
        # Time comparison
        time_diff = comparison['time_diff']
        if time_diff < 0:
            print_success(f"Time improved by {abs(time_diff):.2f}s")
        elif time_diff > 0:
            print_warning(f"Time increased by {time_diff:.2f}s")
        else:
            print(f"Time unchanged")
        
        # Token comparison
        tokens_diff = comparison['tokens_diff']
        if tokens_diff < 0:
            print_success(f"Tokens improved by {abs(tokens_diff):.0f}")
        elif tokens_diff > 0:
            print_warning(f"Tokens increased by {tokens_diff:.0f}")
        else:
            print(f"Tokens unchanged")
    
    print_section("Summary")
    
    # Calculate overall improvements
    total_tasks = len(comparisons)
    improved_success = sum(1 for c in comparisons.values() if c['success_rate_diff'] > 0)
    improved_time = sum(1 for c in comparisons.values() if c['time_diff'] < 0)
    improved_tokens = sum(1 for c in comparisons.values() if c['tokens_diff'] < 0)
    
    print(f"Total tasks: {total_tasks}")
    print(f"Success rate improved: {improved_success}/{total_tasks} tasks")
    print(f"Time improved: {improved_time}/{total_tasks} tasks")
    print(f"Tokens improved: {improved_tokens}/{total_tasks} tasks")
    
    # Overall conclusion
    if improved_success > total_tasks / 2:
        print_success("Overall: Skills show positive impact")
    elif improved_success < total_tasks / 2:
        print_warning("Overall: Skills show negative impact")
    else:
        print("Overall: Mixed results")


def main():
    print_header("Phase 4 Experiment Results Analysis")
    
    # Load results
    script_dir = Path(__file__).parent
    results_dir = script_dir.parent / "data" / "results"
    results = load_results(results_dir)
    
    if not results:
        print_error(f"No results found in {results_dir}")
        return 1
    
    print_success(f"Loaded {len(results)} results")
    
    # Analyze
    stats = analyze_results(results)
    comparisons = compare_groups(stats)
    
    # Print analysis
    print_analysis(stats, comparisons)
    
    return 0


if __name__ == '__main__':
    exit(main())
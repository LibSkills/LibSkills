# Experiment Data

This directory contains experimental data from Phase 4 value validation experiments.

## Directory Structure

```
data/
├── README.md                 # This file
├── results/                  # Raw experiment results
│   ├── raw_results_YYYYMMDD_HHMMSS.json
│   └── analysis.json
├── prompts/                  # Generated prompts for AI
│   └── {task_id}_{group}_trial{n}_prompt.md
└── generated/                # Generated code from AI
    └── {task_id}_{group}_trial{n}/
        ├── main.cpp|rs|py
        └── test_output.txt
```

## Data Format

### Raw Results JSON

```json
{
  "experiment_id": "phase4_20260430_143022",
  "timestamp": "2026-04-30T14:30:22Z",
  "total_tasks": 15,
  "total_results": 300,
  "results": [
    {
      "task_id": "spdlog-1",
      "group": "control",
      "trial": 1,
      "timestamp": "2026-04-30T14:30:22Z",
      "success": true,
      "hallucination_count": 2,
      "compiles": true,
      "runtime_errors": 0,
      "token_count": 1250,
      "iterations": 3,
      "time_seconds": 45.2,
      "notes": "Initial compilation failed due to missing include"
    }
  ]
}
```

### Analysis JSON

```json
[
  {
    "task_id": "spdlog-1",
    "group": "control",
    "count": 10,
    "success_rate": 0.6,
    "compilation_rate": 0.7,
    "avg_hallucinations": 1.8,
    "avg_iterations": 2.5
  },
  {
    "task_id": "spdlog-1",
    "group": "treatment",
    "count": 10,
    "success_rate": 0.9,
    "compilation_rate": 1.0,
    "avg_hallucinations": 0.3,
    "avg_iterations": 1.2
  }
]
```

## Metrics Definitions

| Metric | Definition |
|--------|------------|
| **success** | Code passes all success criteria |
| **hallucination_count** | Number of API calls to non-existent functions |
| **compiles** | Code compiles without errors |
| **runtime_errors** | Number of runtime errors during execution |
| **token_count** | Total tokens used in AI API calls |
| **iterations** | Number of prompts needed to get working code |
| **time_seconds** | Time from first prompt to working code |

## Analysis Scripts

To analyze results, use the provided scripts:

```bash
# Run analysis
python scripts/analyze_results.py data/results/raw_results_YYYYMMDD_HHMMSS.json

# Generate report
python scripts/generate_report.py data/results/analysis.json
```

## Statistical Tests

For comparing control vs treatment groups:

- **t-test**: Compare means of continuous metrics (token count, time)
- **Chi-square**: Compare proportions (success rate, compilation rate)
- **Effect size (Cohen's d)**: Measure magnitude of differences

## Interpreting Results

### Success Thresholds

| Metric | Success Threshold | Failure Threshold |
|--------|------------------|-------------------|
| Hallucination Rate | ≥ 30% reduction | < 10% reduction |
| First-Compile Rate | ≥ 20% increase | < 5% increase |
| Runtime Error Rate | ≥ 25% reduction | < 10% reduction |

### Overall Success Criteria

The experiment is successful if:
- At least 2 of 3 primary metrics meet success threshold
- No primary metric falls below failure threshold
- Qualitative analysis shows clear benefit

## Data Privacy

- All data is anonymized (no user identifiers)
- API keys are never stored
- Results are aggregated for publication
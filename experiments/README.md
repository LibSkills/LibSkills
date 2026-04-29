# Phase 4: Value Validation Experiments

This directory contains the experimental setup for Phase 4 of the LibSkills roadmap: **Proving that skills reduce AI errors**.

## Directory Structure

```
experiments/
├── README.md                      # This file
├── phase4-design.md               # Detailed experiment design
├── REPORT.md                      # Experiment report template
└── phase4/
    ├── scripts/
    │   └── run_experiment.py      # Main experiment runner
    ├── tasks/
    │   └── experiment_tasks.json  # Task definitions
    └── data/
        └── README.md              # Data format documentation
```

## Quick Start

### 1. Install Dependencies

```bash
# Python dependencies (for experiment runner)
pip install requests

# C++ compiler (for spdlog tasks)
sudo apt install g++  # Linux
# or: brew install gcc  # macOS

# Rust compiler (for serde tasks)
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

# Python (for requests tasks)
# Python 3.8+ required
```

### 2. Configure AI API

Create a `.env` file in the `phase4/` directory:

```bash
# For Xiaomi MiMo-V2.5 (Primary)
XIAOMI_API_KEY=your-api-key

# For OpenAI (Optional, for comparison)
# OPENAI_API_KEY=your-api-key

# For Anthropic (Optional, for comparison)
# ANTHROPIC_API_KEY=your-api-key
```

### 3. Run Experiments

#### Using Xiaomi MiMo-V2.5 (Recommended)

```bash
cd experiments/phase4

# Test Xiaomi API connection
python scripts/test_xiaomi.py

# Run full experiment with Xiaomi
python scripts/run_xiaomi_experiment.py \
    --tasks tasks/experiment_tasks.json \
    --skills ../../../libskills-registry \
    --trials 10

# Run specific group
python scripts/run_xiaomi_experiment.py \
    --tasks tasks/experiment_tasks.json \
    --group control \
    --trials 10

python scripts/run_xiaomi_experiment.py \
    --tasks tasks/experiment_tasks.json \
    --group treatment \
    --trials 10
```

#### Using Other Backends

```bash
# Run with OpenAI (if configured)
python scripts/run_experiment.py \
    --tasks tasks/experiment_tasks.json \
    --backend openai \
    --trials 10

# Run with Anthropic (if configured)
python scripts/run_experiment.py \
    --tasks tasks/experiment_tasks.json \
    --backend anthropic \
    --trials 10
```

### 4. Analyze Results

Results are saved to `data/results/`. To analyze:

```bash
# View raw results
cat data/results/raw_results_*.json

# Generate analysis
python scripts/analyze_results.py data/results/raw_results_*.json
```

## Experiment Design

### Hypothesis

> AI agents that read structured library skills before generating code will produce code with significantly fewer errors than agents that do not.

### Variables

| Variable | Description |
|----------|-------------|
| **Independent** | Access to skills (Control: No, Treatment: Yes) |
| **Dependent** | Error rates, compilation success, token usage |

### Libraries Tested

| Library | Language | Tasks | Key Skills Tested |
|---------|----------|-------|-------------------|
| spdlog | C++ | 5 | Async logging, thread safety, lifecycle |
| serde | Rust | 5 | Serialization, validation, performance |
| requests | Python | 5 | Sessions, auth, retry logic |

### Metrics

| Metric | Definition | Success Threshold |
|--------|------------|-------------------|
| Hallucination Rate | % of invalid API calls | ≥ 30% reduction |
| First-Compile Rate | % that compile on first try | ≥ 20% increase |
| Runtime Error Rate | % with runtime errors | ≥ 25% reduction |

## Success Criteria

The experiment is **successful** if:
- At least 2 of 3 primary metrics meet success threshold
- No primary metric falls below failure threshold
- Qualitative analysis shows clear benefit

## Timeline

| Week | Activity | Deliverable |
|------|----------|-------------|
| 1 | Setup & Preparation | Test environment ready |
| 2-3 | Data Collection (Control) | Raw data for control group |
| 4-5 | Data Collection (Ttreatment) | Raw data for treatment group |
| 6 | Analysis & Report | Phase 4 Report |

## Next Steps

After completing the experiments:

1. **If successful**: 
   - Publish results on blog and social media
   - Update README with validation data
   - Proceed to Phase 5 (Expand Skills)
   - Engage AI tool vendors with evidence

2. **If unsuccessful**:
   - Analyze why skills didn't help
   - Revise skill format based on findings
   - Design new experiment with improvements
   - Repeat Phase 4

## Security Notice

⚠️ **IMPORTANT: Never commit API keys or .env files!**

- The `.env` file contains sensitive API keys and should NEVER be committed to version control
- `.gitignore` is configured to ignore `.env` files
- Use `.env.example` as a template to create your local `.env` file
- Never share your API keys publicly

To set up your environment securely:

1. Copy the example file:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and add your actual API keys:
   ```bash
   XIAOMI_API_KEY=your-actual-api-key
   ```

3. Verify `.env` is ignored by git:
   ```bash
   git status  # .env should NOT appear
   ```

## API Backend Options

The experiments support multiple AI backends:

### Xiaomi MiMo-V2.5 (Primary)
- Best performance for the experiments
- Configured via `XIAOMI_API_KEY`
- Model: `mimo-v2.5`

### OpenAI GPT-4 (Optional)
- For comparison experiments
- Configured via `OPENAI_API_KEY`
- Model: `gpt-4`

### Anthropic Claude (Optional)
- For comparison experiments
- Configured via `ANTHROPIC_API_KEY`
- Model: `claude-3-opus-20240229`

You can run experiments with different backends:

```bash
# Xiaomi (default)
python scripts/run_xiaomi_experiment.py --tasks tasks/experiment_tasks.json

# OpenAI (if configured)
python scripts/run_experiment.py --tasks tasks/experiment_tasks.json --backend openai

# Anthropic (if configured)
python scripts/run_experiment.py --tasks tasks/experiment_tasks.json --backend anthropic
```

## Troubleshooting

### API Key Issues
- Check that your `.env` file exists and contains valid keys
- Verify your API keys are active and have sufficient quota
- Check network connectivity to the API endpoints

### Python Issues
- Ensure Python 3.8+ is installed
- Install required packages: `pip install requests`

### Compiler Issues
- C++: Install g++ (Linux/macOS) or MinGW (Windows)
- Rust: Install via rustup
- Python: Usually pre-installed

## Contributing

To contribute to the experiments:

1. Add new tasks to `tasks/experiment_tasks.json`
2. Improve experiment scripts
3. Help with data collection
4. Analyze results

See [CONTRIBUTING.md](../../CONTRIBUTING.md) for guidelines.

## References

- [Phase 4 Design Document](phase4-design.md)
- [Experiment Report Template](REPORT.md)
- [Data Format Documentation](phase4/data/README.md)
- [LibSkills Specification](../../libskills-docs/SPEC.md)
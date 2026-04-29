# Start Xiaomi MiMo-V2.5 Experiment
# This script sets up and runs the Phase 4 value validation experiment

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "Phase 4: Value Validation Experiment with Xiaomi MiMo-V2.5" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Check if .env file exists
if (-not (Test-Path "..\.env")) {
    Write-Host "[ERROR] .env file not found!" -ForegroundColor Red
    Write-Host "Please create .env file with your Xiaomi API key."
    Write-Host ""
    if (Test-Path "..\.env.example") {
        Write-Host "You can copy the example file:" -ForegroundColor Yellow
        Write-Host "  copy ..\.env.example ..\.env" -ForegroundColor Gray
        Write-Host "Then edit ..\.env and add your actual API keys." -ForegroundColor Gray
    } else {
        Write-Host "Create a .env file with:" -ForegroundColor Yellow
        Write-Host "  XIAOMI_API_KEY=your-api-key-here" -ForegroundColor Gray
    }
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}

# Check if tasks file exists
if (-not (Test-Path "..\tasks\experiment_tasks.json")) {
    Write-Host "[ERROR] tasks\experiment_tasks.json not found!" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "[1/4] Testing Xiaomi API connection..." -ForegroundColor Yellow
python test_xiaomi.py
if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERROR] API test failed. Please check your API key and network." -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "[2/4] Running single task test..." -ForegroundColor Yellow
python run_xiaomi_experiment.py --tasks ..\tasks\experiment_tasks.json --trials 1 --max-tasks 1
if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERROR] Test run failed." -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "[3/4] Setup complete!" -ForegroundColor Green
Write-Host ""
Write-Host "============================================================" -ForegroundColor Green
Write-Host "Experiment Ready!" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Green
Write-Host ""
Write-Host "To run full experiment:" -ForegroundColor White
Write-Host "  python run_xiaomi_experiment.py --tasks ..\tasks\experiment_tasks.json --trials 10" -ForegroundColor Gray
Write-Host ""
Write-Host "To run specific group:" -ForegroundColor White
Write-Host "  python run_xiaomi_experiment.py --tasks ..\tasks\experiment_tasks.json --group control" -ForegroundColor Gray
Write-Host "  python run_xiaomi_experiment.py --tasks ..\tasks\experiment_tasks.json --group treatment" -ForegroundColor Gray
Write-Host ""
Write-Host "Results will be saved to: ..\data\results\" -ForegroundColor White
Write-Host ""
Read-Host "Press Enter to exit"
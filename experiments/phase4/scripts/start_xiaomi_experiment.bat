@echo off
REM Start Xiaomi MiMo-V2.5 Experiment
REM This script sets up and runs the Phase 4 value validation experiment

echo ============================================================
echo Phase 4: Value Validation Experiment with Xiaomi MiMo-V2.5
echo ============================================================
echo.

REM Check if .env file exists
if not exist "..\.env" (
    echo [ERROR] .env file not found!
    echo Please create .env file with your Xiaomi API key.
    echo.
    if exist "..\.env.example" (
        echo You can copy the example file:
        echo   copy ..\.env.example ..\.env
        echo Then edit ..\.env and add your actual API keys.
    ) else (
        echo Create a .env file with:
        echo   XIAOMI_API_KEY=your-api-key-here
    )
    echo.
    pause
    exit /b 1
)

REM Check if tasks file exists
if not exist "..\tasks\experiment_tasks.json" (
    echo [ERROR] tasks\experiment_tasks.json not found!
    pause
    exit /b 1
)

echo [1/4] Testing Xiaomi API connection...
python test_xiaomi.py
if %errorlevel% neq 0 (
    echo [ERROR] API test failed. Please check your API key and network.
    pause
    exit /b 1
)

echo.
echo [2/4] Running single task test...
python run_xiaomi_experiment.py --tasks ..\tasks\experiment_tasks.json --trials 1 --max-tasks 1
if %errorlevel% neq 0 (
    echo [ERROR] Test run failed.
    pause
    exit /b 1
)

echo.
echo [3/4] Setup complete!
echo.
echo ============================================================
echo Experiment Ready!
echo ============================================================
echo.
echo To run full experiment:
echo   python run_xiaomi_experiment.py --tasks ..\tasks\experiment_tasks.json --trials 10
echo.
echo To run specific group:
echo   python run_xiaomi_experiment.py --tasks ..\tasks\experiment_tasks.json --group control
echo   python run_xiaomi_experiment.py --tasks ..\tasks\experiment_tasks.json --group treatment
echo.
echo Results will be saved to: ..\data\results\
echo.
pause
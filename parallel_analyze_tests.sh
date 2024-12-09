#!/bin/bash
set -euo pipefail

# -----------------------------
# Configuration
# -----------------------------
# Get the absolute path of the script's directory
readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly DATA_DIR="${SCRIPT_DIR}/__internal__/_data"
readonly TESTS_DIR="${SCRIPT_DIR}/__internal__/collected_tests_hybrid/v1"
readonly LOGS_DIR="${SCRIPT_DIR}/__internal__/_logs"

declare -A FRAMEWORKS=(
    [aiohttp]="aiohttp"
    [connexion]="connexion"
    [django]="django"
    [fastapi]="fastapi"
    [flask]="flask"
    [gunicorn]="gunicorn"
    [pyramid]="pyramid"
    [sanic]="sanic"
    [starlette]="starlette"
    [tornado]="tornado"
    [uvicorn]="uvicorn"
)

# -----------------------------
# Helper Functions
# -----------------------------
log() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] $1"
}

analyze_framework() {
    local framework=$1
    local input_dir="${DATA_DIR}/${framework}"
    local output_dir="${TESTS_DIR}/${framework}"
    local log_file="${LOGS_DIR}/${framework}_tests_analysis_output.txt"

    log "Starting analysis of ${framework}"
    log "Input dir: ${input_dir}"
    log "Output dir: ${output_dir}"
    log "Log file: ${log_file}"

    # Ensure input directory exists
    if [ ! -d "$input_dir" ]; then
        log "ERROR: Input directory does not exist for ${framework}: ${input_dir}"
        return 1
    fi

    # Create output directory
    mkdir -p "$output_dir"

    # Run the analysis with debug output
    PYTHONPATH="${SCRIPT_DIR}:${PYTHONPATH:-}" python -m src.gluon.collect_tests.analyze_unit_tests \
        --input-dir "$input_dir" \
        --output-dir "$output_dir" \
        --log-file "$log_file" 2>&1 | tee -a "$log_file"

    local exit_code=${PIPESTATUS[0]}
    if [ $exit_code -ne 0 ]; then
        log "ERROR: Analysis failed for ${framework} with exit code ${exit_code}"
        return $exit_code
    fi

    log "Completed analysis of ${framework}"
}

# -----------------------------
# Main Script
# -----------------------------
log "Creating directories..."
mkdir -p "$DATA_DIR" "$TESTS_DIR" "$LOGS_DIR"

# First, try running one framework to test
log "Testing with single framework (flask)..."
analyze_framework "flask"

if [ $? -eq 0 ]; then
    log "Single framework test successful, proceeding with parallel execution..."
    
    # Run all frameworks in parallel
    log "Running analyses in parallel..."
    export -f log analyze_framework
    export SCRIPT_DIR DATA_DIR TESTS_DIR LOGS_DIR
    printf '%s\n' "${!FRAMEWORKS[@]}" | \
        parallel --jobs 50% --verbose \
        'analyze_framework {}'
else
    log "❌ Single framework test failed, please check the logs"
    exit 1
fi

log "✅ All analyses completed!"

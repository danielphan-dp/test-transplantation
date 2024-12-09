#!/bin/bash
set -euo pipefail

# -----------------------------
# Configuration
# -----------------------------
readonly DATA_DIR="__internal__/_data"
readonly COLLECTED_TESTS_DIR="__internal__/collected_tests"
readonly ANALYSIS_OUTPUT_DIR="__internal__/collected_tests_hybrid/v1"
declare -A REPO_MAP=(
    [connexion]="zalando"
    [fastapi]="tiangolo"
    [flask]="pallets"
    [gunicorn]="benoitc"
    [pyramid]="Pylons"
    [django]="django"
    [starlette]="encode"
    [tornado]="tornadoweb"
    [sanic]="sanic-org"
    [aiohttp]="aio-libs"
    [uvicorn]="encode"
)

# -----------------------------
# Helper Functions
# -----------------------------
log() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] $1"
}

# -----------------------------
# Main Script
# -----------------------------
log "Creating output directory..."
mkdir -p "$ANALYSIS_OUTPUT_DIR"

# Export the log function so it's available to parallel processes
export -f log

# Analyze tests in parallel
printf '%s\n' "${!REPO_MAP[@]}" | \
    parallel --jobs -1 --bar \
    "
    REPO={}
    INPUT_DIR=\"$DATA_DIR/\$REPO\"
    OUTPUT_DIR=\"$ANALYSIS_OUTPUT_DIR/\$REPO\"
    
    log \"Analyzing tests for \$REPO...\"

    # Create output directory if it doesn't exist
    mkdir -p \"\$OUTPUT_DIR\"
    
    # Run the analysis using the gluon environment
    python \\
        -m src.gluon.collect_tests.analyze_unit_tests \\
        -i \"\$INPUT_DIR\" \\
        -o \"\$OUTPUT_DIR\" \\
        > \"\${REPO}_tests_analysis_output.txt\"
    "

log "✅ All analyses completed!"

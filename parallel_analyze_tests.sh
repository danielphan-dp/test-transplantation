#!/bin/bash
set -euo pipefail

# Initialize PYTHONPATH if it doesn't exist
PYTHONPATH=${PYTHONPATH:-}
export PYTHONPATH="$(pwd):$PYTHONPATH"


# -----------------
# | Configuration |
# -----------------
REPOS=(
    "connexion"
    "fastapi"
    "flask"
    "gunicorn"
    "pyramid"
    "sanic"
    "starlette"
    "tornado"
    "uvicorn"
)

BASE_DIR="__internal__/_data"
TESTS_DIR="__internal__/collected_tests_hybrid/v2"
LOGS_DIR="__internal__/_setup_logs/_analyze_tests_logs"

TIMEOUT=$((60 * 60 * 24 * 7))  # 7 days in seconds


# --------------------
# | Helper Functions |
# --------------------
analyze_framework() {
    local repo=$1
    local env_name="venv-${repo}"
    local input_dir="${BASE_DIR}/${repo}"
    local output_dir="${TESTS_DIR}/${repo}"
    local log_file="${LOGS_DIR}/${repo}.log"
    
    {
        echo "=== Analyzing tests for ${repo} ==="
        echo "Start time: $(date)"
        
        # Store the original directory
        ORIGINAL_DIR=$(pwd)
        
        cd "$BASE_DIR/$repo" || return 1
        
        if [ ! -f "${env_name}/bin/activate" ]; then
            echo "Error: Virtual environment not found for ${repo}"
            return 1
        fi
        
        # Activate the framework's virtual environment
        source "${env_name}/bin/activate"

        # First install the framework
        pip install -e .[test]
        
        # Then install analysis dependencies
        pip install --no-cache-dir pytest pytest-xdist coverage pytest-cov tqdm astroid stdlib-list pydantic click
        
        # Return to original directory to install gluon
        cd "$ORIGINAL_DIR"
        pip install -e .
        pip install -e .[dev]
        
        # Create output directory
        mkdir -p "$output_dir"
        
        # Run the analysis with timeout
        timeout $TIMEOUT python -m src.gluon.collect_tests.hybrid_analysis \
            --input-dir "$input_dir" \
            --output-dir "$output_dir"

        local analysis_status=$?

        deactivate
        
        if [ $analysis_status -eq 124 ]; then
            echo "Analysis timed out after ${TIMEOUT} seconds"
            return 1
        fi
        
        echo "End time: $(date)"
        echo "=== Finished analyzing ${repo} ==="

        return $analysis_status

    } &> "$log_file"
    
    return ${PIPESTATUS[0]}
}

# Export function and variables for GNU parallel
export -f analyze_framework
export BASE_DIR TESTS_DIR LOGS_DIR TIMEOUT PYTHONPATH

# Default to 8 parallel processes if not specified
MAX_PARALLEL_PROCESSES=${1:-8}

# Create required directories
mkdir -p "$BASE_DIR"
mkdir -p "$TESTS_DIR"
mkdir -p "$LOGS_DIR"

echo "Configuration:"
echo "MAX_PARALLEL_PROCESSES: $MAX_PARALLEL_PROCESSES"
echo "BASE_DIR: $BASE_DIR"
echo "TESTS_DIR: $TESTS_DIR"
echo "LOGS_DIR: $LOGS_DIR"

# Use GNU parallel to run analyses
echo "Starting parallel analysis. Logs will be written to $LOGS_DIR/"
printf '%s\n' "${REPOS[@]}" | parallel -j "$MAX_PARALLEL_PROCESSES" analyze_framework

# Check for failures in log files
failed_repos=()
for repo in "${REPOS[@]}"; do
    log_file="$LOGS_DIR/${repo}.log"
    if ! grep -q "=== Finished analyzing ${repo} ===" "$log_file" 2>/dev/null; then
        failed_repos+=("$repo")
    fi
done

# Report results
echo "All analyses completed!"
if [ ${#failed_repos[@]} -eq 0 ]; then
    echo "✅ All repository analyses completed successfully!"
else
    echo "Analysis failed for the following repositories:"
    printf '%s\n' "${failed_repos[@]}"
    echo "Check individual log files in $LOGS_DIR/ for details"
    exit 1
fi

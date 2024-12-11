#!/bin/bash
set -euo pipefail

export PYTHONPATH="$(pwd)"

# -----------------------------
# Configuration
# -----------------------------
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
TESTS_DIR="__internal__/collected_tests_hybrid/v1"
LOGS_DIR="__internal__/_setup_logs/_analyze_tests_logs"

# Add timeout configuration
TIMEOUT=1800  # 30 minutes in seconds

# -----------------------------
# Helper Functions
# -----------------------------
analyze_framework() {
    local repo=$1
    local env_name="venv-${repo}"
    local input_dir="${BASE_DIR}/${repo}"
    local output_dir="${TESTS_DIR}/${repo}"
    local log_file="${LOGS_DIR}/${repo}.log"
    
    {
        echo "=== Analyzing tests for ${repo} ==="
        echo "Start time: $(date)"
        
        cd "$BASE_DIR/$repo" || return 1
        
        if [ ! -f "${env_name}/bin/activate" ]; then
            echo "Error: Virtual environment not found for ${repo}"
            return 1
        fi
        
        # Activate the framework's virtual environment
        source "${env_name}/bin/activate"
        
        # Install the gluon package and its dependencies
        cd ../../.. # Return to project root
        pip install -e .
        
        # Create output directory
        mkdir -p "$output_dir"
        
        # Run the analysis with timeout
        timeout $TIMEOUT "${BASE_DIR}/${repo}/${env_name}/bin/python" -m src.gluon.collect_tests.analyze_unit_tests \
            --input-dir "$input_dir" \
            --output-dir "$output_dir"
            
        local analysis_status=$?
        
        deactivate
        
        if [ $analysis_status -eq 124 ]; then
            echo "Analysis timed out after ${TIMEOUT} seconds"
            return 1
        fi
        
        echo "End time: $(date)"
        echo "=== Finished analyzing ${repo} ===\n"
        
        return $analysis_status
        
    } &> "$log_file"
    
    return ${PIPESTATUS[0]}
}

# -----------------------------
# Main Script
# -----------------------------
mkdir -p "$BASE_DIR" "$TESTS_DIR" "$LOGS_DIR"

# Run all frameworks in parallel immediately
echo "Starting parallel analysis. Logs will be written to $LOGS_DIR/"
declare -A pids
failed_repos=()

for repo in "${REPOS[@]}"; do
    echo "Starting analysis for $repo..."
    analyze_framework "$repo" &
    pids[$!]=$repo
done

# Wait for all background processes and check their exit status
for pid in "${!pids[@]}"; do
    if wait $pid; then
        echo "✅ ${pids[$pid]} completed successfully"
    else
        failed_repos+=("${pids[$pid]}")
        echo "❌ ${pids[$pid]} failed"
    fi
done

# Report results
echo "All analyses completed!"
if [ ${#failed_repos[@]} -eq 0 ]; then
    echo "✅ All repository analyses completed successfully!"
else
    echo "❌ Analysis failed for the following repositories:"
    printf '%s\n' "${failed_repos[@]}"
    echo "Check individual log files in $LOGS_DIR/ for details"
    exit 1
fi

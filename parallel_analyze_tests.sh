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
    set +e

    local repo=$1
    local env_name="venv-${repo}"
    local input_dir="${BASE_DIR}/${repo}"
    local output_dir="${TESTS_DIR}/${repo}"
    local log_file="${LOGS_DIR}/${repo}.log"
    
    local analysis_status=0
    
    {
        echo "=== Analyzing tests for ${repo} ==="
        echo "Start time: $(date)"
        
        # Store the original directory
        ORIGINAL_DIR=$(pwd)
        
        cd "$BASE_DIR/$repo" || { analysis_status=1; exit $analysis_status; }
        
        if [ ! -f "${env_name}/bin/activate" ]; then
            echo "Error: Virtual environment not found for ${repo}"
            analysis_status=1
            exit $analysis_status
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

        analysis_status=$?

        deactivate

        if [ $analysis_status -eq 124 ]; then
            echo "Analysis timed out after ${TIMEOUT} seconds"
            analysis_status=1
        fi
        
        echo "End time: $(date)"
        echo "=== Finished analyzing ${repo} ==="

        exit $analysis_status

    } &> "$log_file"

    set -e
    
    return $?
}


# ---------------
# | Main Script |
# ---------------
mkdir -p "$BASE_DIR" "$TESTS_DIR" "$LOGS_DIR"

# Run all frameworks in parallel immediately
echo "Starting parallel analysis. Logs will be written to $LOGS_DIR/"
declare -A pids
failed_repos=()

# This part IS parallel - each framework runs in parallel
for repo in "${REPOS[@]}"; do
    echo "Starting analysis for $repo..."
    analyze_framework "$repo" &  # The & makes it run in background
    pids[$!]=$repo
done

# Wait for all background processes
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

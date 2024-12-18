#!/bin/bash

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
LOGS_DIR="__internal__/_setup_logs/_test_runs_logs"

# Create logs directory if it doesn't exist
mkdir -p "$LOGS_DIR"

run_tests() {
    local repo=$1
    local env_name="venv-${repo}"
    local log_file="$LOGS_DIR/${repo}.log"
    
    {
        echo "=== Running tests for $repo ==="
        echo "Start time: $(date)"
        
        cd "$BASE_DIR/$repo" || return 1
        
        if [ ! -f "${env_name}/bin/activate" ]; then
            echo "Error: Virtual environment not found for $repo"
            return 1
        fi
        
        source "${env_name}/bin/activate"
        
        # Special handling for tornado
        if [ "$repo" = "tornado" ]; then
            echo "Running tornado tests..."
            python -m pytest tornado/test
        else
            echo "Running pytest for $repo..."
            python -m pytest tests/ -v
        fi
        
        local test_status=$?
        
        deactivate
        
        cd - > /dev/null
        
        echo "End time: $(date)"
        echo "=== Finished testing $repo ===\n"
        
        return $test_status
        
    } &> "$log_file"
    
    return ${PIPESTATUS[0]}
}

# Export function and variables for GNU parallel
export -f run_tests
export BASE_DIR LOGS_DIR

# Default to 8 parallel processes if not specified
MAX_PARALLEL_PROCESSES=${1:-8}

echo "Configuration:"
echo "MAX_PARALLEL_PROCESSES: $MAX_PARALLEL_PROCESSES"
echo "BASE_DIR: $BASE_DIR"
echo "LOGS_DIR: $LOGS_DIR"

# Use GNU parallel to run tests
echo "Starting parallel test runs. Logs will be written to $LOGS_DIR/"
printf '%s\n' "${REPOS[@]}" | parallel -j "$MAX_PARALLEL_PROCESSES" run_tests

# Check for failures in log files
failed_repos=()
for repo in "${REPOS[@]}"; do
    log_file="$LOGS_DIR/${repo}.log"
    if ! grep -q "=== Finished testing $repo ===" "$log_file" 2>/dev/null || \
       grep -q "FAILED" "$log_file" 2>/dev/null; then
        failed_repos+=("$repo")
    fi
done

# Report results
echo "All test runs completed!"
if [ ${#failed_repos[@]} -eq 0 ]; then
    echo "All repository tests passed successfully!"
else
    echo "Tests failed for the following repositories:"
    printf '%s\n' "${failed_repos[@]}"
    echo "Check individual log files in $LOGS_DIR/ for details"
    exit 1
fi

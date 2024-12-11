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
    
    case "$repo" in
        "tornado")
            {
                echo "=== Running tests for tornado ==="
                echo "Start time: $(date)"
                
                cd "$BASE_DIR/$repo" || return 1
                
                if [ ! -f "${env_name}/bin/activate" ]; then
                    echo "Error: Virtual environment not found for tornado"
                    return 1
                fi
                
                source "${env_name}/bin/activate"
                
                # Run tornado's test suite using its test module
                echo "Running tornado tests..."
                python -m pytest tornado/test
                
                local test_status=$?
                
                deactivate
                
                cd - > /dev/null
                
                echo "End time: $(date)"
                echo "=== Finished testing tornado ===\n"
                
                return $test_status
                
            } &> "$log_file"
            ;;
        *)
            # Original test logic for other repos
            {
                echo "=== Running tests for $repo ==="
                echo "Start time: $(date)"
                
                cd "$BASE_DIR/$repo" || return 1
                
                if [ ! -f "${env_name}/bin/activate" ]; then
                    echo "Error: Virtual environment not found for $repo"
                    return 1
                fi
                
                source "${env_name}/bin/activate"
                
                echo "Running pytest for $repo..."
                python -m pytest tests/ -v
                
                local test_status=$?
                
                deactivate
                
                cd - > /dev/null
                
                echo "End time: $(date)"
                echo "=== Finished testing $repo ===\n"
                
                return $test_status
                
            } &> "$log_file"
            ;;
    esac
    
    return ${PIPESTATUS[0]}
}

# Array to store process IDs and their corresponding repo names
declare -A pids
failed_repos=()

# Main execution with parallelization
echo "Starting parallel test runs. Logs will be written to $LOGS_DIR/"
for repo in "${REPOS[@]}"; do
    run_tests "$repo" &
    pids[$!]=$repo
done

# Wait for all background processes and check their exit status
for pid in "${!pids[@]}"; do
    wait $pid
    if [ $? -ne 0 ]; then
        failed_repos+=("${pids[$pid]}")
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
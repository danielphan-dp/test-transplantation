#!/bin/bash

REPOS=(
    "connexion"
    "django"
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
LOGS_DIR="__internal__/_setup_repos_envs_logs"

# Create logs directory if it doesn't exist
mkdir -p "$LOGS_DIR"

create_venv() {
    local repo=$1
    local env_name="venv-${repo}"
    
    # Remove existing environment if it exists
    echo "Removing existing environment if present: ${env_name}"
    rm -rf "${env_name}"
    
    echo "Creating virtual environment: ${env_name}"
    python -m venv "${env_name}"
}

activate_and_install() {
    local repo=$1
    local env_name="venv-${repo}"
    
    # Activate the virtual environment
    source "${env_name}/bin/activate"
    
    # Initialize git submodules if they exist
    if [ -f ".gitmodules" ]; then
        echo "Initializing git submodules..."
        git submodule update --init --recursive
    fi
    
    # Install dependencies
    echo "Installing base package..."
    pip install -e .
    
    echo "Installing dev dependencies..."
    pip install -e .[dev] || pip install -e .[testing] || pip install -e .[test] || echo "No dev dependencies found for $repo"
}

cleanup_and_deactivate() {
    echo "Deactivating virtual environment..."
    deactivate 2>/dev/null || true
}

process_repo() {
    local repo=$1
    local log_file="$LOGS_DIR/${repo}.log"
    
    {
        echo "=== Processing $repo ==="
        echo "Start time: $(date)"
        
        # Change to repo directory first
        cd "$BASE_DIR/$repo" || return 1
        
        create_venv "$repo" || return 1
        activate_and_install "$repo" || return 1
        cleanup_and_deactivate
        
        # Return to original directory
        cd - > /dev/null
        
        echo "End time: $(date)"
        echo "=== Finished $repo ===\n"
    } &> "$log_file"
    
    # Return the status of the process
    return ${PIPESTATUS[0]}
}

# Array to store process IDs and their corresponding repo names
declare -A pids
failed_repos=()

# Main execution with parallelization
echo "Starting parallel processing. Logs will be written to $LOGS_DIR/"
for repo in "${REPOS[@]}"; do
    process_repo "$repo" &
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
echo "All processes completed!"
if [ ${#failed_repos[@]} -eq 0 ]; then
    echo "All repositories processed successfully!"
else
    echo "The following repositories failed:"
    printf '%s\n' "${failed_repos[@]}"
    echo "Check individual log files in $LOGS_DIR/ for details"
    exit 1
fi

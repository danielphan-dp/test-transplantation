#!/bin/bash

# Parse command line argument for MAX_PARALLEL_PROCESSES
# Default to 8 if not provided
MAX_PARALLEL_PROCESSES=${1:-8}


# Add debug output
set -x  # This will print each command as it's executed
REPOS=(
    "spec-first/connexion"
    "tiangolo/fastapi"
    "pallets/flask"
    "sanic-org/sanic"
    "tornadoweb/tornado"
    "Pylons/pyramid"
    "encode/starlette"
    "benoitc/gunicorn"
    "encode/uvicorn"
)
BASE_DIR="__internal__/_data"
LOGS_DIR="__internal__/_setup_logs/_clone_repos_logs"


# Print parallel job processing configuration
echo "Configuration:"
echo "MAX_PARALLEL_PROCESSES: $MAX_PARALLEL_PROCESSES"
echo "BASE_DIR: $BASE_DIR"
echo "LOGS_DIR: $LOGS_DIR"


# Add debug output for directory creation
echo "Creating directories:"
echo "BASE_DIR: $BASE_DIR"
echo "LOGS_DIR: $LOGS_DIR"


# Create base and logs directories if they don't exist
mkdir -p "$BASE_DIR"
mkdir -p "$LOGS_DIR"

clone_repo() {
    local repo=$1
    local repo_name=$(echo "$repo" | cut -d'/' -f2)
    local target_dir="$BASE_DIR/$repo_name"
    local log_file="$LOGS_DIR/${repo_name}.log"
    
    {
        echo "=== Cloning $repo ==="
        echo "Start time: $(date)"
        
        if [ -d "$target_dir" ]; then
            echo "Removing existing directory for $repo_name..."
            rm -rf "$target_dir"
        fi
        
        git clone "https://github.com/$repo.git" "$target_dir"
        local clone_status=$?
        
        echo "End time: $(date)"
        echo "=== Finished cloning $repo ===\n"
        
        return $clone_status
    } &> "$log_file"
    
    return ${PIPESTATUS[0]}
}


# Replace the manual parallel implementation with GNU parallel
echo "Starting parallel repository cloning to $BASE_DIR/. Logs will be written to $LOGS_DIR/"


# Export the functions and variables so parallel can use them
export -f clone_repo
export BASE_DIR LOGS_DIR


# Use parallel to clone repos with max 8 jobs
printf '%s\n' "${REPOS[@]}" | parallel -j $MAX_PARALLEL_PROCESSES clone_repo


# Check for any failures in the log files
failed_repos=()
for repo in "${REPOS[@]}"; do
    repo_name=$(echo "$repo" | cut -d'/' -f2)
    log_file="$LOGS_DIR/${repo_name}.log"
    if grep -q "fatal\|error" "$log_file" 2>/dev/null; then
        failed_repos+=("$repo")
    fi
done


# Report results
echo "All clone operations completed!"
if [ ${#failed_repos[@]} -eq 0 ]; then
    echo "All repositories cloned successfully!"
else
    echo "Cloning failed for the following repositories:"
    printf '%s\n' "${failed_repos[@]}"
    exit 1
fi

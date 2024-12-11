#!/bin/bash

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

# Array to store process IDs and their corresponding repo names
declare -A pids
failed_repos=()

# Main execution with parallelization
echo "Starting parallel repository cloning to $BASE_DIR/. Logs will be written to $LOGS_DIR/"
for repo in "${REPOS[@]}"; do
    clone_repo "$repo" &
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
echo "All clone operations completed!"
if [ ${#failed_repos[@]} -eq 0 ]; then
    echo "All repositories cloned successfully!"
else
    echo "Cloning failed for the following repositories:"
    printf '%s\n' "${failed_repos[@]}"
    exit 1
fi

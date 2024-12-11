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
LOGS_DIR="__internal__/_setup_repos_envs_logs"

# Create logs directory if it doesn't exist
mkdir -p "$LOGS_DIR"

create_venv() {
    local repo=$1
    local env_name="venv-${repo}"
    
    # Remove existing environment if it exists
    echo "Removing existing environment if present: ${env_name}"
    rm -rf "$env_name"
    
    # Create new environment
    python -m venv "$env_name"
    
    # Activate and upgrade pip
    source "$env_name/bin/activate"
    pip install --upgrade pip

    deactivate
}

activate_and_install() {
    local repo=$1
    local env_name="venv-${repo}"
    
    # Activate the virtual environment
    source "${env_name}/bin/activate"
    
    # Upgrade pip first
    echo "Upgrading pip..."
    pip install --upgrade pip
    
    # Install base package with testing extras first
    echo "Installing base package with testing dependencies..."
    pip install -e .[testing] || \
    pip install -e .[test] || \
    pip install -e .[tests] || \
    echo "No testing extras found, installing base package..."
    pip install -e .
    
    # Install test requirements if they exist
    if [ -f "test-requirements.txt" ]; then
        echo "Installing test-requirements.txt..."
        pip install -r test-requirements.txt
    fi
    if [ -f "requirements-test.txt" ]; then
        echo "Installing requirements-test.txt..."
        pip install -r requirements-test.txt
    fi
    
    # Ensure pytest and coverage are installed regardless
    echo "Ensuring pytest and coverage tools are installed..."
    pip install pytest pytest-cov coverage
}

cleanup_and_deactivate() {
    echo "Deactivating virtual environment..."
    deactivate 2>/dev/null || true
}

setup_fastapi() {
    local repo="fastapi"
    local env_name="venv-${repo}"
    local log_file="$LOGS_DIR/${repo}.log"
    
    {
        echo "=== Setting up FastAPI ==="
        echo "Start time: $(date)"
        
        cd "$BASE_DIR/$repo" || return 1
        
        # Create and activate venv
        python -m venv "$env_name"
        source "$env_name/bin/activate"
        
        # Upgrade pip
        pip install --upgrade pip
        
        # Install main package with all extras
        pip install -e .[all]
        
        # Install all requirements files
        pip install -r requirements-tests.txt
        pip install -r requirements-docs.txt
        pip install -r requirements-docs-tests.txt
        pip install -r requirements-github-actions.txt
        
        # Install pre-commit if specified in requirements.txt
        pip install pre-commit
        
        # Install playwright if specified in requirements.txt
        pip install playwright
        
        deactivate
        
        echo "End time: $(date)"
        echo "=== Finished FastAPI setup ===\n"
        
    } &> "$log_file"
}

setup_uvicorn() {
    local repo="uvicorn"
    local env_name="venv-${repo}"
    local log_file="$LOGS_DIR/${repo}.log"
    
    {
        echo "=== Setting up Uvicorn ==="
        echo "Start time: $(date)"
        
        cd "$BASE_DIR/$repo" || return 1
        
        # Create and activate venv
        python -m venv "$env_name"
        source "$env_name/bin/activate"
        
        # Upgrade pip
        pip install --upgrade pip
        
        # Install main package with standard extras
        pip install -e .[standard]
        
        # Install core dependencies from requirements.txt
        pip install -r requirements.txt
        
        # Install development dependencies
        pip install build==1.2.2 twine==5.1.1
        
        # Install testing tools
        pip install ruff==0.6.8 pytest==8.3.3 pytest-mock==3.14.0 mypy==1.11.2
        pip install coverage coverage-conditional-plugin
        pip install httpx watchgod
        
        # Install documentation tools
        pip install mkdocs mkdocs-material
        
        deactivate
        
        echo "End time: $(date)"
        echo "=== Finished Uvicorn setup ===\n"
        
    } &> "$log_file"
}

process_repo() {
    local repo=$1
    
    if [ "$repo" = "fastapi" ]; then
        setup_fastapi
        return $?
    elif [ "$repo" = "uvicorn" ]; then
        setup_uvicorn
        return $?
    fi
    
    # Original process_repo logic for other repos
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

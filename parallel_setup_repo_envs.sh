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
LOGS_DIR="__internal__/_setup_logs/_setup_repos_envs_logs"

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
    pip install pytest pytest-cov coverage tqdm astroid stdlib-list pydantic click
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

setup_connexion() {
    local repo="connexion"
    local env_name="venv-${repo}"
    local log_file="$LOGS_DIR/${repo}.log"
    
    {
        echo "=== Setting up Connexion ==="
        echo "Start time: $(date)"
        
        cd "$BASE_DIR/$repo" || return 1
        
        # Create and activate venv
        python -m venv "$env_name"
        source "$env_name/bin/activate"
        
        # Install poetry
        pip install poetry
        
        # Install dependencies with all extras
        poetry install --all-extras
        
        # Install pre-commit hooks
        pre-commit install
        
        deactivate
        
        echo "End time: $(date)"
        echo "=== Finished Connexion setup ===\n"
        
    } &> "$log_file"
}

setup_flask() {
    local repo="flask"
    local env_name="venv-${repo}"
    local log_file="$LOGS_DIR/${repo}.log"
    
    {
        echo "=== Setting up Flask ==="
        echo "Start time: $(date)"
        
        cd "$BASE_DIR/$repo" || return 1
        
        # Create and activate venv
        python -m venv "$env_name"
        source "$env_name/bin/activate"
        
        # Upgrade pip
        pip install --upgrade pip
        
        # Install build dependencies
        pip install flit_core
        
        # Install package in editable mode with all optional dependencies
        pip install -e ".[async,dotenv]"
        
        # Install test dependencies
        pip install -r requirements/tests.txt
        
        # Install additional development tools
        pip install pytest pytest-cov coverage pre-commit
        
        deactivate
        
        echo "End time: $(date)"
        echo "=== Finished Flask setup ===\n"
        
    } &> "$log_file"
}

setup_gunicorn() {
    local repo="gunicorn"
    local env_name="venv-${repo}"
    local log_file="$LOGS_DIR/${repo}.log"
    
    {
        echo "=== Setting up Gunicorn ==="
        echo "Start time: $(date)"
        
        cd "$BASE_DIR/$repo" || return 1
        
        # Create and activate venv
        python -m venv "$env_name"
        source "$env_name/bin/activate"
        
        # Upgrade pip
        pip install --upgrade pip
        
        # Install main package
        pip install -e .
        
        # Install test requirements
        pip install -r requirements_test.txt
        
        # Install testing tools
        pip install pytest pytest-cov coverage
        
        deactivate
        
        echo "End time: $(date)"
        echo "=== Finished Gunicorn setup ===\n"
        
    } &> "$log_file"
}

setup_pyramid() {
    local repo="pyramid"
    local env_name="venv-${repo}"
    local log_file="$LOGS_DIR/${repo}.log"
    
    {
        echo "=== Setting up Pyramid ==="
        echo "Start time: $(date)"
        
        cd "$BASE_DIR/$repo" || return 1
        
        # Create and activate venv
        python -m venv "$env_name"
        source "$env_name/bin/activate"
        
        # Upgrade pip
        pip install --upgrade pip
        
        # Install main package with testing extras
        pip install -e .[testing]
        
        # Install additional testing tools
        pip install pytest pytest-cov coverage tox
        
        deactivate
        
        echo "End time: $(date)"
        echo "=== Finished Pyramid setup ===\n"
        
    } &> "$log_file"
}

setup_sanic() {
    local repo="sanic"
    local env_name="venv-${repo}"
    local log_file="$LOGS_DIR/${repo}.log"
    
    {
        echo "=== Setting up Sanic ==="
        echo "Start time: $(date)"
        
        cd "$BASE_DIR/$repo" || return 1
        
        # Create and activate venv
        python -m venv "$env_name"
        source "$env_name/bin/activate"
        
        # Upgrade pip
        pip install --upgrade pip
        
        # Install package with test extras
        pip install -e ".[test,http3]"
        
        # Install development requirements
        pip install -r requirements/dev.txt
        
        # Install additional tools required by tox.ini
        pip install ruff mypy slotscheck bandit
        
        # Install testing tools
        pip install pytest pytest-cov coverage
        
        deactivate
        
        echo "End time: $(date)"
        echo "=== Finished Sanic setup ===\n"
        
    } &> "$log_file"
}

setup_starlette() {
    local repo="starlette"
    local env_name="venv-${repo}"
    local log_file="$LOGS_DIR/${repo}.log"
    
    {
        echo "=== Setting up Starlette ==="
        echo "Start time: $(date)"
        
        cd "$BASE_DIR/$repo" || return 1
        
        # Create and activate venv
        python -m venv "$env_name"
        source "$env_name/bin/activate"
        
        # Upgrade pip
        pip install --upgrade pip
        
        # Install main package
        pip install -e .
        
        # Install test requirements
        pip install -r requirements.txt
        
        # Install additional testing tools
        pip install pytest pytest-cov coverage
        
        deactivate
        
        echo "End time: $(date)"
        echo "=== Finished Starlette setup ===\n"
        
    } &> "$log_file"
}

setup_tornado() {
    local repo="tornado"
    local env_name="venv-${repo}"
    local log_file="$LOGS_DIR/${repo}.log"
    
    {
        echo "=== Setting up Tornado ==="
        echo "Start time: $(date)"
        
        cd "$BASE_DIR/$repo" || return 1
        
        # Create and activate venv
        python -m venv "$env_name"
        source "$env_name/bin/activate"
        
        # Upgrade pip
        pip install --upgrade pip
        
        # Install main package
        pip install -e .
        
        # Install test requirements
        pip install -r requirements.txt
        
        # Install testing tools
        pip install pytest pytest-cov coverage
        
        deactivate
        
        echo "End time: $(date)"
        echo "=== Finished Tornado setup ===\n"
        
    } &> "$log_file"
}

process_repo() {
    local repo=$1
    
    case "$repo" in
        "fastapi")
            setup_fastapi
            ;;
        "uvicorn")
            setup_uvicorn
            ;;
        "connexion")
            setup_connexion
            ;;
        "flask")
            setup_flask
            ;;
        "gunicorn")
            setup_gunicorn
            ;;
        "pyramid")
            setup_pyramid
            ;;
        "sanic")
            setup_sanic
            ;;
        "starlette")
            setup_starlette
            ;;
        "tornado")
            setup_tornado
            ;;
        *)
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
            ;;
    esac
    
    return ${PIPESTATUS[0]}
}

# Export functions and variables for GNU parallel
export -f process_repo create_venv activate_and_install cleanup_and_deactivate
export -f setup_fastapi setup_uvicorn setup_connexion setup_flask setup_gunicorn
export -f setup_pyramid setup_sanic setup_starlette setup_tornado
export BASE_DIR LOGS_DIR

# Default to 8 parallel processes if not specified
MAX_PARALLEL_PROCESSES=${1:-8}

echo "Configuration:"
echo "MAX_PARALLEL_PROCESSES: $MAX_PARALLEL_PROCESSES"
echo "BASE_DIR: $BASE_DIR"
echo "LOGS_DIR: $LOGS_DIR"

# Use GNU parallel to process repos
echo "Starting parallel processing. Logs will be written to $LOGS_DIR/"
printf '%s\n' "${REPOS[@]}" | parallel -j "$MAX_PARALLEL_PROCESSES" process_repo

# Check for failures in log files
failed_repos=()
for repo in "${REPOS[@]}"; do
    log_file="$LOGS_DIR/${repo}.log"
    if grep -q "error\|failed\|failure" "$log_file" 2>/dev/null; then
        failed_repos+=("$repo")
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

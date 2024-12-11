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

# Base directory
BASE_DIR="__internal__/_data"

# Loop through each repository
for repo in "${REPOS[@]}"; do
    echo "=== Installing $repo ==="
    cd "$BASE_DIR/$repo" || continue
    
    # Initialize git submodules if they exist
    if [ -f ".gitmodules" ]; then
        echo "Initializing git submodules..."
        git submodule update --init --recursive
    fi
    
    # Try to install both -e . and -e .[dev]
    echo "Installing base package..."
    pip install -e .
    
    echo "Installing dev dependencies..."
    pip install -e .[dev] || pip install -e .[testing] || pip install -e .[test] || echo "No dev dependencies found for $repo"
    
    # Go back to original directory
    cd - > /dev/null
    
    echo "=== Finished $repo ===\n"
done

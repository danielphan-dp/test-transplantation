#!/bin/bash
set -euo pipefail  # Add error handling

# -----------------------------
# Configuration
# -----------------------------
readonly DATA_DIR="__internal__/data"
readonly TESTS_DIR="__internal__/collected_tests"
readonly REPOS="connexion fastapi flask gunicorn pyramid"
readonly REPO_OWNERS=(
    "zalando/connexion"
    "tiangolo/fastapi"
    "pallets/flask"
    "benoitc/gunicorn"
    "Pylons/pyramid"
)

# -----------------------------
# Helper Functions
# -----------------------------
log() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] $1"
}

cleanup() {
    cd - >/dev/null  # Return to original directory
}

# -----------------------------
# Create required directories
# -----------------------------
log "Creating directories..."
mkdir -p "$DATA_DIR" "$TESTS_DIR"

# -----------------------------
# Clone repositories in parallel
# -----------------------------
trap cleanup EXIT  # Ensure we return to original directory
cd "$DATA_DIR" || exit 1

log "Cloning repositories..."
echo "$REPOS" | tr ' ' '\n' | parallel --jobs 100% '
    if [ ! -d {} ]; then
        echo "Cloning {}..."
        git clone --depth 1 https://github.com/{owner}/{} 2>/dev/null
    else
        echo "{} already exists"
    fi' \
    --env owner \
    ::: "${REPO_OWNERS[@]}"
cd ../..

# -----------------------------
# Collect tests in parallel
# -----------------------------
log "Collecting tests..."
echo "$REPOS" | tr ' ' '\n' | \
parallel --jobs -1 --bar \
    'python -m src.gluon.collect_tests.collect_unit_tests \
        '"$DATA_DIR"'/{} \
        '"$TESTS_DIR"'/collected_tests__{}.json \
        --log-level INFO'

log "✅ All collections completed!"

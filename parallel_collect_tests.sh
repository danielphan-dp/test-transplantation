#!/bin/bash
set -euo pipefail

# -----------------------------
# Configuration
# -----------------------------
readonly DATA_DIR="__internal__/data"
readonly TESTS_DIR="__internal__/collected_tests"
declare -A REPO_MAP=(
    [connexion]="zalando"
    [fastapi]="tiangolo"
    [flask]="pallets"
    [gunicorn]="benoitc"
    [pyramid]="Pylons"
    [django]="django"
    [starlette]="encode"
    [tornado]="tornadoweb"
    [sanic]="sanic-org"
    [aiohttp]="aio-libs"
    [uvicorn]="encode"
)

# -----------------------------
# Helper Functions
# -----------------------------
log() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] $1"
}

# -----------------------------
# Main Script
# -----------------------------
log "Creating directories..."
mkdir -p "$DATA_DIR" "$TESTS_DIR"

log "Cloning repositories..."
cd "$DATA_DIR" || exit 1

# Clone repositories in parallel
printf '%s\n' "${!REPO_MAP[@]}" | \
    parallel --jobs 100% \
    '
    if [ ! -d {} ]; then
        owner="${REPO_MAP[{}]}"
        echo "Cloning {}: https://github.com/$owner/{}"
        git clone --depth 1 "https://github.com/$owner/{}" || exit 1
    else
        echo "{} already exists"
    fi
    '

# Verify clones
for repo in "${!REPO_MAP[@]}"; do
    if [ ! -d "$repo" ]; then
        log "ERROR: Repository $repo was not cloned successfully"
        exit 1
    fi
done

cd ../..

log "Collecting tests..."
printf '%s\n' "${!REPO_MAP[@]}" | \
    parallel --jobs -1 --bar \
    'python -m src.gluon.collect_tests.collect_unit_tests \
        '"$DATA_DIR"'/{} \
        '"$TESTS_DIR"'/collected_tests__{}.json \
        --log-level INFO'

log "✅ All collections completed!"

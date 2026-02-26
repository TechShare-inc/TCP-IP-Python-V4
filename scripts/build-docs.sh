#!/usr/bin/env bash
# build-docs.sh — Build the full documentation site.
#
# Usage:
#   ./scripts/build-docs.sh          # full build (Sphinx + VitePress)
#   ./scripts/build-docs.sh --api    # regenerate API reference only
#   ./scripts/build-docs.sh --site   # build VitePress site only
set -euo pipefail
cd "$(dirname "$0")/.."

API_ONLY=false
SITE_ONLY=false

for arg in "$@"; do
  case $arg in
    --api)  API_ONLY=true ;;
    --site) SITE_ONLY=true ;;
  esac
done

# --- Step 1: Install Python docs dependencies ---
if [ "$SITE_ONLY" = false ]; then
  echo "==> Installing Python docs dependencies..."
  uv pip install -e ".[docs]" --quiet

  echo "==> Generating API reference with Sphinx..."
  .venv/bin/sphinx-build -b markdown _sphinx/ docs/reference/api/ -q
  echo "    Done — Markdown written to docs/reference/api/"
fi

# --- Step 2: Build VitePress site ---
if [ "$API_ONLY" = false ]; then
  echo "==> Installing Node.js dependencies..."
  npm install --silent

  echo "==> Building VitePress site..."
  npm run docs:build
  echo "    Done — Site output in docs/.vitepress/dist/"
fi

echo "==> Build complete."

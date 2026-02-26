# build-docs.ps1 — Build the full documentation site (Windows).
#
# Usage:
#   .\scripts\build-docs.ps1          # full build (Sphinx + VitePress)
#   .\scripts\build-docs.ps1 -ApiOnly # regenerate API reference only
#   .\scripts\build-docs.ps1 -SiteOnly # build VitePress site only

param(
    [switch]$ApiOnly,
    [switch]$SiteOnly
)

$ErrorActionPreference = "Stop"
Push-Location (Split-Path -Parent $PSScriptRoot)

try {
    # --- Step 1: Generate API reference with Sphinx ---
    if (-not $SiteOnly) {
        Write-Host "==> Installing Python docs dependencies..."
        uv pip install -e ".[docs]" --quiet

        Write-Host "==> Generating API reference with Sphinx..."
        & .venv\Scripts\sphinx-build.exe -b markdown _sphinx/ docs/reference/api/ -q
        Write-Host "    Done - Markdown written to docs/reference/api/"
    }

    # --- Step 2: Build VitePress site ---
    if (-not $ApiOnly) {
        Write-Host "==> Installing Node.js dependencies..."
        npm install --silent

        Write-Host "==> Building VitePress site..."
        npm run docs:build
        Write-Host "    Done - Site output in docs/.vitepress/dist/"
    }

    Write-Host "==> Build complete."
}
finally {
    Pop-Location
}

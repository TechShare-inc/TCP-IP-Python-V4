# Sphinx configuration for Dobot V4 Python SDK API reference.
#
# This generates Markdown output (via sphinx-markdown-builder) that is
# consumed by VitePress under docs/reference/api/.

import os
import sys

# Ensure the package is importable
sys.path.insert(0, os.path.abspath(".."))

# -- Project information -----------------------------------------------

project = "dobot_api_v4"
copyright = "2024-2026, Dobot / TechShare Corp."  # noqa: A001
author = "Dobot"
release = "4.1.0"

# -- General configuration ---------------------------------------------

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx_markdown_builder",
]

# Napoleon settings (Google-style docstrings)
napoleon_google_docstring = True
napoleon_numpy_docstring = False
napoleon_include_init_with_doc = True
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = True
napoleon_use_admonition_for_notes = True

# Autodoc settings
autodoc_typehints = "description"
autodoc_member_order = "bysource"
autodoc_default_options = {
    "members": True,
    "undoc-members": False,
    "show-inheritance": True,
    "inherited-members": False,
}

# Exclude internal/private names
autodoc_default_flags = ["members"]

# -- Options for Markdown output ----------------------------------------

# sphinx-markdown-builder writes .md files
# Output directory is set via sphinx-build -b markdown CLI flag

# Default language for code blocks (avoids "default" language in VitePress)
highlight_language = "python"

# Suppress warnings about missing references to external types
nitpicky = False

# -- Exclude patterns ---------------------------------------------------

exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

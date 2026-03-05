---
name: ts-examples-creator
description: Create or update Python tutorial examples in a project-agnostic way. Use when asked to build a basic-to-advanced learning series in examples/, follow NN_topic naming such as 01_basic_motion.py, align examples with Diataxis tutorial style, and enforce context-first, quality, and style rules.
---

# ts-examples-creator

Generate a progressive tutorial series of Python examples that teach users from basic to advanced usage.

## Scope

- Restrict this skill to Python projects.
- Create Python files only (`.py`) in the example series.
- Reject requests to generate equivalent examples in other languages.

## Bundled Resources

- `scripts/check_examples.py`: Validates `NN_topic.py` naming in the skill's `examples/` folder.
- `assets/example-template.py`: Starter template for new tutorial examples.
- `examples/01_basic_usage.py`: Minimal reference example for beginner-level flow.

## Required Pre-Read

Before writing or updating examples, read project context to avoid guessing API usage:

- Inspect source code first (`src/`, package modules, and entry points) to identify real public APIs and usage patterns.
- Inspect existing `examples/` files if present to preserve style and progression.
- Inspect tests for real usage patterns and edge cases.
- Inspect docs under `docs/` only if docs already exist.
- Detect lint/format/test tooling from config files (for example `pyproject.toml`).
- Identify the canonical import path and preferred construction pattern from existing code.

Only start writing new examples after this context pass.

## Workflow

1. Read project source and identify canonical public APIs and lifecycle patterns.
2. Choose the next tutorial topic in a basic-to-advanced sequence.
3. Create one focused example file using the required naming pattern and starting from `assets/example-template.py`.
4. Write runnable code with type hints, safe defaults, and project-standard style.
5. Add docstring metadata and optional `See also:` links if docs exist.
6. Run `scripts/check_examples.py`, then format and lint with project tooling before finalizing.

## Output Standards

### Output and Naming

- Write files under `examples/` at repository root.
- Name files as `NN_topic.py` with a zero-padded two-digit prefix, for example `01_basic_motion.py`.
- Keep a strict learning order from basic to advanced.
- Continue numbering from the highest existing prefix for incremental additions.
- Keep one focused learning objective per example file.

### Tutorial Progression (Diataxis)

Treat the series as Tutorial content in Diataxis:

- Optimize for guided learning, not exhaustive API coverage.
- Ensure each step depends only on prior examples.
- Add short narrative guidance in module docstrings so users understand what they learn next.
- Prefer a progression like:
  1. Installation and first successful call
  2. Basic usage patterns and common operations
  3. Reading results and handling state
  4. Error handling and recovery patterns
  5. Configuration and integration examples
  6. Advanced workflows and composition
  7. Expert or low-level features (if applicable)

### Required Script Skeleton

Use this baseline structure for every new example:

```python
#!/usr/bin/env python3
"""<Title> example.

<One-paragraph description of what this example demonstrates.>

Difficulty: <Beginner / Intermediate / Advanced>
Prerequisites: <What must be known or installed first>
"""

from package_name import Client

CONFIG_VALUE = "example"


def main() -> None:
    """<Brief verb phrase describing the action.>"""
    client = Client(CONFIG_VALUE)
    result = client.run()
    print(result)


if __name__ == "__main__":
    main()
```

### API Usage Rules

- Import from the project's public package API, not internal/private modules.
- Follow the project's canonical setup and teardown patterns.
- Use context managers where the project uses context-managed resources.
- Use low-level/internal APIs only when needed, and explain why.

### Error Handling and Safety

- Wrap long-running examples in `try/except KeyboardInterrupt` when appropriate.
- Catch project-specific exception types when demonstrating explicit error handling.
- Never use bare `except:`.
- Add guardrails for external effects (network, filesystem, device, or API side effects).
- Keep defaults conservative and safe for first-time users.

### Style Rules

- Add full type annotations for all function signatures.
- Use Google-style docstrings where function complexity justifies it.
- Use `snake_case` for variables and parameters.
- Use `UPPER_SNAKE_CASE` for module constants.
- Prefix boolean params with `is_`, `has_`, `should_`, or `can_`.
- Keep line length at `<= 120`.
- Target Python `>= 3.10`; use `X | Y` instead of `Union[X, Y]`.
- Ensure output passes `ruff format` and `ruff check`.

### Module Docstring Contract

Include these fields in the module docstring:

- Title line ending with `example.`
- One-paragraph description
- `Difficulty: <Beginner / Intermediate / Advanced>`
- `Prerequisites: <Dependencies or prior examples>`

When applicable, add a `See also:` block linking to related docs, for example:

```python
"""Basic motion example.

See also:
- docs/tutorial/basic-motion.md
- docs/reference/api/client.md#run
"""
```

If documentation is not prepared yet, omit `See also:` links instead of creating placeholder links.

## Quality Checklist

- [ ] Use canonical public imports from the project package
- [ ] Follow the project's setup/teardown lifecycle conventions
- [ ] Add completion/wait synchronization when later steps depend on prior operations
- [ ] Keep defaults conservative and beginner-safe
- [ ] Keep type hints and naming conventions consistent
- [ ] Include required module docstring fields
- [ ] Use tutorial naming format `NN_topic.py` (for example `01_basic_motion.py`)
- [ ] Maintain basic-to-advanced ordering across the series
- [ ] Confirm project context was read before authoring examples
- [ ] Use public APIs and canonical project patterns
- [ ] Pass `ruff format` and `ruff check`

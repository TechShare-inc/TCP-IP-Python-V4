"""Code generator: regenerates the forwarding region in robot.py.

Usage::

    python -m dobot_api_v4._codegen

The script introspects ``DobotApiDashboard`` and emits one-liner::

    def <name>(self, ...) -> ...:
        return self.dashboard.<name>(...)

methods for every public dashboard command, replacing the marked region
between ``# --- BEGIN GENERATED FORWARDS ---`` and
``# --- END GENERATED FORWARDS ---`` in ``robot.py``.

The script is idempotent: running it twice produces identical output.
"""

from __future__ import annotations

import inspect
import re
import sys
from pathlib import Path
from typing import Any

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

_HERE = Path(__file__).parent
ROBOT_PY = _HERE / "robot.py"

BEGIN_MARKER = "    # --- BEGIN GENERATED FORWARDS ---"
END_MARKER = "    # --- END GENERATED FORWARDS ---"

# typing names that might appear in rendered annotations
_TYPING_NAMES: frozenset[str] = frozenset(
    {
        "Any",
        "Callable",
        "ClassVar",
        "Dict",
        "Final",
        "FrozenSet",
        "Iterable",
        "Iterator",
        "List",
        "Mapping",
        "Optional",
        "Sequence",
        "Set",
        "Tuple",
        "Type",
        "Union",
    }
)

_TYPING_TOKEN_RE = re.compile(r"\b([A-Z][a-zA-Z]+)\b")


_MIXIN_ORDER = [
    "_SystemMixin",
    "_ConfigMixin",
    "_IOMixin",
    "_ModbusMixin",
    "_QueryMixin",
    "_MotionMixin",
    "_ForceMixin",
    "_ConveyorMixin",
    "_WeldMixin",
    "_CheckMixin",
]

_MIXIN_LABELS: dict[str, str] = {
    "_SystemMixin": "System",
    "_ConfigMixin": "Config",
    "_IOMixin": "I/O",
    "_ModbusMixin": "Modbus",
    "_QueryMixin": "Query",
    "_MotionMixin": "Motion",
    "_ForceMixin": "Force",
    "_ConveyorMixin": "Conveyor",
    "_WeldMixin": "Weld",
    "_CheckMixin": "Check",
}

# ---------------------------------------------------------------------------
# Annotation / signature helpers
# ---------------------------------------------------------------------------


def _render_annotation(ann: Any) -> str:
    """Return a short Python expression for a type annotation."""
    if ann is inspect.Parameter.empty:
        return ""
    if ann is None:
        return "None"
    # Use the stdlib formatter which handles typing generics correctly,
    # then strip any package-path prefixes (dobot_api_v4.dtypes.Pose -> Pose).
    formatted = inspect.formatannotation(ann)
    formatted = re.sub(r"\bdobot_api_v4(?:\.\w+)*\.(\w+)\b", r"\1", formatted)
    return formatted


def _render_param(param: inspect.Parameter) -> str:
    """Render one parameter for the ``def`` signature line (excluding self)."""
    name = param.name
    ann = param.annotation

    has_ann = ann is not inspect.Parameter.empty
    has_default = param.default is not inspect.Parameter.empty

    if param.kind == inspect.Parameter.VAR_POSITIONAL:
        base = f"*{name}" + (f": {_render_annotation(ann)}" if has_ann else "")
        return base
    if param.kind == inspect.Parameter.VAR_KEYWORD:
        base = f"**{name}" + (f": {_render_annotation(ann)}" if has_ann else "")
        return base

    base = f"{name}: {_render_annotation(ann)}" if has_ann else name
    if has_default:
        base = f"{base} = {param.default!r}"
    return base


def _render_call_arg(param: inspect.Parameter) -> str:
    """Render one parameter for the forwarding call body."""
    if param.kind == inspect.Parameter.VAR_POSITIONAL:
        return f"*{param.name}"
    if param.kind == inspect.Parameter.VAR_KEYWORD:
        return f"**{param.name}"
    if param.kind == inspect.Parameter.KEYWORD_ONLY:
        return f"{param.name}={param.name}"
    return param.name


def _generate_method(name: str, func: Any) -> list[str]:
    """Return the source lines for a forwarding method, including any docstring."""
    sig = inspect.signature(func)
    params = [p for p in sig.parameters.values() if p.name != "self"]

    param_strs = ["self"] + [_render_param(p) for p in params]
    call_args = [_render_call_arg(p) for p in params]

    ret = _render_annotation(sig.return_annotation)
    ret_part = f" -> {ret}" if ret else ""

    def_line = f"    def {name}({', '.join(param_strs)}){ret_part}:"
    body_line = f"        return self.dashboard.{name}({', '.join(call_args)})"

    lines = [def_line]

    doc = inspect.getdoc(func)
    if doc:
        doc_lines = doc.splitlines()
        if len(doc_lines) == 1:
            lines.append(f'        """{doc_lines[0]}"""')
        else:
            lines.append(f'        """{doc_lines[0]}')
            for dl in doc_lines[1:]:
                lines.append(f"        {dl}" if dl.strip() else "")
            lines.append('        """')

    lines.append(body_line)
    return lines


# ---------------------------------------------------------------------------
# Region generation
# ---------------------------------------------------------------------------


def generate_region() -> tuple[str, int]:
    """Introspect ``DobotApiDashboard`` and return (region_text, method_count)."""
    from dobot_api_v4.base import DobotApi  # noqa: PLC0415
    from dobot_api_v4.commands.dashboard import DobotApiDashboard  # noqa: PLC0415

    # Names defined on the base class -- these are infrastructure, not commands.
    base_names: set[str] = {
        name for name, _ in inspect.getmembers(DobotApi, predicate=inspect.isfunction)
    }

    # Build a lookup: mixin class name -> [(method_name, func), ...]
    # Use vars(mixin_cls) to preserve source-file ordering within each mixin.
    mixin_classes: dict[str, type] = {
        cls.__name__: cls
        for cls in DobotApiDashboard.__mro__
        if cls.__name__ in _MIXIN_ORDER
    }

    mixin_methods: dict[str, list[tuple[str, Any]]] = {m: [] for m in _MIXIN_ORDER}
    uncategorized: list[tuple[str, Any]] = []
    seen: set[str] = set()

    for mixin_name in _MIXIN_ORDER:
        mixin_cls = mixin_classes.get(mixin_name)
        if mixin_cls is None:
            continue
        for attr_name, obj in vars(mixin_cls).items():
            if (
                attr_name.startswith("_")
                or attr_name in base_names
                or attr_name in seen
                or not inspect.isfunction(obj)
            ):
                continue
            mixin_methods[mixin_name].append((attr_name, obj))
            seen.add(attr_name)

    # Catch any public methods not in a known mixin (shouldn't normally happen)
    for name, method in inspect.getmembers(
        DobotApiDashboard, predicate=inspect.isfunction
    ):
        if name.startswith("_") or name in base_names or name in seen:
            continue
        uncategorized.append((name, method))
        seen.add(name)

    # Collect all method lines first so we can scan for typing names
    method_sections: list[tuple[str, list[list[str]]]] = []  # (label, [method_lines])
    total = 0
    for mixin_name in _MIXIN_ORDER:
        entries = mixin_methods[mixin_name]
        if not entries:
            continue
        label = _MIXIN_LABELS[mixin_name]
        section_methods: list[list[str]] = []
        for method_name, func in entries:
            section_methods.append(_generate_method(method_name, func))
            total += 1
        method_sections.append((label, section_methods))

    other_methods: list[list[str]] = []
    for method_name, func in uncategorized:
        other_methods.append(_generate_method(method_name, func))
        total += 1

    # Scan all generated def lines for typing names that need to be imported
    all_def_lines = " ".join(
        ml[0] for _, section in method_sections for ml in section  # the def line
    ) + " ".join(ml[0] for ml in other_methods)
    needed_typing: list[str] = sorted(
        name
        for name in _TYPING_NAMES
        if re.search(rf"\b{re.escape(name)}\b", all_def_lines)
    )

    # Assemble the region
    lines: list[str] = [
        BEGIN_MARKER,
        "    # Auto-generated by `python -m dobot_api_v4._codegen` -- do not edit manually.",
    ]
    if needed_typing:
        lines.append(f"    from typing import {', '.join(needed_typing)}")
    lines.append("")

    for label, section_methods in method_sections:
        lines.append(f"    # --- {label} ---")
        lines.append("")
        for method_lines in section_methods:
            lines.extend(method_lines)
            lines.append("")

    if other_methods:
        lines.append("    # --- Other ---")
        lines.append("")
        for method_lines in other_methods:
            lines.extend(method_lines)
            lines.append("")

    lines.append(END_MARKER)
    return "\n".join(lines), total


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> None:
    """Regenerate the forwarding region in ``robot.py``."""
    if not ROBOT_PY.exists():
        sys.exit(f"Error: {ROBOT_PY} not found")

    source = ROBOT_PY.read_text(encoding="utf-8")

    begin_idx = source.find(BEGIN_MARKER)
    end_idx = source.find(END_MARKER)

    if begin_idx == -1 or end_idx == -1:
        sys.exit(
            f"Error: region markers not found in {ROBOT_PY.name}\n"
            f"  Expected: {BEGIN_MARKER!r}\n"
            f"  And:      {END_MARKER!r}"
        )

    region, total = generate_region()

    # Replace from BEGIN_MARKER through END_MARKER (inclusive)
    end_of_end = end_idx + len(END_MARKER)
    new_source = source[:begin_idx] + region + source[end_of_end:]

    ROBOT_PY.write_text(new_source, encoding="utf-8")
    print(f"Generated {total} forwarding methods -> {ROBOT_PY.name}")


if __name__ == "__main__":
    main()

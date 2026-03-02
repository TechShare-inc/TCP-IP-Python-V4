"""Type aliases for protocol command parameters."""

from typing import Union

DynParam = Union[int, float, str, tuple]
ToolDynParam = tuple[int, int, int]

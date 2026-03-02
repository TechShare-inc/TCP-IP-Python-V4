"""Composed dashboard command client for Dobot V4."""

from ..base import DobotApi
from ._check_mixin import _CheckMixin
from ._config_mixin import _ConfigMixin
from ._conveyor_mixin import _ConveyorMixin
from ._force_mixin import _ForceMixin
from ._io_mixin import _IOMixin
from ._modbus_mixin import _ModbusMixin
from ._motion_mixin import _MotionMixin
from ._query_mixin import _QueryMixin
from ._system_mixin import _SystemMixin
from ._weld_mixin import _WeldMixin


class DobotApiDashboard(
    _SystemMixin,
    _ConfigMixin,
    _IOMixin,
    _ModbusMixin,
    _QueryMixin,
    _MotionMixin,
    _ForceMixin,
    _ConveyorMixin,
    _WeldMixin,
    _CheckMixin,
    DobotApi,
):
    """Dashboard command client for Dobot V4 control API (port 29999).

    Composes all command categories via multiple inheritance:
    - System/lifecycle commands (_SystemMixin)
    - Configuration commands (_ConfigMixin)
    - Digital/analog I/O commands (_IOMixin)
    - Modbus and register commands (_ModbusMixin)
    - Status queries (_QueryMixin)
    - Motion commands (_MotionMixin)
    - Force control commands (_ForceMixin)
    - Conveyor commands (_ConveyorMixin)
    - Weld/weave commands (_WeldMixin)
    - Motion check commands (_CheckMixin)
    """

    ...

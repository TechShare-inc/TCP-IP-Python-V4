"""Conveyor tracking commands for Dobot V4 API."""

from ._parse import parse_ack, parse_int
from ._serialization import _SerializationMixin


class _ConveyorMixin(_SerializationMixin):
    """Mixin for conveyor belt tracking commands.

    Includes conveyor initialization, conveyor-synchronized linear/circular
    motions, object retrieval, offset/compensation, and sync start/stop.
    """

    # ------------------------------------------------------------------
    # Initialization
    # ------------------------------------------------------------------

    def cnv_init(self, index: int) -> None:
        """Initialize the conveyor.

        Args:
            index: Conveyor index.

        Returns:
            Raw response string from robot.
        """
        string = f"CnvInit({index:d})"
        return parse_ack(self.send_recv_msg(string))

    # ------------------------------------------------------------------
    # Conveyor Motion
    # ------------------------------------------------------------------

    def cnv_mov_l(
        self,
        j1: float,
        j2: float,
        j3: float,
        j4: float,
        j5: float,
        j6: float,
        user: int = -1,
        tool: int = -1,
        a: int = -1,
        v: int = -1,
        cp: int = -1,
        r: int = -1,
    ) -> int:
        """Conveyor-synchronized linear motion.

        Args:
            j1: X or joint-1 value.
            j2: Y or joint-2 value.
            j3: Z or joint-3 value.
            j4: Rx or joint-4 value.
            j5: Ry or joint-5 value.
            j6: Rz or joint-6 value.
            user: User coordinate system index. -1 = not set.
            tool: Tool coordinate system index. -1 = not set.
            a: Acceleration. -1 = not set.
            v: Velocity. -1 = not set.
            cp: Continuous path setting. -1 = not set.
            r: Blending radius. -1 = not set.

        Returns:
            Raw response string from robot.
        """
        string = f"CnvMovL(pose={{{j1:f},{j2:f},{j3:f},{j4:f},{j5:f},{j6:f}}}"
        params = []
        if user != -1:
            params.append(f"user={user:d}")
        if tool != -1:
            params.append(f"tool={tool:d}")
        if a != -1:
            params.append(f"a={a:d}")
        if v != -1:
            params.append(f"v={v:d}")
        if cp != -1:
            params.append(f"cp={cp:d}")
        if r != -1:
            params.append(f"r={r:d}")
        if params:
            string += "," + ",".join(params)
        string += ")"
        return parse_int(self.send_recv_msg(string))

    def cnv_mov_c(
        self,
        j1a: float,
        j2a: float,
        j3a: float,
        j4a: float,
        j5a: float,
        j6a: float,
        j1b: float,
        j2b: float,
        j3b: float,
        j4b: float,
        j5b: float,
        j6b: float,
        user: int = -1,
        tool: int = -1,
        a: int = -1,
        v: int = -1,
        cp: int = -1,
        r: int = -1,
        mode: int = 1,
    ) -> int:
        """Conveyor-synchronized circular motion.

        Args:
            j1a: X or joint-1 of the first via point.
            j2a: Y or joint-2 of the first via point.
            j3a: Z or joint-3 of the first via point.
            j4a: Rx or joint-4 of the first via point.
            j5a: Ry or joint-5 of the first via point.
            j6a: Rz or joint-6 of the first via point.
            j1b: X or joint-1 of the second via point.
            j2b: Y or joint-2 of the second via point.
            j3b: Z or joint-3 of the second via point.
            j4b: Rx or joint-4 of the second via point.
            j5b: Ry or joint-5 of the second via point.
            j6b: Rz or joint-6 of the second via point.
            user: User coordinate system index. -1 = not set.
            tool: Tool coordinate system index. -1 = not set.
            a: Acceleration. -1 = not set.
            v: Velocity. -1 = not set.
            cp: Continuous path setting. -1 = not set.
            r: Blending radius. -1 = not set.
            mode: Circle mode. 1 = default.

        Returns:
            Raw response string from robot.
        """
        string = (
            f"CnvMovC(pose={{{j1a:f},{j2a:f},{j3a:f},{j4a:f},{j5a:f},{j6a:f}}}"
            + f",pose={{{j1b:f},{j2b:f},{j3b:f},{j4b:f},{j5b:f},{j6b:f}}}"
        )
        params = []
        if user != -1:
            params.append(f"user={user:d}")
        if tool != -1:
            params.append(f"tool={tool:d}")
        if a != -1:
            params.append(f"a={a:d}")
        if v != -1:
            params.append(f"v={v:d}")
        if cp != -1:
            params.append(f"cp={cp:d}")
        if r != -1:
            params.append(f"r={r:d}")
        if mode != 1:
            params.append(f"mode={mode:d}")
        if params:
            string += "," + ",".join(params)
        string += ")"
        return parse_int(self.send_recv_msg(string))

    # ------------------------------------------------------------------
    # Object & Offset
    # ------------------------------------------------------------------

    def get_cnv_object(self, obj_id: int) -> str:
        """Get conveyor object information.

        Args:
            obj_id: Object identifier.

        Returns:
            Raw response string from robot.
        """
        return self.send_recv_msg(f"GetCnvObject({obj_id:d})")

    def set_cnv_point_offset(self, x_offset: float, y_offset: float) -> None:
        """Set conveyor point offset.

        Args:
            x_offset: X-axis offset value.
            y_offset: Y-axis offset value.

        Returns:
            Raw response string from robot.
        """
        return parse_ack(self.send_recv_msg(f"SetCnvPointOffset({x_offset:f},{y_offset:f})"))

    def set_cnv_time_compensation(self, time: int) -> None:
        """Set conveyor time compensation.

        Args:
            time: Time compensation value in milliseconds.

        Returns:
            Raw response string from robot.
        """
        return parse_ack(self.send_recv_msg(f"SetCnvTimeCompensation({time:d})"))

    # ------------------------------------------------------------------
    # Sync Start / Stop
    # ------------------------------------------------------------------

    def start_sync_cnv(self) -> None:
        """Start synchronous conveyor tracking.

        Returns:
            Raw response string from robot.
        """
        return parse_ack(self.send_recv_msg("StartSyncCnv()"))

    def stop_sync_cnv(self) -> None:
        """Stop synchronous conveyor tracking.

        Returns:
            Raw response string from robot.
        """
        return parse_ack(self.send_recv_msg("StopSyncCnv()"))

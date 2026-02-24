"""Conveyor tracking commands for Dobot V4 API."""

from ._serialization import _SerializationMixin


class _ConveyorMixin(_SerializationMixin):
    """Mixin for conveyor belt tracking commands.

    Includes conveyor initialization, conveyor-synchronized linear/circular
    motions, object retrieval, offset/compensation, and sync start/stop.
    """

    # ------------------------------------------------------------------
    # Initialization
    # ------------------------------------------------------------------

    def cnv_init(self, index: int) -> str:
        """Initialize the conveyor.

        Args:
            index: Conveyor index.

        Returns:
            Raw response string from robot.
        """
        string = "CnvInit({:d})".format(index)
        return self.send_recv_msg(string)

    CnvInit = cnv_init

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
    ) -> str:
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
        string = "CnvMovL(pose={{{:f},{:f},{:f},{:f},{:f},{:f}}}".format(
            j1, j2, j3, j4, j5, j6
        )
        params = []
        if user != -1:
            params.append("user={:d}".format(user))
        if tool != -1:
            params.append("tool={:d}".format(tool))
        if a != -1:
            params.append("a={:d}".format(a))
        if v != -1:
            params.append("v={:d}".format(v))
        if cp != -1:
            params.append("cp={:d}".format(cp))
        if r != -1:
            params.append("r={:d}".format(r))
        if params:
            string += "," + ",".join(params)
        string += ")"
        return self.send_recv_msg(string)

    CnvMovL = cnv_mov_l

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
    ) -> str:
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
        string = "CnvMovC(pose={{{:f},{:f},{:f},{:f},{:f},{:f}}},pose={{{:f},{:f},{:f},{:f},{:f},{:f}}}".format(
            j1a, j2a, j3a, j4a, j5a, j6a, j1b, j2b, j3b, j4b, j5b, j6b
        )
        params = []
        if user != -1:
            params.append("user={:d}".format(user))
        if tool != -1:
            params.append("tool={:d}".format(tool))
        if a != -1:
            params.append("a={:d}".format(a))
        if v != -1:
            params.append("v={:d}".format(v))
        if cp != -1:
            params.append("cp={:d}".format(cp))
        if r != -1:
            params.append("r={:d}".format(r))
        if mode != 1:
            params.append("mode={:d}".format(mode))
        if params:
            string += "," + ",".join(params)
        string += ")"
        return self.send_recv_msg(string)

    CnvMovC = cnv_mov_c

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
        return self.send_recv_msg("GetCnvObject({:d})".format(obj_id))

    GetCnvObject = get_cnv_object

    def set_cnv_point_offset(self, x_offset: float, y_offset: float) -> str:
        """Set conveyor point offset.

        Args:
            x_offset: X-axis offset value.
            y_offset: Y-axis offset value.

        Returns:
            Raw response string from robot.
        """
        return self.send_recv_msg(
            "SetCnvPointOffset({:f},{:f})".format(x_offset, y_offset)
        )

    SetCnvPointOffset = set_cnv_point_offset

    def set_cnv_time_compensation(self, time: int) -> str:
        """Set conveyor time compensation.

        Args:
            time: Time compensation value in milliseconds.

        Returns:
            Raw response string from robot.
        """
        return self.send_recv_msg("SetCnvTimeCompensation({:d})".format(time))

    SetCnvTimeCompensation = set_cnv_time_compensation

    # ------------------------------------------------------------------
    # Sync Start / Stop
    # ------------------------------------------------------------------

    def start_sync_cnv(self) -> str:
        """Start synchronous conveyor tracking.

        Returns:
            Raw response string from robot.
        """
        return self.send_recv_msg("StartSyncCnv()")

    StartSyncCnv = start_sync_cnv

    def stop_sync_cnv(self) -> str:
        """Stop synchronous conveyor tracking.

        Returns:
            Raw response string from robot.
        """
        return self.send_recv_msg("StopSyncCnv()")

    StopSyncCnv = stop_sync_cnv

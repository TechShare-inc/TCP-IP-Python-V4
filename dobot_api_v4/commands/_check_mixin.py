"""Motion check commands for Dobot V4 API."""

from ._serialization import _SerializationMixin


class _CheckMixin(_SerializationMixin):
    """Mixin for motion-check commands.

    Provides collision/reachability pre-check versions of MovC, MovJ, and MovL,
    as well as their "odd" (7-axis / redundant) variants.
    """

    # ------------------------------------------------------------------
    # helpers (private)
    # ------------------------------------------------------------------

    @staticmethod
    def _append_check_params(
        params: list,
        user: int,
        tool: int,
        a: int,
        v: int,
        cp: int,
    ) -> None:
        """Append optional named parameters for check commands."""
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

    # ------------------------------------------------------------------
    # Standard Check Commands
    # ------------------------------------------------------------------

    def check_mov_c(
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
        j1c: float,
        j2c: float,
        j3c: float,
        j4c: float,
        j5c: float,
        j6c: float,
        user: int = -1,
        tool: int = -1,
        a: int = -1,
        v: int = -1,
        cp: int = -1,
    ) -> str:
        """Pre-check a circular (MovC) motion for reachability/collision.

        Args:
            j1a: Joint-1 of the first via point.
            j2a: Joint-2 of the first via point.
            j3a: Joint-3 of the first via point.
            j4a: Joint-4 of the first via point.
            j5a: Joint-5 of the first via point.
            j6a: Joint-6 of the first via point.
            j1b: Joint-1 of the second via point.
            j2b: Joint-2 of the second via point.
            j3b: Joint-3 of the second via point.
            j4b: Joint-4 of the second via point.
            j5b: Joint-5 of the second via point.
            j6b: Joint-6 of the second via point.
            j1c: Joint-1 of the target point.
            j2c: Joint-2 of the target point.
            j3c: Joint-3 of the target point.
            j4c: Joint-4 of the target point.
            j5c: Joint-5 of the target point.
            j6c: Joint-6 of the target point.
            user: User coordinate system index. -1 = not set.
            tool: Tool coordinate system index. -1 = not set.
            a: Acceleration. -1 = not set.
            v: Velocity. -1 = not set.
            cp: Continuous path setting. -1 = not set.

        Returns:
            Raw response string from robot.
        """
        string = (
            "CheckMovC("
            f"joint={{{j1a:f},{j2a:f},{j3a:f},{j4a:f},{j5a:f},{j6a:f}}},"
            f"joint={{{j1b:f},{j2b:f},{j3b:f},{j4b:f},{j5b:f},{j6b:f}}},"
            f"joint={{{j1c:f},{j2c:f},{j3c:f},{j4c:f},{j5c:f},{j6c:f}}}"
        )
        params = []
        self._append_check_params(params, user, tool, a, v, cp)
        if params:
            string += "," + ",".join(params)
        string += ")"
        return self.send_recv_msg(string)

    def check_mov_j(
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
    ) -> str:
        """Pre-check a joint (MovJ) motion for reachability/collision.

        Args:
            j1a: Joint-1 of the first point.
            j2a: Joint-2 of the first point.
            j3a: Joint-3 of the first point.
            j4a: Joint-4 of the first point.
            j5a: Joint-5 of the first point.
            j6a: Joint-6 of the first point.
            j1b: Joint-1 of the second point.
            j2b: Joint-2 of the second point.
            j3b: Joint-3 of the second point.
            j4b: Joint-4 of the second point.
            j5b: Joint-5 of the second point.
            j6b: Joint-6 of the second point.
            user: User coordinate system index. -1 = not set.
            tool: Tool coordinate system index. -1 = not set.
            a: Acceleration. -1 = not set.
            v: Velocity. -1 = not set.
            cp: Continuous path setting. -1 = not set.

        Returns:
            Raw response string from robot.
        """
        string = (
            "CheckMovJ("
            f"joint={{{j1a:f},{j2a:f},{j3a:f},{j4a:f},{j5a:f},{j6a:f}}},"
            f"joint={{{j1b:f},{j2b:f},{j3b:f},{j4b:f},{j5b:f},{j6b:f}}}"
        )
        params = []
        self._append_check_params(params, user, tool, a, v, cp)
        if params:
            string += "," + ",".join(params)
        string += ")"
        return self.send_recv_msg(string)

    def check_mov_l(
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
    ) -> str:
        """Pre-check a linear (MovL) motion for reachability/collision.

        Args:
            j1a: Joint-1 of the first point.
            j2a: Joint-2 of the first point.
            j3a: Joint-3 of the first point.
            j4a: Joint-4 of the first point.
            j5a: Joint-5 of the first point.
            j6a: Joint-6 of the first point.
            j1b: Joint-1 of the second point.
            j2b: Joint-2 of the second point.
            j3b: Joint-3 of the second point.
            j4b: Joint-4 of the second point.
            j5b: Joint-5 of the second point.
            j6b: Joint-6 of the second point.
            user: User coordinate system index. -1 = not set.
            tool: Tool coordinate system index. -1 = not set.
            a: Acceleration. -1 = not set.
            v: Velocity. -1 = not set.
            cp: Continuous path setting. -1 = not set.

        Returns:
            Raw response string from robot.
        """
        string = (
            "CheckMovL("
            f"joint={{{j1a:f},{j2a:f},{j3a:f},{j4a:f},{j5a:f},{j6a:f}}},"
            f"joint={{{j1b:f},{j2b:f},{j3b:f},{j4b:f},{j5b:f},{j6b:f}}}"
        )
        params = []
        self._append_check_params(params, user, tool, a, v, cp)
        if params:
            string += "," + ",".join(params)
        string += ")"
        return self.send_recv_msg(string)

    # ------------------------------------------------------------------
    # Odd (7-axis / Redundant) Check Commands
    # ------------------------------------------------------------------

    def check_odd_mov_c(
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
        j1c: float,
        j2c: float,
        j3c: float,
        j4c: float,
        j5c: float,
        j6c: float,
        user: int = -1,
        tool: int = -1,
        a: int = -1,
        v: int = -1,
        cp: int = -1,
    ) -> str:
        """Pre-check an odd-axis circular (MovC) motion.

        Args:
            j1a: Joint-1 of the first via point.
            j2a: Joint-2 of the first via point.
            j3a: Joint-3 of the first via point.
            j4a: Joint-4 of the first via point.
            j5a: Joint-5 of the first via point.
            j6a: Joint-6 of the first via point.
            j1b: Joint-1 of the second via point.
            j2b: Joint-2 of the second via point.
            j3b: Joint-3 of the second via point.
            j4b: Joint-4 of the second via point.
            j5b: Joint-5 of the second via point.
            j6b: Joint-6 of the second via point.
            j1c: Joint-1 of the target point.
            j2c: Joint-2 of the target point.
            j3c: Joint-3 of the target point.
            j4c: Joint-4 of the target point.
            j5c: Joint-5 of the target point.
            j6c: Joint-6 of the target point.
            user: User coordinate system index. -1 = not set.
            tool: Tool coordinate system index. -1 = not set.
            a: Acceleration. -1 = not set.
            v: Velocity. -1 = not set.
            cp: Continuous path setting. -1 = not set.

        Returns:
            Raw response string from robot.
        """
        string = (
            "CheckOddMovC("
            f"joint={{{j1a:f},{j2a:f},{j3a:f},{j4a:f},{j5a:f},{j6a:f}}},"
            f"joint={{{j1b:f},{j2b:f},{j3b:f},{j4b:f},{j5b:f},{j6b:f}}},"
            f"joint={{{j1c:f},{j2c:f},{j3c:f},{j4c:f},{j5c:f},{j6c:f}}}"
        )
        params = []
        self._append_check_params(params, user, tool, a, v, cp)
        if params:
            string += "," + ",".join(params)
        string += ")"
        return self.send_recv_msg(string)

    def check_odd_mov_j(
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
    ) -> str:
        """Pre-check an odd-axis joint (MovJ) motion.

        Args:
            j1a: Joint-1 of the first point.
            j2a: Joint-2 of the first point.
            j3a: Joint-3 of the first point.
            j4a: Joint-4 of the first point.
            j5a: Joint-5 of the first point.
            j6a: Joint-6 of the first point.
            j1b: Joint-1 of the second point.
            j2b: Joint-2 of the second point.
            j3b: Joint-3 of the second point.
            j4b: Joint-4 of the second point.
            j5b: Joint-5 of the second point.
            j6b: Joint-6 of the second point.
            user: User coordinate system index. -1 = not set.
            tool: Tool coordinate system index. -1 = not set.
            a: Acceleration. -1 = not set.
            v: Velocity. -1 = not set.
            cp: Continuous path setting. -1 = not set.

        Returns:
            Raw response string from robot.
        """
        string = (
            "CheckOddMovJ("
            f"joint={{{j1a:f},{j2a:f},{j3a:f},{j4a:f},{j5a:f},{j6a:f}}},"
            f"joint={{{j1b:f},{j2b:f},{j3b:f},{j4b:f},{j5b:f},{j6b:f}}}"
        )
        params = []
        self._append_check_params(params, user, tool, a, v, cp)
        if params:
            string += "," + ",".join(params)
        string += ")"
        return self.send_recv_msg(string)

    def check_odd_mov_l(
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
    ) -> str:
        """Pre-check an odd-axis linear (MovL) motion.

        Args:
            j1a: Joint-1 of the first point.
            j2a: Joint-2 of the first point.
            j3a: Joint-3 of the first point.
            j4a: Joint-4 of the first point.
            j5a: Joint-5 of the first point.
            j6a: Joint-6 of the first point.
            j1b: Joint-1 of the second point.
            j2b: Joint-2 of the second point.
            j3b: Joint-3 of the second point.
            j4b: Joint-4 of the second point.
            j5b: Joint-5 of the second point.
            j6b: Joint-6 of the second point.
            user: User coordinate system index. -1 = not set.
            tool: Tool coordinate system index. -1 = not set.
            a: Acceleration. -1 = not set.
            v: Velocity. -1 = not set.
            cp: Continuous path setting. -1 = not set.

        Returns:
            Raw response string from robot.
        """
        string = (
            "CheckOddMovL("
            f"joint={{{j1a:f},{j2a:f},{j3a:f},{j4a:f},{j5a:f},{j6a:f}}},"
            f"joint={{{j1b:f},{j2b:f},{j3b:f},{j4b:f},{j5b:f},{j6b:f}}}"
        )
        params = []
        self._append_check_params(params, user, tool, a, v, cp)
        if params:
            string += "," + ",".join(params)
        string += ")"
        return self.send_recv_msg(string)


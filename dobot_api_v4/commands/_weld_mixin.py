"""Weld and weave commands for Dobot V4 API."""

from typing import Sequence

from ._serialization import _SerializationMixin


class _WeldMixin(_SerializationMixin):
    """Mixin for arc-track welding, weave, and weld-arc-speed commands.

    Includes arc-track start/end/params, arc-track offset, relative-point
    weld line/arc helpers, weave start/end/params, and weld arc speed control.
    """

    # ------------------------------------------------------------------
    # Arc Track
    # ------------------------------------------------------------------

    def arc_track_start(self) -> str:
        """Start arc tracking.

        Returns:
            Raw response string from robot.
        """
        return self.send_recv_msg("ArcTrackStart()")

    ArcTrackStart = arc_track_start

    def arc_track_params(
        self,
        sample_time: int,
        coordinate_type: int,
        up_down_compensation_min: float,
        up_down_compensation_max: float,
        up_down_compensation_offset: float,
        left_right_compensation_min: float,
        left_right_compensation_max: float,
        left_right_compensation_offset: float,
    ) -> str:
        """Set arc tracking parameters.

        Args:
            sample_time: Sampling interval.
            coordinate_type: Coordinate system type.
            up_down_compensation_min: Minimum up/down compensation.
            up_down_compensation_max: Maximum up/down compensation.
            up_down_compensation_offset: Up/down compensation offset.
            left_right_compensation_min: Minimum left/right compensation.
            left_right_compensation_max: Maximum left/right compensation.
            left_right_compensation_offset: Left/right compensation offset.

        Returns:
            Raw response string from robot.
        """
        string = "ArcTrackParams({:d},{:d},{:f},{:f},{:f},{:f},{:f},{:f})".format(
            sample_time,
            coordinate_type,
            up_down_compensation_min,
            up_down_compensation_max,
            up_down_compensation_offset,
            left_right_compensation_min,
            left_right_compensation_max,
            left_right_compensation_offset,
        )
        return self.send_recv_msg(string)

    ArcTrackParams = arc_track_params

    def arc_track_end(self) -> str:
        """End arc tracking.

        Returns:
            Raw response string from robot.
        """
        return self.send_recv_msg("ArcTrackEnd()")

    ArcTrackEnd = arc_track_end

    def set_arc_track_offset(
        self,
        offset_x: float,
        offset_y: float,
        offset_z: float,
        offset_rx: float,
        offset_ry: float,
        offset_rz: float,
    ) -> str:
        """Set arc tracking offset.

        Args:
            offset_x: X-axis offset.
            offset_y: Y-axis offset.
            offset_z: Z-axis offset.
            offset_rx: Rx-axis offset.
            offset_ry: Ry-axis offset.
            offset_rz: Rz-axis offset.

        Returns:
            Raw response string from robot.
        """
        string = "SetArcTrackOffset({{{:f},{:f},{:f},{:f},{:f},{:f}}})".format(
            offset_x, offset_y, offset_z, offset_rx, offset_ry, offset_rz
        )
        return self.send_recv_msg(string)

    SetArcTrackOffset = set_arc_track_offset

    # ------------------------------------------------------------------
    # Relative Point Weld
    # ------------------------------------------------------------------

    def rel_point_weld_line(
        self,
        start_x: float,
        end_x: float,
        y: float,
        z: float,
        work_angle: float,
        travel_angle: float,
        p1: Sequence[float],
        p2: Sequence[float],
    ) -> str:
        """Execute a relative-point weld line motion.

        Args:
            start_x: Start X position.
            end_x: End X position.
            y: Y position.
            z: Z position.
            work_angle: Work angle.
            travel_angle: Travel angle.
            p1: First pose (6 elements: x, y, z, rx, ry, rz).
            p2: Second pose (6 elements: x, y, z, rx, ry, rz).

        Returns:
            Raw response string from robot.
        """
        string = (
            "RelPointWeldLine("
            "{:f},{:f},{:f},{:f},{:f},{:f},"
            "{{{:f},{:f},{:f},{:f},{:f},{:f}}},"
            "{{{:f},{:f},{:f},{:f},{:f},{:f}}})"
        ).format(
            start_x,
            end_x,
            y,
            z,
            work_angle,
            travel_angle,
            p1[0],
            p1[1],
            p1[2],
            p1[3],
            p1[4],
            p1[5],
            p2[0],
            p2[1],
            p2[2],
            p2[3],
            p2[4],
            p2[5],
        )
        return self.send_recv_msg(string)

    RelPointWeldLine = rel_point_weld_line

    def rel_point_weld_arc(
        self,
        start_x: float,
        end_x: float,
        y: float,
        z: float,
        work_angle: float,
        travel_angle: float,
        p1: Sequence[float],
        p2: Sequence[float],
        p3: Sequence[float],
    ) -> str:
        """Execute a relative-point weld arc motion.

        Args:
            start_x: Start X position.
            end_x: End X position.
            y: Y position.
            z: Z position.
            work_angle: Work angle.
            travel_angle: Travel angle.
            p1: First pose (6 elements: x, y, z, rx, ry, rz).
            p2: Second pose (6 elements: x, y, z, rx, ry, rz).
            p3: Third pose (6 elements: x, y, z, rx, ry, rz).

        Returns:
            Raw response string from robot.
        """
        string = (
            "RelPointWeldArc("
            "{:f},{:f},{:f},{:f},{:f},{:f},"
            "{{{:f},{:f},{:f},{:f},{:f},{:f}}},"
            "{{{:f},{:f},{:f},{:f},{:f},{:f}}},"
            "{{{:f},{:f},{:f},{:f},{:f},{:f}}})"
        ).format(
            start_x,
            end_x,
            y,
            z,
            work_angle,
            travel_angle,
            p1[0],
            p1[1],
            p1[2],
            p1[3],
            p1[4],
            p1[5],
            p2[0],
            p2[1],
            p2[2],
            p2[3],
            p2[4],
            p2[5],
            p3[0],
            p3[1],
            p3[2],
            p3[3],
            p3[4],
            p3[5],
        )
        return self.send_recv_msg(string)

    RelPointWeldArc = rel_point_weld_arc

    # ------------------------------------------------------------------
    # Weave
    # ------------------------------------------------------------------

    def weave_start(self) -> str:
        """Start weave motion.

        Returns:
            Raw response string from robot.
        """
        return self.send_recv_msg("WeaveStart()")

    WeaveStart = weave_start

    def weave_params(
        self,
        weld_type: int,
        frequency: float,
        left_amplitude: float,
        right_amplitude: float,
        direction: int,
        stop_mode: int,
        stop_time1: int,
        stop_time2: int,
        stop_time3: int,
        stop_time4: int,
        radius: float,
        radian: float,
        **kwargs,
    ) -> str:
        """Set weave parameters.

        Args:
            weld_type: Weld type identifier.
            frequency: Weave frequency.
            left_amplitude: Left-side weave amplitude.
            right_amplitude: Right-side weave amplitude.
            direction: Weave direction.
            stop_mode: Stop mode setting.
            stop_time1: First stop time.
            stop_time2: Second stop time.
            stop_time3: Third stop time.
            stop_time4: Fourth stop time.
            radius: Weave radius.
            radian: Weave radian.
            **kwargs: Additional key=value parameters appended to the command.

        Returns:
            Raw response string from robot.
        """
        string = "WeaveParams({:d},{:f},{:f},{:f},{:d},{:d},{:d},{:d},{:d},{:d},{:f},{:f}".format(
            weld_type,
            frequency,
            left_amplitude,
            right_amplitude,
            direction,
            stop_mode,
            stop_time1,
            stop_time2,
            stop_time3,
            stop_time4,
            radius,
            radian,
        )
        if kwargs:
            for key, value in kwargs.items():
                string += ",{}={}".format(key, value)
        string += ")"
        return self.send_recv_msg(string)

    WeaveParams = weave_params

    def weave_end(self) -> str:
        """End weave motion.

        Returns:
            Raw response string from robot.
        """
        return self.send_recv_msg("WeaveEnd()")

    WeaveEnd = weave_end

    # ------------------------------------------------------------------
    # Weld Arc Speed
    # ------------------------------------------------------------------

    def weld_arc_speed_start(self) -> str:
        """Start weld arc speed mode.

        Returns:
            Raw response string from robot.
        """
        return self.send_recv_msg("WeldArcSpeedStart()")

    WeldArcSpeedStart = weld_arc_speed_start

    def weld_arc_speed(self, speed: float) -> str:
        """Set weld arc speed.

        Args:
            speed: Arc welding speed value.

        Returns:
            Raw response string from robot.
        """
        return self.send_recv_msg("WeldArcSpeed({:f})".format(speed))

    WeldArcSpeed = weld_arc_speed

    def weld_arc_speed_end(self) -> str:
        """End weld arc speed mode.

        Returns:
            Raw response string from robot.
        """
        return self.send_recv_msg("WeldArcSpeedEnd()")

    WeldArcSpeedEnd = weld_arc_speed_end

    def weld_weave_start(
        self,
        weld_type: int,
        frequency: float,
        left_amplitude: float,
        right_amplitude: float,
        direction: int,
        stop_mode: int,
        stop_time1: int,
        stop_time2: int,
        stop_time3: int,
        stop_time4: int,
        radius: float,
        radian: float,
    ) -> str:
        """Start weld weave with parameters.

        Args:
            weld_type: Weld type identifier.
            frequency: Weave frequency.
            left_amplitude: Left-side weave amplitude.
            right_amplitude: Right-side weave amplitude.
            direction: Weave direction.
            stop_mode: Stop mode setting.
            stop_time1: First stop time.
            stop_time2: Second stop time.
            stop_time3: Third stop time.
            stop_time4: Fourth stop time.
            radius: Weave radius.
            radian: Weave radian.

        Returns:
            Raw response string from robot.
        """
        string = "WeldWeaveStart({:d},{:f},{:f},{:f},{:d},{:d},{:d},{:d},{:d},{:d},{:f},{:f})".format(
            weld_type,
            frequency,
            left_amplitude,
            right_amplitude,
            direction,
            stop_mode,
            stop_time1,
            stop_time2,
            stop_time3,
            stop_time4,
            radius,
            radian,
        )
        return self.send_recv_msg(string)

    WeldWeaveStart = weld_weave_start

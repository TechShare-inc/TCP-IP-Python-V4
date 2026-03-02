"""Weld and weave commands for Dobot V4 API."""

from collections.abc import Sequence

from ._parse import parse_ack, parse_int
from ._serialization import _SerializationMixin


class _WeldMixin(_SerializationMixin):
    """Mixin for arc-track welding, weave, and weld-arc-speed commands.

    Includes arc-track start/end/params, arc-track offset, relative-point
    weld line/arc helpers, weave start/end/params, and weld arc speed control.
    """

    # ------------------------------------------------------------------
    # Arc Track
    # ------------------------------------------------------------------

    def arc_track_start(self) -> None:
        """Start arc tracking.

        Returns:
            Raw response string from robot.
        """
        return parse_ack(self.send_recv_msg("ArcTrackStart()"))

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
    ) -> None:
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
        string = (
            f"ArcTrackParams({sample_time:d},{coordinate_type:d},"
            f"{up_down_compensation_min:f},{up_down_compensation_max:f},"
            f"{up_down_compensation_offset:f},"
            f"{left_right_compensation_min:f},"
            f"{left_right_compensation_max:f},"
            f"{left_right_compensation_offset:f})"
        )
        return parse_ack(self.send_recv_msg(string))

    def arc_track_end(self) -> None:
        """End arc tracking.

        Returns:
            Raw response string from robot.
        """
        return parse_ack(self.send_recv_msg("ArcTrackEnd()"))

    def set_arc_track_offset(
        self,
        offset_x: float,
        offset_y: float,
        offset_z: float,
        offset_rx: float,
        offset_ry: float,
        offset_rz: float,
    ) -> None:
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
        string = (
            f"SetArcTrackOffset({{{offset_x:f},{offset_y:f},"
            f"{offset_z:f},{offset_rx:f},"
            f"{offset_ry:f},{offset_rz:f}}})"
        )
        return parse_ack(self.send_recv_msg(string))

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
    ) -> int:
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
            f"{start_x:f},{end_x:f},{y:f},{z:f},{work_angle:f},{travel_angle:f},"
            f"{{{p1[0]:f},{p1[1]:f},{p1[2]:f},{p1[3]:f},{p1[4]:f},{p1[5]:f}}},"
            f"{{{p2[0]:f},{p2[1]:f},{p2[2]:f},{p2[3]:f},{p2[4]:f},{p2[5]:f}}})"
        )
        return parse_int(self.send_recv_msg(string))

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
    ) -> int:
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
            f"{start_x:f},{end_x:f},{y:f},{z:f},{work_angle:f},{travel_angle:f},"
            f"{{{p1[0]:f},{p1[1]:f},{p1[2]:f},{p1[3]:f},{p1[4]:f},{p1[5]:f}}},"
            f"{{{p2[0]:f},{p2[1]:f},{p2[2]:f},{p2[3]:f},{p2[4]:f},{p2[5]:f}}},"
            f"{{{p3[0]:f},{p3[1]:f},{p3[2]:f},{p3[3]:f},{p3[4]:f},{p3[5]:f}}})"
        )
        return parse_int(self.send_recv_msg(string))

    # ------------------------------------------------------------------
    # Weave
    # ------------------------------------------------------------------

    def weave_start(self) -> None:
        """Start weave motion.

        Returns:
            Raw response string from robot.
        """
        return parse_ack(self.send_recv_msg("WeaveStart()"))

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
    ) -> None:
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
        string = (
            f"WeaveParams({weld_type:d},{frequency:f},"
            f"{left_amplitude:f},{right_amplitude:f},"
            f"{direction:d},{stop_mode:d},"
            f"{stop_time1:d},{stop_time2:d},"
            f"{stop_time3:d},{stop_time4:d},"
            f"{radius:f},{radian:f}"
        )
        if kwargs:
            for key, value in kwargs.items():
                string += f",{key}={value}"
        string += ")"
        return parse_ack(self.send_recv_msg(string))

    def weave_end(self) -> None:
        """End weave motion.

        Returns:
            Raw response string from robot.
        """
        return parse_ack(self.send_recv_msg("WeaveEnd()"))

    # ------------------------------------------------------------------
    # Weld Arc Speed
    # ------------------------------------------------------------------

    def weld_arc_speed_start(self) -> None:
        """Start weld arc speed mode.

        Returns:
            Raw response string from robot.
        """
        return parse_ack(self.send_recv_msg("WeldArcSpeedStart()"))

    def weld_arc_speed(self, speed: float) -> None:
        """Set weld arc speed.

        Args:
            speed: Arc welding speed value.

        Returns:
            Raw response string from robot.
        """
        return parse_ack(self.send_recv_msg(f"WeldArcSpeed({speed:f})"))

    def weld_arc_speed_end(self) -> None:
        """End weld arc speed mode.

        Returns:
            Raw response string from robot.
        """
        return parse_ack(self.send_recv_msg("WeldArcSpeedEnd()"))

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
    ) -> None:
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
        string = (
            f"WeldWeaveStart({weld_type:d},{frequency:f},"
            f"{left_amplitude:f},{right_amplitude:f},"
            f"{direction:d},{stop_mode:d},"
            f"{stop_time1:d},{stop_time2:d},"
            f"{stop_time3:d},{stop_time4:d},"
            f"{radius:f},{radian:f})"
        )
        return parse_ack(self.send_recv_msg(string))

"""
Dobot API Movement Commands Module

This module contains the DobotApiMove class with all robot movement commands.
Adopts V3's architectural pattern of separating movement functionality
into its own class, while preserving all V4 method signatures and features.

Movement categories included:
- Basic motion: MovJ, MovL, MovC, MovLIO, MovJIO
- Servo control: ServoJ, ServoP
- Arc/Circle motion: Arc, Circle
- Relative motion: RelMovJUser, RelMovLUser, RelMovJTool, RelMovLTool, RelJointMovJ
- Trajectory playback: StartPath, GetStartPose
- V4-specific: RunTo, MovS, CheckMovJ, CheckMovL, CheckMovC
- Conveyor tracking: CnvInit, CnvMovL, CnvMovC
- Force control: FCForceMode, FCOff, FCSet* methods
- Welding: WeaveStart, WeaveEnd, ArcTrackStart, WeldArcSpeed
"""

from .base import DobotApi


class DobotApiMove(DobotApi):
    """
    Dobot API Movement Commands Class

    Inherits from DobotApi base class and provides all movement-related methods
    for controlling the Dobot robot arm.
    """

    def __init__(self, ip: str, port: int, *args) -> None:
        """
        Initialize DobotApiMove instance

        Args:
            ip: Robot IP address
            port: Robot port number
            *args: Additional arguments passed to base class
        """
        super().__init__(ip, port, *args)

    def _fmt(self, v):
        """
        Format a value for command string construction

        Args:
            v: Value to format (can be list, tuple, float, int, or other)

        Returns:
            Formatted string representation of the value
        """
        if isinstance(v, (list, tuple)):
            return "{" + ",".join([self._fmt(x) for x in v]) + "}"
        if isinstance(v, float):
            return "{:f}".format(v)
        if isinstance(v, int):
            return "{:d}".format(v)
        return str(v)

    def _build_cmd(self, name, *args, **kwargs):
        """
        Build a command string from name and arguments

        Args:
            name: Command name
            *args: Positional arguments
            **kwargs: Keyword arguments

        Returns:
            Formatted command string
        """
        parts = []
        for a in args:
            parts.append(self._fmt(a))
        for k, v in kwargs.items():
            parts.append(f"{k}={self._fmt(v)}")
        return f"{name}(" + ",".join(parts) + ")"

    def MovJ(
        self,
        a1,
        b1,
        c1,
        d1,
        e1,
        f1,
        coordinateMode,
        user=-1,
        tool=-1,
        a=-1,
        v=-1,
        cp=-1,
    ):
        """
        Description
        Move from the current position to the target position through joint motion.
        Required parameter:
        Parameter name     Type     Description
        P     string     Target point (joint variables or posture variables)
        coordinateMode     int      Coordinate mode of the target point, 0: pose, 1: joint
        Optional parameter:
        Parameter name     Type     Description
        user     int     user coordinate system
        tool     int     tool coordinate system
        a     int     acceleration rate of the robot arm when executing this command. Range: (0,100].
        v     int     velocity rate of the robot arm when executing this command. Range: (0,100].
        cp     int     continuous path rate. Range: [0,100].
        """
        string = ""
        if coordinateMode == 0:
            string = "MovJ(pose={{{:f},{:f},{:f},{:f},{:f},{:f}}}".format(
                a1, b1, c1, d1, e1, f1
            )
        elif coordinateMode == 1:
            string = "MovJ(joint={{{:f},{:f},{:f},{:f},{:f},{:f}}}".format(
                a1, b1, c1, d1, e1, f1
            )
        else:
            print("coordinateMode param is wrong")
            return ""
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
        for ii in params:
            string = string + "," + ii
        string = string + ")"
        return self.sendRecvMsg(string)

    def MovL(
        self,
        a1,
        b1,
        c1,
        d1,
        e1,
        f1,
        coordinateMode,
        user=-1,
        tool=-1,
        a=-1,
        v=-1,
        speed=-1,
        cp=-1,
        r=-1,
    ):
        """
        Description
        Move from the current position to the target position in a linear mode.
        Required parameter:
        Parameter name     Type     Description
        P     string     Target point (joint variables or posture variables)
        coordinateMode     int      Coordinate mode of the target point, 0: pose, 1: joint
        Optional parameter:
        Parameter name     Type     Description
        user     int     user coordinate system
        tool     int     tool coordinate system
        a     int     acceleration rate of the robot arm when executing this command. Range: (0,100].
        v     int     velocity rate of the robot arm when executing this command, incompatible with "speed". Range: (0,100].
        speed     int     target speed of the robot arm when executing this command, incompatible with "v". If both "speed" and "v" exist, speed takes precedence. Range: [0, maximum motion speed], unit: mm/s.
        cp     int     continuous path rate, incompatible with "r". Range: [0,100].
        r     int     continuous path radius, incompatible with "cp". If both "r" and "cp" exist, r takes precedence. Unit: mm.
        """
        string = ""
        if coordinateMode == 0:
            string = "MovL(pose={{{:f},{:f},{:f},{:f},{:f},{:f}}}".format(
                a1, b1, c1, d1, e1, f1
            )
        elif coordinateMode == 1:
            string = "MovL(joint={{{:f},{:f},{:f},{:f},{:f},{:f}}}".format(
                a1, b1, c1, d1, e1, f1
            )
        else:
            print("coordinateMode  param  is wrong")
            return ""
        params = []
        if user != -1:
            params.append("user={:d}".format(user))
        if tool != -1:
            params.append("tool={:d}".format(tool))
        if a != -1:
            params.append("a={:d}".format(a))
        if v != -1 and speed != -1:
            params.append("speed={:d}".format(speed))
        elif speed != -1:
            params.append("speed={:d}".format(speed))
        elif v != -1:
            params.append("v={:d}".format(v))
        if cp != -1 and r != -1:
            params.append("r={:d}".format(r))
        elif r != -1:
            params.append("r={:d}".format(r))
        elif cp != -1:
            params.append("cp={:d}".format(cp))
        for ii in params:
            string = string + "," + ii
        string = string + ")"
        return self.sendRecvMsg(string)

    def ServoJ(self, J1, J2, J3, J4, J5, J6, t=-1.0, aheadtime=-1.0, gain=-1.0):
        """
        Joint string Target point joint variables
        t float Optional parameter.Running time of the point, unit: s, value range: [0.02,3600.0], default value:0.1
        aheadtime float Optional parameter.Advanced time, similar to the D in PID control. Scalar, no unit, valuerange: [20.0,100.0], default value: 50.
        gain float Optional parameter.Proportional gain of the target position, similar to the P in PID control.Scalar, no unit, value range: [200.0,1000.0], default value: 500.
        """
        string = ""
        string = "ServoJ({:f},{:f},{:f},{:f},{:f},{:f}".format(J1, J2, J3, J4, J5, J6)
        params = []
        if t != -1:
            params.append("t={:f}".format(t))
        if aheadtime != -1:
            params.append("aheadtime={:f}".format(aheadtime))
        if gain != -1:
            params.append("gain={:f}".format(gain))
        for ii in params:
            string = string + "," + ii
        string = string + ")"
        return self.sendRecvMsg(string)

    def ServoP(self, X, Y, Z, RX, RY, RZ, t=-1.0, aheadtime=-1.0, gain=-1.0):
        """
        Pose string  Target point posture variables. The reference coordinate system is the global user and tool coordinate system, see the User and Tool command descriptions in Settings command (the default values are both 0
        t float Optional parameter.Running time of the point, unit: s, value range: [0.02,3600.0], default value:0.1
        aheadtime float Optional parameter.Advanced time, similar to the D in PID control. Scalar, no unit, valuerange: [20.0,100.0], default value: 50.
        gain float Optional parameter.Proportional gain of the target position, similar to the P in PID control.Scalar, no unit, value range: [200.0,1000.0], default value: 500.
        """
        string = ""
        string = "ServoP({:f},{:f},{:f},{:f},{:f},{:f}".format(X, Y, Z, RX, RY, RZ)
        params = []
        if t != -1:
            params.append("t={:f}".format(t))
        if aheadtime != -1:
            params.append("aheadtime={:f}".format(aheadtime))
        if gain != -1:
            params.append("gain={:f}".format(gain))
        for ii in params:
            string = string + "," + ii
        string = string + ")"
        return self.sendRecvMsg(string)

    def MovLIO(
        self,
        a1,
        b1,
        c1,
        d1,
        e1,
        f1,
        coordinateMode,
        Mode,
        Distance,
        Index,
        Status,
        user=-1,
        tool=-1,
        a=-1,
        v=-1,
        speed=-1,
        cp=-1,
        r=-1,
    ):
        """
        Description
        Move from the current position to the target position in a linear mode, and set the status of digital output port when the robot is moving.
        Required parameter:
        Parameter name     Type     Description
        P     string     Target point (joint variables or posture variables)
        coordinateMode     int      Coordinate mode of the target point, 0: pose, 1: joint
        {Mode,Distance,Index,Status}: digital output parameters, used to set the specified DO to be triggered when the robot arm moves to a specified distance or percentage. Multiple groups of parameters can be set.
        Parameter name     Type     Description
        Mode     int     Trigger mode. 0: distance percentage, 1: distance value.
        Distance     int     Specified distance.
        If Distance is positive, it refers to the distance away from the starting point;
        If Distance is negative, it refers to the distance away from the target point;
        If Mode is 0, Distance refers to the percentage of total distance. Range: (0,100];
        If Mode is 1, Distance refers to the distance value. Unit: mm.
        Index     int     DO index
        Status     int     DO status. 0: no signal, 1: have signal.
        Optional parameter:
        Parameter name     Type     Description
        user     int     user coordinate system
        tool     int     tool coordinate system
        a     int     acceleration rate of the robot arm when executing this command. Range: (0,100].
        v     int     velocity rate of the robot arm when executing this command, incompatible with "speed". Range: (0,100].
        speed     int     target speed of the robot arm when executing this command, incompatible with "v". If both "speed" and "v" exist, speed takes precedence. Range: [0, maximum motion speed], unit: mm/s.
        cp     int     continuous path rate, incompatible with "r". Range: [0,100].
        r     int     continuous path radius, incompatible with "cp". If both "r" and "cp" exist, r takes precedence. Unit: mm.
        """
        string = ""
        if coordinateMode == 0:
            string = "MovLIO(pose={{{:f},{:f},{:f},{:f},{:f},{:f}}},{{{:d},{:d},{:d},{:d}}}".format(
                a1, b1, c1, d1, e1, f1, Mode, Distance, Index, Status
            )
        elif coordinateMode == 1:
            string = "MovLIO(joint={{{:f},{:f},{:f},{:f},{:f},{:f}}},{{{:d},{:d},{:d},{:d}}}".format(
                a1, b1, c1, d1, e1, f1, Mode, Distance, Index, Status
            )
        else:
            print("coordinateMode  param  is wrong")
            return ""
        params = []
        if user != -1:
            params.append("user={:d}".format(user))
        if tool != -1:
            params.append("tool={:d}".format(tool))
        if a != -1:
            params.append("a={:d}".format(a))
        if v != -1 and speed != -1:
            params.append("speed={:d}".format(speed))
        elif speed != -1:
            params.append("speed={:d}".format(speed))
        elif v != -1:
            params.append("v={:d}".format(v))
        if cp != -1 and r != -1:
            params.append("r={:d}".format(r))
        elif r != -1:
            params.append("r={:d}".format(r))
        elif cp != -1:
            params.append("cp={:d}".format(cp))
        for ii in params:
            string = string + "," + ii
        string = string + ")"
        return self.sendRecvMsg(string)

    def MovJIO(
        self,
        a1,
        b1,
        c1,
        d1,
        e1,
        f1,
        coordinateMode,
        Mode,
        Distance,
        Index,
        Status,
        user=-1,
        tool=-1,
        a=-1,
        v=-1,
        cp=-1,
    ):
        """
        Description
        Move from the current position to the target position through joint motion, and set the status of digital output port when the robot is moving.
        Required parameter:
        Parameter name     Type     Description
        P     string     Target point (joint variables or posture variables)
        coordinateMode     int      Coordinate mode of the target point, 0: pose, 1: joint
        {Mode,Distance,Index,Status}: digital output parameters, used to set the specified DO to be triggered when the robot arm moves to a specified distance or percentage. Multiple groups of parameters can be set.
        Parameter name     Type     Description
        Mode     int     Trigger mode. 0: distance percentage, 1: distance value.
        The system will synthesise the joint angles into an angular vector and calculate the angular difference between the end point and the start point as the total distance of the motion.
        Distance     int     Specified distance.
        If Distance is positive, it refers to the distance away from the starting point;
        If Distance is negative, it refers to the distance away from the target point;
        If Mode is 0, Distance refers to the percentage of total distance. Range: (0,100];
        If Mode is 1, Distance refers to the distance value. Unit: °.
        Index     int     DO index
        Status     int     DO status. 0: no signal, 1: have signal.
        Optional parameter:
        Parameter name     Type     Description
        user     int     user coordinate system
        tool     int     tool coordinate system
        a     int     acceleration rate of the robot arm when executing this command. Range: (0,100].
        v     int     velocity rate of the robot arm when executing this command. Range: (0,100].
        cp     int     continuous path rate. Range: [0,100].
        """
        string = ""
        if coordinateMode == 0:
            string = "MovJIO(pose={{{:f},{:f},{:f},{:f},{:f},{:f}}},{{{:d},{:d},{:d},{:d}}}".format(
                a1, b1, c1, d1, e1, f1, Mode, Distance, Index, Status
            )
        elif coordinateMode == 1:
            string = "MovJIO(joint={{{:f},{:f},{:f},{:f},{:f},{:f}}},{{{:d},{:d},{:d},{:d}}}".format(
                a1, b1, c1, d1, e1, f1, Mode, Distance, Index, Status
            )
        else:
            print("coordinateMode  param  is wrong")
            return ""
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
        for ii in params:
            string = string + "," + ii
        string = string + ")"
        return self.sendRecvMsg(string)

    def Arc(
        self,
        a1,
        b1,
        c1,
        d1,
        e1,
        f1,
        a2,
        b2,
        c2,
        d2,
        e2,
        f2,
        coordinateMode,
        user=-1,
        tool=-1,
        a=-1,
        v=-1,
        speed=-1,
        cp=-1,
        r=-1,
    ):
        """
        Description
        Move from the current position to the target position in an arc interpolated mode.
        As the arc needs to be determined through the current position, through point and target point, the current position should not be in a straight line determined by P1 and P2.
        Required parameter:
        Parameter name     Type     Description
        P1     string     Through point (joint variables or posture variables)
        P2     string     Target point (joint variables or posture variables)
        coordinateMode     int      Coordinate mode of the target point, 0: pose, 1: joint
        Optional parameter:
        Parameter name     Type     Description
        user     int     user coordinate system
        tool     int     tool coordinate system
        a     int     acceleration rate of the robot arm when executing this command. Range: (0,100].
        v     int     velocity rate of the robot arm when executing this command, incompatible with "speed". Range: (0,100].
        speed     int     target speed of the robot arm when executing this command, incompatible with "v". If both "speed" and "v" exist, speed takes precedence. Range: [0, maximum motion speed], unit: mm/s.
        cp     int     continuous path rate, incompatible with "r". Range: [0,100].
        r     int     continuous path radius, incompatible with "cp". If both "r" and "cp" exist, r takes precedence. Unit: mm.
        """
        string = ""
        if coordinateMode == 0:
            string = "Arc(pose={{{:f},{:f},{:f},{:f},{:f},{:f}}},pose={{{:f},{:f},{:f},{:f},{:f},{:f}}}".format(
                a1, b1, c1, d1, e1, f1, a2, b2, c2, d2, e2, f2
            )
        elif coordinateMode == 1:
            string = "Arc(joint={{{:f},{:f},{:f},{:f},{:f},{:f}}},joint={{{:f},{:f},{:f},{:f},{:f},{:f}}}".format(
                a1, b1, c1, d1, e1, f1, a2, b2, c2, d2, e2, f2
            )
        else:
            print("coordinateMode  param  is wrong")
            return ""
        params = []
        if user != -1:
            params.append("user={:d}".format(user))
        if tool != -1:
            params.append("tool={:d}".format(tool))
        if a != -1:
            params.append("a={:d}".format(a))
        if v != -1 and speed != -1:
            params.append("speed={:d}".format(speed))
        elif speed != -1:
            params.append("speed={:d}".format(speed))
        elif v != -1:
            params.append("v={:d}".format(v))
        if cp != -1 and r != -1:
            params.append("r={:d}".format(r))
        elif r != -1:
            params.append("r={:d}".format(r))
        elif cp != -1:
            params.append("cp={:d}".format(cp))
        for ii in params:
            string = string + "," + ii
        string = string + ")"
        return self.sendRecvMsg(string)

    def Circle(
        self,
        a1,
        b1,
        c1,
        d1,
        e1,
        f1,
        a2,
        b2,
        c2,
        d2,
        e2,
        f2,
        coordinateMode,
        count,
        user=-1,
        tool=-1,
        a=-1,
        v=-1,
        speed=-1,
        cp=-1,
        r=-1,
    ):
        """
        Description
        Move from the current position in a circle interpolated mode, and return to the current position after moving specified circles.
        As the circle needs to be determined through the current position, P1 and P2, the current position should not be in a straight line determined by P1 and P2, and the circle determined by the three points cannot exceed the motion range of the robot arm.
        Required parameter:
        Parameter name     Type     Description
        P1     string     Through point (joint variables or posture variables)
        P2     string     End point (joint variables or posture variables)
        coordinateMode     int      Coordinate mode of the target point, 0: pose, 1: joint
        count     int     Number of circles, range: [1,999].
        Optional parameter:
        Parameter name     Type     Description
        user     int     user coordinate system
        tool     int     tool coordinate system
        a     int     acceleration rate of the robot arm when executing this command. Range: (0,100].
        v     int     velocity rate of the robot arm when executing this command, incompatible with "speed". Range: (0,100].
        speed     int     target speed of the robot arm when executing this command, incompatible with "v". If both "speed" and "v" exist, speed takes precedence. Range: [0, maximum motion speed], unit: mm/s.
        cp     int     continuous path rate, incompatible with "r". Range: [0,100].
        r     int     continuous path radius, incompatible with "cp". If both "r" and "cp" exist, r takes precedence. Unit: mm.
        """
        string = ""
        if coordinateMode == 0:
            string = "Circle(pose={{{:f},{:f},{:f},{:f},{:f},{:f}}},pose={{{:f},{:f},{:f},{:f},{:f},{:f}}},{:d}".format(
                a1, b1, c1, d1, e1, f1, a2, b2, c2, d2, e2, f2, count
            )
        elif coordinateMode == 1:
            string = "Circle(joint={{{:f},{:f},{:f},{:f},{:f},{:f}}},joint={{{:f},{:f},{:f},{:f},{:f},{:f}}},{:d}".format(
                a1, b1, c1, d1, e1, f1, a2, b2, c2, d2, e2, f2, count
            )
        else:
            print("coordinateMode  param  is wrong")
            return ""
        params = []
        if user != -1:
            params.append("user={:d}".format(user))
        if tool != -1:
            params.append("tool={:d}".format(tool))
        if a != -1:
            params.append("a={:d}".format(a))
        if v != -1 and speed != -1:
            params.append("speed={:d}".format(speed))
        elif speed != -1:
            params.append("speed={:d}".format(speed))
        elif v != -1:
            params.append("v={:d}".format(v))
        if cp != -1 and r != -1:
            params.append("r={:d}".format(r))
        elif r != -1:
            params.append("r={:d}".format(r))
        elif cp != -1:
            params.append("cp={:d}".format(cp))
        for ii in params:
            string = string + "," + ii
        string = string + ")"
        return self.sendRecvMsg(string)

    def MoveJog(self, axis_id="", coordtype=-1, user=-1, tool=-1):
        """
        Joint motion
        axis_id: Joint motion axis, optional string value:
            J1+ J2+ J3+ J4+ J5+ J6+
            J1- J2- J3- J4- J5- J6-
            X+ Y+ Z+ Rx+ Ry+ Rz+
            X- Y- Z- Rx- Ry- Rz-
        *dynParams: Parameter Settings（coord_type, user_index, tool_index）
                    coord_type: 1: User coordinate 2: tool coordinate (default value is 1)
                    user_index: user index is 0 ~ 9 (default value is 0)
                    tool_index: tool index is 0 ~ 9 (default value is 0)
        """
        string = "MoveJog({:s}".format(axis_id)
        params = []
        if coordtype != -1:
            params.append("coordtype={:d}".format(coordtype))
        if user != -1:
            params.append("user={:d}".format(user))
        if tool != -1:
            params.append("tool={:d}".format(tool))
        for ii in params:
            string = string + "," + ii
        string = string + ")"
        return self.sendRecvMsg(string)

    def GetStartPose(self, trace_name):
        """
        Description
        Get the start point of the trajectory.
        Required parameter:
        Parameter name     Type     Description
        traceName     string     trajectory file name (with suffix)
        The trajectory file is stored in /dobot/userdata/project/process/trajectory/.
        If the name contains Chinese, the encoding of the sender must be set to UTF-8, otherwise
        it will cause an exception for receiving Chinese.
        """
        string = "GetStartPose({:s})".format(trace_name)
        return self.sendRecvMsg(string)

    def StartPath(self, trace_name, isConst=-1, multi=-1.0, user=-1, tool=-1):
        """
        traceName string
        Description
        Move according to the recorded points in the specified trajectory file to play back the recorded trajectory.
        After the trajectory playback command is successfully delivered, you can check the robot status via RobotMode command.
        ROBOT_MODE_RUNNING: the robot is in trajectory playback, ROBOT_MODE_IDLE: trajectory playback is completed,
        ROBOT_MODE_ERROR: alarm.
        Required parameter:
        Parameter name     Type     Description
        traceName string
        trajectory file name (with suffix). The trajectory file is stored in /dobot/userdata/project/process/trajectory/.
        If the name contains Chinese, the encoding of the sender must be set to UTF-8, otherwise it will cause an exception for receiving Chinese.
        Optional parameter:
        Parameter name     Type     Description
        isConst     int     if or not to play back at a constant speed.
           1: the trajectory will be played back at the global rate at a uniform rate by the arm;
           0: the trajectory will be played back at the same speed as when it was recorded, and the motion speed can be scaled equivalently using the multi parameter, where the motion speed of the arm is not affected by the global rate.
        multi     double     Speed multiplier in playback, valid only when isConst=0. Range: [0.25, 2], 1 by default.
        user     int     User coordinate system index corresponding to the specified trajectory point (use the user coordinate system index recorded in the trajectory file if not specified).
        tool     int     tool coordinate system index corresponding to the specified trajectory point (use the tool coordinate system index recorded in the trajectory file if not specified).
        """
        string = "StartPath({:s}".format(trace_name)
        params = []
        if isConst != -1:
            params.append("isConst={:d}".format(isConst))
        if multi != -1:
            params.append("multi={:f}".format(multi))
        if user != -1:
            params.append("user={:d}".format(user))
        if tool != -1:
            params.append("tool={:d}".format(tool))
        for ii in params:
            string = string + "," + ii
        string = string + ")"
        return self.sendRecvMsg(string)

    def RelMovJTool(
        self,
        offset_x,
        offset_y,
        offset_z,
        offset_rx,
        offset_ry,
        offset_rz,
        user=-1,
        tool=-1,
        a=-1,
        v=-1,
        cp=-1,
    ):
        """
        Description
        Perform relative motion along the tool coordinate system, and the end motion is joint motion.
        Required parameter:
        Parameter name     Type     Description
        offsetX     double     X-axis offset, unit: mm
        offsetY     double     Y-axis offset, unit: mm
        offsetZ     double     Z-axis offset, unit: mm
        offsetRx     double     Rx-axis offset, unit: °
        offsetRy     double     Ry-axis offset, unit: °
        offsetRz     double     Rz-axis offset, unit: °
        Optional parameter:
        Parameter name     Type     Description
        user     int     user coordinate system
        tool     int     tool coordinate system
        a     int     acceleration rate of the robot arm when executing this command. Range: (0,100].
        v     int     velocity rate of the robot arm when executing this command. Range: (0,100].
        cp     int     continuous path rate. Range: [0,100].
        """
        string = "RelMovJTool({:f},{:f},{:f},{:f},{:f},{:f}".format(
            offset_x, offset_y, offset_z, offset_rx, offset_ry, offset_rz
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
        for ii in params:
            string = string + "," + ii
        string = string + ")"
        return self.sendRecvMsg(string)

    def RelMovLTool(
        self,
        offset_x,
        offset_y,
        offset_z,
        offset_rx,
        offset_ry,
        offset_rz,
        user=-1,
        tool=-1,
        a=-1,
        v=-1,
        speed=-1,
        cp=-1,
        r=-1,
    ):
        """
        Description
        Perform relative motion along the tool coordinate system, and the end motion is linear motion.
        This command is for 6-axis robots.
        Required parameter:
        Parameter name     Type     Description
        offsetX     double     X-axis offset, unit: mm
        offsetY     double     Y-axis offset, unit: mm
        offsetZ     double     Z-axis offset, unit: mm
        offsetRx     double     Rx-axis offset, unit: °
        offsetRy     double     Ry-axis offset, unit: °
        offsetRz     double     Rz-axis offset, unit: °
        Optional parameter:
        Parameter name     Type     Description
        user     int     user coordinate system
        tool     int     tool coordinate system
        a     int     acceleration rate of the robot arm when executing this command. Range: (0,100].
        v     int     velocity rate of the robot arm when executing this command. Range: (0,100].
        speed     int     target speed of the robot arm when executing this command, incompatible with "v". If both "speed" and "v" exist, speed takes precedence. Range: [0, maximum motion speed], unit: mm/s.
        cp     int     continuous path rate, incompatible with "r". Range: [0,100].
        r     int     continuous path radius, incompatible with "cp". If both "r" and "cp" exist, r takes precedence. Unit: mm.
        """
        string = "RelMovLTool({:f},{:f},{:f},{:f},{:f},{:f}".format(
            offset_x, offset_y, offset_z, offset_rx, offset_ry, offset_rz
        )
        params = []
        if user != -1:
            params.append("user={:d}".format(user))
        if tool != -1:
            params.append("tool={:d}".format(tool))
        if a != -1:
            params.append("a={:d}".format(a))
        if v != -1 and speed != -1:
            params.append("speed={:d}".format(speed))
        elif speed != -1:
            params.append("speed={:d}".format(speed))
        elif v != -1:
            params.append("v={:d}".format(v))
        if cp != -1 and r != -1:
            params.append("r={:d}".format(r))
        elif r != -1:
            params.append("r={:d}".format(r))
        elif cp != -1:
            params.append("cp={:d}".format(cp))
        for ii in params:
            string = string + "," + ii
        string = string + ")"
        return self.sendRecvMsg(string)

    def RelMovJUser(
        self,
        offset_x,
        offset_y,
        offset_z,
        offset_rx,
        offset_ry,
        offset_rz,
        user=-1,
        tool=-1,
        a=-1,
        v=-1,
        cp=-1,
    ):
        """
        Description
        Perform relative motion along the user coordinate system, and the end motion is joint motion.
        Required parameter:
        Parameter name     Type     Description
        offsetX     double     X-axis offset, unit: mm
        offsetY     double     Y-axis offset, unit: mm
        offsetZ     double     Z-axis offset, unit: mm
        offsetRx     double     Rx-axis offset, unit: °
        offsetRy     double     Ry-axis offset, unit: °
        offsetRz     double     Rz-axis offset, unit: °
        Optional parameter:
        Parameter name     Type     Description
        user     int     user coordinate system
        tool     int     tool coordinate system
        a     int     acceleration rate of the robot arm when executing this command. Range: (0,100].
        v     int     velocity rate of the robot arm when executing this command. Range: (0,100].
        cp     int     continuous path rate. Range: [0,100].
        """
        string = "RelMovJUser({:f},{:f},{:f},{:f},{:f},{:f}".format(
            offset_x, offset_y, offset_z, offset_rx, offset_ry, offset_rz
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
        for ii in params:
            string = string + "," + ii
        string = string + ")"
        return self.sendRecvMsg(string)

    def RelMovLUser(
        self,
        offset_x,
        offset_y,
        offset_z,
        offset_rx,
        offset_ry,
        offset_rz,
        user=-1,
        tool=-1,
        a=-1,
        v=-1,
        speed=-1,
        cp=-1,
        r=-1,
    ):
        """
        Description
        Perform relative motion along the user coordinate system, and the end motion is linear motion.
        Required parameter:
        Parameter name     Type     Description
        offsetX     double     X-axis offset, unit: mm
        offsetY     double     Y-axis offset, unit: mm
        offsetZ     double     Z-axis offset, unit: mm
        offsetRx     double     Rx-axis offset, unit: °
        offsetRy     double     Ry-axis offset, unit: °
        offsetRz     double     Rz-axis offset, unit: °
        Optional parameter:
        Parameter name     Type     Description
        user     int     user coordinate system
        tool     int     tool coordinate system
        a     int     acceleration rate of the robot arm when executing this command. Range: (0,100].
        v     int     velocity rate of the robot arm when executing this command. Range: (0,100].
        speed     int     target speed of the robot arm when executing this command, incompatible with "v". If both "speed" and "v" exist, speed takes precedence. Range: [0, maximum motion speed], unit: mm/s.
        cp     int     continuous path rate, incompatible with "r". Range: [0,100].
        r     int     continuous path radius, incompatible with "cp". If both "r" and "cp" exist, r takes precedence. Unit: mm.
        """
        string = "RelMovLUser({:f},{:f},{:f},{:f},{:f},{:f}".format(
            offset_x, offset_y, offset_z, offset_rx, offset_ry, offset_rz
        )
        params = []
        if user != -1:
            params.append("user={:d}".format(user))
        if tool != -1:
            params.append("tool={:d}".format(tool))
        if a != -1:
            params.append("a={:d}".format(a))
        if v != -1 and speed != -1:
            params.append("speed={:d}".format(speed))
        elif speed != -1:
            params.append("speed={:d}".format(speed))
        elif v != -1:
            params.append("v={:d}".format(v))
        if cp != -1 and r != -1:
            params.append("r={:d}".format(r))
        elif r != -1:
            params.append("r={:d}".format(r))
        elif cp != -1:
            params.append("cp={:d}".format(cp))
        for ii in params:
            string = string + "," + ii
        string = string + ")"
        return self.sendRecvMsg(string)

    def RelJointMovJ(
        self,
        offset_x,
        offset_y,
        offset_z,
        offset_rx,
        offset_ry,
        offset_rz,
        a=-1,
        v=-1,
        cp=-1,
    ):
        """
        Description
        Perform relative motion along the joint coordinate system, and the end motion is joint motion.
        Required parameter:
        Parameter name     Type     Description
        offset1     double     J1-axis offset, unit: °
        offset2     double     J2-axis offset, unit: °
        offset3     double     J3-axis offset, unit: °
        offset4     double     J4-axis offset, unit: °
        offset5     double     J5-axis offset, unit: °
        offset6     double     J6-axis offset, unit: °
        Optional parameter:
        Parameter name     Type     Description
        a     int     acceleration rate of the robot arm when executing this command. Range: (0,100].
        v     int     velocity rate of the robot arm when executing this command. Range: (0,100].
        cp     int     continuous path rate. Range: [0,100].
        """
        string = "RelJointMovJ({:f},{:f},{:f},{:f},{:f},{:f}".format(
            offset_x, offset_y, offset_z, offset_rx, offset_ry, offset_rz
        )
        params = []
        if a != -1:
            params.append("a={:d}".format(a))
        if v != -1:
            params.append("v={:d}".format(v))
        if cp != -1:
            params.append("cp={:d}".format(cp))
        for ii in params:
            string = string + "," + ii
        string = string + ")"
        return self.sendRecvMsg(string)

    def GetCurrentCommandID(self):
        """
        Get the algorithm queue ID of the currently executed command, which can be used to judge which command is currently being executed by the robot.
        """
        string = "GetCurrentCommandID()"
        return self.sendRecvMsg(string)


    def SetResumeOffset(self, distance):
        """
        """
        string = "SetResumeOffset({:f})".format(distance)
        return self.sendRecvMsg(string)

    def PathRecovery(self):
        """
        """
        string = "PathRecovery()"
        return self.sendRecvMsg(string)

    def PathRecoveryStop(self):
        """
        """
        string = "PathRecoveryStop()"
        return self.sendRecvMsg(string)

    def PathRecoveryStatus(self):
        """
        """
        string = "PathRecoveryStatus()"
        return self.sendRecvMsg(string)

    def LogExportUSB(self, range):
        """
        """
        string = "LogExportUSB({:d})".format(range)
        return self.sendRecvMsg(string)

    def GetExportStatus(self):
        """
        """
        string = "GetExportStatus()"
        return self.sendRecvMsg(string)

    def EnableFTSensor(self, status):
        """
        """
        string = "EnableFTSensor({:d})".format(status)
        return self.sendRecvMsg(string)

    def SixForceHome(self):
        """
        """
        string = "SixForceHome()"
        return self.sendRecvMsg(string)

    def GetForce(self, tool=-1):
        """
        """
        if tool == -1:
            string = "GetForce()"
        else:
            string = "GetForce({:d})".format(tool)
        return self.sendRecvMsg(string)

    def ForceDriveMode(self, x, y, z, rx, ry, rz, user=-1):
        """
        {x,y,z,rx,ry,rz} string
        """
        string = ""
        string = (
            "ForceDriveMode("
            + "{"
            + "{:d},{:d},{:d},{:d},{:d},{:d}".format(x, y, z, rx, ry, rz)
            + "}"
        )
        if user != -1:
            string = string + ",{:d}".format(user)
        string = string + ")"
        return self.sendRecvMsg(string)

    def ForceDriveSpeed(self, speed):
        """
        """
        string = "ForceDriveSpeed({:d})".format(speed)
        return self.sendRecvMsg(string)

    def FCForceMode(
        self,
        x,
        y,
        z,
        rx,
        ry,
        rz,
        fx,
        fy,
        fz,
        frx,
        fry,
        frz,
        reference=-1,
        user=-1,
        tool=-1,
    ):
        """
        {x,y,z,rx,ry,rz}
        {fx,fy,fz,frx,fry,frz}
        reference
        user
        tool
        """
        string = ""
        string = (
            "FCForceMode("
            + "{"
            + "{:d},{:d},{:d},{:d},{:d},{:d}".format(x, y, z, rx, ry, rz)
            + "},"
            + "{"
            + "{:d},{:d},{:d},{:d},{:d},{:d}".format(fx, fy, fz, frx, fry, frz)
            + "}"
        )
        params = []
        if reference != -1:
            params.append("reference={:d}".format(reference))
        if user != -1:
            params.append("user={:d}".format(user))
        if tool != -1:
            params.append("tool={:d}".format(tool))
        for ii in params:
            string = string + "," + ii
        string = string + ")"
        return self.sendRecvMsg(string)

    def FCSetDeviation(self, x, y, z, rx, ry, rz, controltype=-1):
        """
        x、y、z
        rx、ry、rz
        controltype
        """
        string = ""
        string = (
            "FCSetDeviation("
            + "{"
            + "{:d},{:d},{:d},{:d},{:d},{:d}".format(x, y, z, rx, ry, rz)
            + "}"
        )
        if controltype != -1:
            string = string + ",{:d}".format(controltype)
        string = string + ")"
        return self.sendRecvMsg(string)

    def FCSetForceLimit(self, x, y, z, rx, ry, rz):
        """
        """
        string = ""
        string = "FCSetForceLimit(" + "{:d},{:d},{:d},{:d},{:d},{:d}".format(
            x, y, z, rx, ry, rz
        )
        string = string + ")"
        return self.sendRecvMsg(string)

    def FCSetMass(self, x, y, z, rx, ry, rz):
        """
        """
        string = ""
        string = "FCSetMass(" + "{:d},{:d},{:d},{:d},{:d},{:d}".format(
            x, y, z, rx, ry, rz
        )
        string = string + ")"
        return self.sendRecvMsg(string)

    def FCSetStiffness(self, x, y, z, rx, ry, rz):
        """
        """
        string = ""
        string = "FCSetStiffness(" + "{:d},{:d},{:d},{:d},{:d},{:d}".format(
            x, y, z, rx, ry, rz
        )
        string = string + ")"
        return self.sendRecvMsg(string)

    def FCSetDamping(self, x, y, z, rx, ry, rz):
        """
        """
        string = ""
        string = "FCSetDamping(" + "{:d},{:d},{:d},{:d},{:d},{:d}".format(
            x, y, z, rx, ry, rz
        )
        string = string + ")"
        return self.sendRecvMsg(string)

    def FCOff(self):
        """
        """
        string = "FCOff()"
        return self.sendRecvMsg(string)

    def FCSetForceSpeedLimit(self, x, y, z, rx, ry, rz):
        """
        """
        string = ""
        string = "FCSetForceSpeedLimit(" + "{:d},{:d},{:d},{:d},{:d},{:d}".format(
            x, y, z, rx, ry, rz
        )
        string = string + ")"
        return self.sendRecvMsg(string)

    def FCSetForce(self, x, y, z, rx, ry, rz):
        """
        """
        string = ""
        string = "FCSetForce(" + "{:d},{:d},{:d},{:d},{:d},{:d}".format(
            x, y, z, rx, ry, rz
        )
        string = string + ")"
        return self.sendRecvMsg(string)

    def RequestControl(self):
        """
        Request control of the robot.
        Note: This function sends a request for the control of the robot, which may be approved or denied.
        """
        string = "RequestControl()"
        return self.sendRecvMsg(string)


    def RelPointTool(self, coordinateMode, a1, b1, c1, d1, e1, f1, x, y, z, rx, ry, rz):
        """
        """
        string = ""
        if coordinateMode == 0:
            string = "RelPointTool(pose={{{:f},{:f},{:f},{:f},{:f},{:f}}},".format(
                a1, b1, c1, d1, e1, f1
            )
        elif coordinateMode == 1:
            string = "RelPointTool(joint={{{:f},{:f},{:f},{:f},{:f},{:f}}},".format(
                a1, b1, c1, d1, e1, f1
            )
        string = (
            string
            + "{"
            + "{:f},{:f},{:f},{:f},{:f},{:f}".format(x, y, z, rx, ry, rz)
            + "}"
        )
        string = string + ")"
        return self.sendRecvMsg(string)

    def RelPointUser(self, coordinateMode, a1, b1, c1, d1, e1, f1, x, y, z, rx, ry, rz):
        """
        """
        string = ""
        string = ""
        if coordinateMode == 0:
            string = "RelPointUser(pose={{{:f},{:f},{:f},{:f},{:f},{:f}}},".format(
                a1, b1, c1, d1, e1, f1
            )
        elif coordinateMode == 1:
            string = "RelPointUser(joint={{{:f},{:f},{:f},{:f},{:f},{:f}}},".format(
                a1, b1, c1, d1, e1, f1
            )
        string = (
            string
            + "{"
            + "{:f},{:f},{:f},{:f},{:f},{:f}".format(x, y, z, rx, ry, rz)
            + "}"
        )
        string = string + ")"
        return self.sendRecvMsg(string)

    def RelJoint(
        self,
        j1,
        j2,
        j3,
        j4,
        j5,
        j6,
        offset1,
        offset2,
        offset3,
        offset4,
        offset5,
        offset6,
    ):
        """
        RelJoint command
        """
        string = "RelJoint({:f},{:f},{:f},{:f},{:f},{:f},{{{:f},{:f},{:f},{:f},{:f},{:f}}})".format(
            j1, j2, j3, j4, j5, j6, offset1, offset2, offset3, offset4, offset5, offset6
        )
        return self.sendRecvMsg(string)

    def ArcIO(
        self,
        a1,
        b1,
        c1,
        d1,
        e1,
        f1,
        a2,
        b2,
        c2,
        d2,
        e2,
        f2,
        coordinateMode,
        *io_params,
        user=-1,
        tool=-1,
        a=-1,
        v=-1,
        speed=-1,
        cp=-1,
        r=-1,
        mode=-1,
    ):
        """
        """
        string = ""
        if coordinateMode == 0:
            string = "ArcIO(pose={{{:f},{:f},{:f},{:f},{:f},{:f}}},pose={{{:f},{:f},{:f},{:f},{:f},{:f}}}".format(
                a1, b1, c1, d1, e1, f1, a2, b2, c2, d2, e2, f2
            )
        elif coordinateMode == 1:
            string = "ArcIO(joint={{{:f},{:f},{:f},{:f},{:f},{:f}}},joint={{{:f},{:f},{:f},{:f},{:f},{:f}}}".format(
                a1, b1, c1, d1, e1, f1, a2, b2, c2, d2, e2, f2
            )
        else:
            print("coordinateMode  param  is wrong")
            return ""

        for io_param in io_params:
            if isinstance(io_param, (list, tuple)) and len(io_param) == 4:
                string += ",{{{:d},{:d},{:d},{:d}}}".format(*io_param)
            else:
                print("io_param format is wrong")

        params = []
        if user != -1:
            params.append("user={:d}".format(user))
        if tool != -1:
            params.append("tool={:d}".format(tool))
        if a != -1:
            params.append("a={:d}".format(a))
        if v != -1 and speed != -1:
            params.append("speed={:d}".format(speed))
        elif speed != -1:
            params.append("speed={:d}".format(speed))
        elif v != -1:
            params.append("v={:d}".format(v))
        if cp != -1 and r != -1:
            params.append("r={:d}".format(r))
        elif r != -1:
            params.append("r={:d}".format(r))
        elif cp != -1:
            params.append("cp={:d}".format(cp))
        if mode != -1:
            params.append("mode={:d}".format(mode))

        for ii in params:
            string += "," + ii
        string += ")"
        return self.sendRecvMsg(string)

    def ArcTrackStart(self):
        return self.sendRecvMsg("ArcTrackStart()")

    def ArcTrackParams(
        self,
        sampleTime,
        coordinateType,
        upDownCompensationMin,
        upDownCompensationMax,
        upDownCompensationOffset,
        leftRightCompensationMin,
        leftRightCompensationMax,
        leftRightCompensationOffset,
    ):
        string = "ArcTrackParams({:d},{:d},{:f},{:f},{:f},{:f},{:f},{:f})".format(
            sampleTime,
            coordinateType,
            upDownCompensationMin,
            upDownCompensationMax,
            upDownCompensationOffset,
            leftRightCompensationMin,
            leftRightCompensationMax,
            leftRightCompensationOffset,
        )
        return self.sendRecvMsg(string)

    def ArcTrackEnd(self):
        return self.sendRecvMsg("ArcTrackEnd()")

    def CheckMovC(
        self,
        j1a,
        j2a,
        j3a,
        j4a,
        j5a,
        j6a,
        j1b,
        j2b,
        j3b,
        j4b,
        j5b,
        j6b,
        j1c,
        j2c,
        j3c,
        j4c,
        j5c,
        j6c,
        user=-1,
        tool=-1,
        a=-1,
        v=-1,
        cp=-1,
    ):
        string = "CheckMovC(joint={{{:f},{:f},{:f},{:f},{:f},{:f}}},joint={{{:f},{:f},{:f},{:f},{:f},{:f}}},joint={{{:f},{:f},{:f},{:f},{:f},{:f}}}".format(
            j1a,
            j2a,
            j3a,
            j4a,
            j5a,
            j6a,
            j1b,
            j2b,
            j3b,
            j4b,
            j5b,
            j6b,
            j1c,
            j2c,
            j3c,
            j4c,
            j5c,
            j6c,
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
        if params:
            string += "," + ",".join(params)
        string += ")"
        return self.sendRecvMsg(string)

    def CheckMovJ(
        self,
        j1a,
        j2a,
        j3a,
        j4a,
        j5a,
        j6a,
        j1b,
        j2b,
        j3b,
        j4b,
        j5b,
        j6b,
        user=-1,
        tool=-1,
        a=-1,
        v=-1,
        cp=-1,
    ):
        string = "CheckMovJ(joint={{{:f},{:f},{:f},{:f},{:f},{:f}}},joint={{{:f},{:f},{:f},{:f},{:f},{:f}}}".format(
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
        if params:
            string += "," + ",".join(params)
        string += ")"
        return self.sendRecvMsg(string)

    def CheckOddMovC(
        self,
        j1a,
        j2a,
        j3a,
        j4a,
        j5a,
        j6a,
        j1b,
        j2b,
        j3b,
        j4b,
        j5b,
        j6b,
        j1c,
        j2c,
        j3c,
        j4c,
        j5c,
        j6c,
        user=-1,
        tool=-1,
        a=-1,
        v=-1,
        cp=-1,
    ):
        string = "CheckOddMovC(joint={{{:f},{:f},{:f},{:f},{:f},{:f}}},joint={{{:f},{:f},{:f},{:f},{:f},{:f}}},joint={{{:f},{:f},{:f},{:f},{:f},{:f}}}".format(
            j1a,
            j2a,
            j3a,
            j4a,
            j5a,
            j6a,
            j1b,
            j2b,
            j3b,
            j4b,
            j5b,
            j6b,
            j1c,
            j2c,
            j3c,
            j4c,
            j5c,
            j6c,
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
        if params:
            string += "," + ",".join(params)
        string += ")"
        return self.sendRecvMsg(string)

    def CheckOddMovJ(
        self,
        j1a,
        j2a,
        j3a,
        j4a,
        j5a,
        j6a,
        j1b,
        j2b,
        j3b,
        j4b,
        j5b,
        j6b,
        user=-1,
        tool=-1,
        a=-1,
        v=-1,
        cp=-1,
    ):
        string = "CheckOddMovJ(joint={{{:f},{:f},{:f},{:f},{:f},{:f}}},joint={{{:f},{:f},{:f},{:f},{:f},{:f}}}".format(
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
        if params:
            string += "," + ",".join(params)
        string += ")"
        return self.sendRecvMsg(string)

    def CheckOddMovL(
        self,
        j1a,
        j2a,
        j3a,
        j4a,
        j5a,
        j6a,
        j1b,
        j2b,
        j3b,
        j4b,
        j5b,
        j6b,
        user=-1,
        tool=-1,
        a=-1,
        v=-1,
        cp=-1,
    ):
        string = "CheckOddMovL(joint={{{:f},{:f},{:f},{:f},{:f},{:f}}},joint={{{:f},{:f},{:f},{:f},{:f},{:f}}}".format(
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
        if params:
            string += "," + ",".join(params)
        string += ")"
        return self.sendRecvMsg(string)

    def CnvInit(self, index):
        """
        CnvInit command
        """
        string = "CnvInit({:d})".format(index)
        return self.sendRecvMsg(string)

    def CnvMovL(
        self, j1, j2, j3, j4, j5, j6, user=-1, tool=-1, a=-1, v=-1, cp=-1, r=-1
    ):
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
        return self.sendRecvMsg(string)

    def CnvMovC(
        self,
        j1a,
        j2a,
        j3a,
        j4a,
        j5a,
        j6a,
        j1b,
        j2b,
        j3b,
        j4b,
        j5b,
        j6b,
        user=-1,
        tool=-1,
        a=-1,
        v=-1,
        cp=-1,
        r=-1,
        mode=1,
    ):
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
        return self.sendRecvMsg(string)

    def CreateTray(self, *args, **kwargs):
        """
        CreateTray command
        Due to missing documentation on exact parameters, this function uses dynamic arguments.
        Example: CreateTray(rows=3, cols=4, ...)
        """
        return self.sendRecvMsg(self._build_cmd("CreateTray", *args, **kwargs))

    def EndRTOffset(self):
        return self.sendRecvMsg("EndRTOffset()")

    def StartRTOffset(self):
        """
        StartRTOffset command
        """
        return self.sendRecvMsg("StartRTOffset()")

    def FCCollisionSwitch(self, enable):
        return self.sendRecvMsg("FCCollisionSwitch(enable={:d})".format(enable))

    def SetFCCollision(self, force, torque):
        return self.sendRecvMsg("SetFCCollision({:f},{:f})".format(force, torque))

    def GetCnvObject(self, objId):
        return self.sendRecvMsg("GetCnvObject({:d})".format(objId))

    def DOGroupDEC(self, group, value):
        return self.sendRecvMsg("DOGroupDEC({:d},{:d})".format(group, value))

    def GetDOGroupDEC(self, group, value):
        return self.sendRecvMsg("GetDOGroupDEC({:d},{:d})".format(group, value))

    def DIGroupDEC(self, group, value):
        return self.sendRecvMsg("DIGroupDEC({:d},{:d})".format(group, value))

    def InverseSolution(self, a1, b1, c1, d1, e1, f1, user=-1, tool=-1, isJoint=0):
        """
        InverseSolution command
        """
        string = "InverseSolution(pose={{{:f},{:f},{:f},{:f},{:f},{:f}}}".format(
            a1, b1, c1, d1, e1, f1
        )

        params = []
        if user != -1:
            params.append("user={:d}".format(user))
        if tool != -1:
            params.append("tool={:d}".format(tool))
        if isJoint != 0:
            params.append("isJoint={:d}".format(isJoint))

        for ii in params:
            string += "," + ii
        string += ")"
        return self.sendRecvMsg(string)

    def MoveL(
        self,
        a1,
        b1,
        c1,
        d1,
        e1,
        f1,
        user=-1,
        tool=-1,
        a=-1,
        v=-1,
        speed=-1,
        cp=-1,
        r=-1,
    ):
        """
        MoveL command
        """
        string = "MoveL(pose={{{:f},{:f},{:f},{:f},{:f},{:f}}}".format(
            a1, b1, c1, d1, e1, f1
        )

        params = []
        if user != -1:
            params.append("user={:d}".format(user))
        if tool != -1:
            params.append("tool={:d}".format(tool))
        if a != -1:
            params.append("a={:d}".format(a))
        if v != -1 and speed != -1:
            params.append("speed={:d}".format(speed))
        elif speed != -1:
            params.append("speed={:d}".format(speed))
        elif v != -1:
            params.append("v={:d}".format(v))
        if cp != -1 and r != -1:
            params.append("r={:d}".format(r))
        elif r != -1:
            params.append("r={:d}".format(r))
        elif cp != -1:
            params.append("cp={:d}".format(cp))

        for ii in params:
            string += "," + ii
        string += ")"
        return self.sendRecvMsg(string)

    def MovS(
        self,
        file=None,
        coordinateMode=-1,
        points=None,
        user=-1,
        tool=-1,
        v=-1,
        speed=-1,
        a=-1,
        freq=-1,
    ):
        """
        MovS command
        """
        string = "MovS("
        if file is not None:
            string += "file={:s}".format(file)
        elif points is not None and coordinateMode != -1:
            # points should be a list of tuples/lists
            pts_str = []
            for pt in points:
                if coordinateMode == 0:
                    pts_str.append("pose={{{:f},{:f},{:f},{:f},{:f},{:f}}}".format(*pt))
                elif coordinateMode == 1:
                    pts_str.append(
                        "joint={{{:f},{:f},{:f},{:f},{:f},{:f}}}".format(*pt)
                    )
            string += ",".join(pts_str)
        else:
            print("MovS param is wrong")
            return ""

        params = []
        if user != -1:
            params.append("user={:d}".format(user))
        if tool != -1:
            params.append("tool={:d}".format(tool))
        if v != -1 and speed != -1:
            params.append("speed={:d}".format(speed))
        elif speed != -1:
            params.append("speed={:d}".format(speed))
        elif v != -1:
            params.append("v={:d}".format(v))
        if a != -1:
            params.append("a={:d}".format(a))
        if freq != -1:
            params.append("freq={:d}".format(freq))

        if len(params) > 0:
            if file is not None or (points is not None and len(points) > 0):
                string += ","
            string += ",".join(params)

        string += ")"
        return self.sendRecvMsg(string)

    def OffsetPara(self, x, y, z, rx, ry, rz):
        """
        OffsetPara command
        """
        string = "OffsetPara({:f},{:f},{:f},{:f},{:f},{:f})".format(x, y, z, rx, ry, rz)
        return self.sendRecvMsg(string)

    def GetTrayPoint(self, *args, **kwargs):
        """
        GetTrayPoint command
        Due to missing documentation on exact parameters, this function uses dynamic arguments.
        Example: GetTrayPoint(trayName)
        """
        return self.sendRecvMsg(self._build_cmd("GetTrayPoint", *args, **kwargs))

    def ResetRobot(self):
        return self.sendRecvMsg("ResetRobot()")

    def RunTo(self, a1, b1, c1, d1, e1, f1, moveType, user=-1, tool=-1, a=-1, v=-1):
        """
        RunTo command
        """
        string = ""
        if moveType == 0:
            string = "RunTo(pose={{{:f},{:f},{:f},{:f},{:f},{:f}}},moveType=0".format(
                a1, b1, c1, d1, e1, f1
            )
        elif moveType == 1:
            string = "RunTo(joint={{{:f},{:f},{:f},{:f},{:f},{:f}}},moveType=1".format(
                a1, b1, c1, d1, e1, f1
            )
        else:
            print("moveType param is wrong")
            return ""

        params = []
        if user != -1:
            params.append("user={:d}".format(user))
        if tool != -1:
            params.append("tool={:d}".format(tool))
        if a != -1:
            params.append("a={:d}".format(a))
        if v != -1:
            params.append("v={:d}".format(v))

        for ii in params:
            string += "," + ii
        string += ")"
        return self.sendRecvMsg(string)

    def SetArcTrackOffset(
        self, offsetX, offsetY, offsetZ, offsetRx, offsetRy, offsetRz
    ):
        string = "SetArcTrackOffset({{{:f},{:f},{:f},{:f},{:f},{:f}}})".format(
            offsetX, offsetY, offsetZ, offsetRx, offsetRy, offsetRz
        )
        return self.sendRecvMsg(string)

    def SetCnvPointOffset(self, xOffset, yOffset):
        return self.sendRecvMsg("SetCnvPointOffset({:f},{:f})".format(xOffset, yOffset))

    def SetCnvTimeCompensation(self, time):
        return self.sendRecvMsg("SetCnvTimeCompensation({:d})".format(time))

    def StartSyncCnv(self):
        return self.sendRecvMsg("StartSyncCnv()")

    def StopSyncCnv(self):
        return self.sendRecvMsg("StopSyncCnv()")

    def TcpSendAndParse(self, cmd):
        """
        TcpSendAndParse command
        """
        return self.sendRecvMsg('TcpSendAndParse("{:s}")'.format(cmd))

    def Sleep(self, count):
        return self.sendRecvMsg("Sleep({:d})".format(count))

    def RelPointWeldLine(self, StartX, EndX, Y, Z, WorkAngle, TravelAngle, P1, P2):
        string = "RelPointWeldLine({:f},{:f},{:f},{:f},{:f},{:f},{{{:f},{:f},{:f},{:f},{:f},{:f}}},{{{:f},{:f},{:f},{:f},{:f},{:f}}})".format(
            StartX,
            EndX,
            Y,
            Z,
            WorkAngle,
            TravelAngle,
            P1[0],
            P1[1],
            P1[2],
            P1[3],
            P1[4],
            P1[5],
            P2[0],
            P2[1],
            P2[2],
            P2[3],
            P2[4],
            P2[5],
        )
        return self.sendRecvMsg(string)

    def RelPointWeldArc(self, StartX, EndX, Y, Z, WorkAngle, TravelAngle, P1, P2, P3):
        string = "RelPointWeldArc({:f},{:f},{:f},{:f},{:f},{:f},{{{:f},{:f},{:f},{:f},{:f},{:f}}},{{{:f},{:f},{:f},{:f},{:f},{:f}}},{{{:f},{:f},{:f},{:f},{:f},{:f}}})".format(
            StartX,
            EndX,
            Y,
            Z,
            WorkAngle,
            TravelAngle,
            P1[0],
            P1[1],
            P1[2],
            P1[3],
            P1[4],
            P1[5],
            P2[0],
            P2[1],
            P2[2],
            P2[3],
            P2[4],
            P2[5],
            P3[0],
            P3[1],
            P3[2],
            P3[3],
            P3[4],
            P3[5],
        )
        return self.sendRecvMsg(string)

    def WeaveStart(self):
        return self.sendRecvMsg("WeaveStart()")

    def WeaveParams(
        self,
        weldType,
        frequency,
        leftAmplitude,
        rightAmplitude,
        direction,
        stopMode,
        stopTime1,
        stopTime2,
        stopTime3,
        stopTime4,
        radius,
        radian,
        **kwargs,
    ):
        string = "WeaveParams({:d},{:f},{:f},{:f},{:d},{:d},{:d},{:d},{:d},{:d},{:f},{:f}".format(
            weldType,
            frequency,
            leftAmplitude,
            rightAmplitude,
            direction,
            stopMode,
            stopTime1,
            stopTime2,
            stopTime3,
            stopTime4,
            radius,
            radian,
        )
        if kwargs:
            for key, value in kwargs.items():
                string += ",{}={}".format(key, value)
        string += ")"
        return self.sendRecvMsg(string)

    def WeaveEnd(self):
        return self.sendRecvMsg("WeaveEnd()")

    def WeldArcSpeedStart(self):
        return self.sendRecvMsg("WeldArcSpeedStart()")

    def WeldArcSpeed(self, speed):
        return self.sendRecvMsg("WeldArcSpeed({:f})".format(speed))

    def WeldArcSpeedEnd(self):
        return self.sendRecvMsg("WeldArcSpeedEnd()")

    def WeldWeaveStart(
        self,
        weldType,
        frequency,
        leftAmplitude,
        rightAmplitude,
        direction,
        stopMode,
        stopTime1,
        stopTime2,
        stopTime3,
        stopTime4,
        radius,
        radian,
    ):
        string = "WeldWeaveStart({:d},{:f},{:f},{:f},{:d},{:d},{:d},{:d},{:d},{:d},{:f},{:f})".format(
            weldType,
            frequency,
            leftAmplitude,
            rightAmplitude,
            direction,
            stopMode,
            stopTime1,
            stopTime2,
            stopTime3,
            stopTime4,
            radius,
            radian,
        )
        return self.sendRecvMsg(string)

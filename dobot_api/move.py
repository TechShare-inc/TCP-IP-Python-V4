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
        描述
        从当前位置以关节运动⽅式运动⾄⽬标点。
        必选参数
        参数名 类型 说明
        P string ⽬标点，⽀持关节变量或位姿变量
        coordinateMode int  目标点的坐标值模式    0为pose方式  1为joint
        可选参数
        参数名 类型 说明
        user int ⽤⼾坐标系
        tool int ⼯具坐标系
        a int 执⾏该条指令时的机械臂运动加速度⽐例。取值范围：(0,100]
        v int 执⾏该条指令时的机械臂运动速度⽐例。取值范围：(0,100]
        cp int 平滑过渡⽐例。取值范围：[0,100]
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
        描述
        从当前位置以直线运动⽅式运动⾄⽬标点。
        必选参数
        参数名 类型 说明
        P string ⽬标点，⽀持关节变量或位姿变量
        coordinateMode int  目标点的坐标值模式    0为pose方式  1为joint
        可选参数
        参数名 类型  说明
        user int ⽤⼾坐标系
        tool int ⼯具坐标系
        a    int 执⾏该条指令时的机械臂运动加速度⽐例。取值范围：(0,100]
        v    int 执⾏该条指令时的机械臂运动速度⽐例，与speed互斥。取值范围：(0,100]
        speed int 执⾏该条指令时的机械臂运动⽬标速度，与v互斥，若同时存在以speed为
        准。取值范围：[1, 最⼤运动速度]，单位：mm/s
        cp  int 平滑过渡⽐例，与r互斥。取值范围：[0,100]
        r   int 平滑过渡半径，与cp互斥，若同时存在以r为准。单位：mm
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
        参数名 类型 含义
        参数范围
        J1 double 点J1 轴位置，单位：度 是
        J2 double 点J2 轴位置，单位：度 是
        J3 double 点J3 轴位置，单位：度 是
        J4 double 点J4 轴位置，单位：度 是
        J5 double 点J5 轴位置，单位：度 是
        J6 double 点J6 轴位置，单位：度 是
        t float 该点位的运行时间，默认0.1,单位：s 否 [0.004,3600.0]
        aheadtime float 作用类似于PID的D项，默认50，标量，无单位 否 [20.0,100.0]
        gain float 目标位置的比例放大器，作用类似于PID的P项，默认500，标量，无单位 否 [200.0,1000.0]
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
        参数名 类型 含义 是否必填 参数范围
        X double X 轴位置，单位：毫米 是
        Y double Y 轴位置，单位：毫米 是
        Z double Z 轴位置，单位：毫米 是
        Rx double Rx 轴位置，单位：度 是
        Ry double Ry 轴位置，单位：度 是
        Rz double Rz 轴位置，单位：度 是
        t float 该点位的运行时间，默认0.1,单位：s 否 [0.004,3600.0]
        aheadtime float 作用类似于PID的D项，默认50，标量，无单位 否 [20.0,100.0]
        gain float 目标位置的比例放大器，作用类似于PID的P项，默认500，标量，无单位 否 [200.0,1000.0]
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
        描述
        从当前位置以直线运动⽅式运动⾄⽬标点，运动时并⾏设置数字输出端⼝状态。
        必选参数
        参数名 类型 说明
        P string ⽬标点，⽀持关节变量或位姿变量
        coordinateMode int  目标点的坐标值模式    0为pose方式  1为joint
        {Mode,Distance,Index,Status}为并⾏数字输出参数，⽤于设置当机械臂运动到指定距离或百分⽐
        时，触发指定DO。可设置多组，参数具体含义如下：
        参数名 类型 说明
        Mode int 触发模式。0表⽰距离百分⽐，1表⽰距离数值
        Distance int 指定距离。
        Distance为正数时，表⽰离起点的距离；
        Distance为负数时，表⽰离⽬标点的距离；
        Mode为0时，Distance表⽰和总距离的百分⽐；取值范围：(0,100]；
        Mode为1时，Distance表⽰距离的值。单位：mm
        Index int DO端⼦的编号
        Status int 要设置的DO状态，0表⽰⽆信号，1表⽰有信号
        可选参数
        参数名  类型  说明
        user int ⽤⼾坐标系
        tool int ⼯具坐标系
        a int 执⾏该条指令时的机械臂运动加速度⽐例。取值范围：(0,100]
        v int 执⾏该条指令时的机械臂运动速度⽐例，与speed互斥。取值范围：(0,100]
        speed int 执⾏该条指令时的机械臂运动⽬标速度，与v互斥，若同时存在以speed为
        准。取值范围：[1, 最⼤运动速度]，单位：mm/s
        cp int 平滑过渡⽐例，与r互斥。取值范围：[0,100]
        r int 平滑过渡半径，与cp互斥，若同时存在以r为准。单位：mm
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
        描述
        从当前位置以关节运动⽅式运动⾄⽬标点，运动时并⾏设置数字输出端⼝状态。
        必选参数
        参数名 类型 说明
        P string ⽬标点，⽀持关节变量或位姿变量
        coordinateMode int  目标点的坐标值模式    0为pose方式  1为joint
        {Mode,Distance,Index,Status}为并⾏数字输出参数，⽤于设置当机械臂运动到指定距离或百分⽐
        时，触发指定DO。可设置多组，参数具体含义如下：
        参数名   类型  说明
        Mode int 触发模式。0表⽰距离百分⽐，1表⽰距离数值。系统会将各关节⻆合成
        ⼀个⻆度向量，并计算终点和起点的⻆度差作为运动的总距离。
        Distance int 指定距离。
        Distance为正数时，表⽰离起点的距离；
        Distance为负数时，表⽰离⽬标点的距离；
        Mode为0时，Distance表⽰和总距离的百分⽐；取值范围：(0,100]；
        Mode为1时，Distance表⽰距离的⻆度。单位：°
        Index int DO端⼦的编号
        Status int 要设置的DO状态，0表⽰⽆信号，1表⽰有信号
        可选参数
        参数名 类型 说明
        user int ⽤⼾坐标系
        tool int ⼯具坐标系
        a int 执⾏该条指令时的机械臂运动加速度⽐例。取值范围：(0,100]
        v int 执⾏该条指令时的机械臂运动速度⽐例。取值范围：(0,100]
        cp int 平滑过渡⽐例。取值范围：[0,100]
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
        描述
        从当前位置以圆弧插补⽅式运动⾄⽬标点。
        需要通过当前位置，圆弧中间点，运动⽬标点三个点确定⼀个圆弧，因此当前位置不能在P1和P2
        确定的直线上。
        必选参数
        参数名 类型 说明
        P1 string 圆弧中间点，⽀持关节变量或位姿变量
        P2 string 运动⽬标点，⽀持关节变量或位姿变量
        coordinateMode int  目标点的坐标值模式    0为pose方式  1为joint
        可选参数
        参数名  类型  说明
        user int ⽤⼾坐标系
        tool int ⼯具坐标系
        a int  执⾏该条指令时的机械臂运动加速度⽐例。取值范围：(0,100]
        v int 执⾏该条指令时的机械臂运动速度⽐例，与speed互斥。取值范围：(0,100]
        speed int执⾏该条指令时的机械臂运动⽬标速度，与v互斥，若同时存在以speed为
        准。取值范围：[1, 最⼤运动速度]，单位：mm/s
        cp int 平滑过渡⽐例，与r互斥。取值范围：[0,100]
        r int 平滑过渡半径，与cp互斥，若同时存在以r为准。单位：mm
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
        描述
        从当前位置进⾏整圆插补运动，运动指定圈数后重新回到当前位置。
        需要通过当前位置，P1，P2三个点确定⼀个整圆，因此当前位置不能在P1和P2确定的直线上，且
        三个点确定的整圆不能超出机械臂的运动范围。
        必选参数
        参数名 类型 说明
        P1 string 整圆中间点，⽀持关节变量或位姿变量
        P2 string 整圆结束点点，⽀持关节变量或位姿变量
        coordinateMode int  目标点的坐标值模式    0为pose方式  1为joint
        count int 进⾏整圆运动的圈数，取值范围：[1,999]。
        可选参数
        参数名  类型  说明
        user int ⽤⼾坐标系
        tool int ⼯具坐标系
        a int 执⾏该条指令时的机械臂运动加速度⽐例。取值范围：(0,100]
        v int 执⾏该条指令时的机械臂运动速度⽐例，与speed互斥。取值范围：(0,100]
        speed int执⾏该条指令时的机械臂运动⽬标速度，与v互斥，若同时存在以speed为
        准。取值范围：[1, 最⼤运动速度]，单位：mm/s
        cp int 平滑过渡⽐例，与r互斥。取值范围：[0,100]
        r int 平滑过渡半径，与cp互斥，若同时存在以r为准。单位：mm
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
        描述
        获取指定轨迹的第⼀个点位。
        必选参数
        参数名 类型 说明
        traceName string  轨迹⽂件名（含后缀）
        轨迹⽂件存放在/dobot/userdata/project/process/trajectory/
        如果名称包含中⽂，必须将发送端的编码⽅式设置为UTF-8，否则
        会导致中⽂接收异常
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
        描述
        根据指定的轨迹⽂件中的记录点位进⾏运动，复现录制的运动轨迹。
        下发轨迹复现指令成功后，⽤⼾可以通过RobotMode指令查询机械臂运⾏状态，
        ROBOT_MODE_RUNNING表⽰机器⼈在轨迹复现运⾏中，变成ROBOT_MODE_IDLE表⽰轨迹复现
        运⾏完成，ROBOT_MODE_ERROR表⽰报警。
        必选参数
        参数名 类型 说明
        traceName string
        轨迹⽂件名（含后缀）轨迹⽂件存放在/dobot/userdata/project/process/trajectory/
        如果名称包含中⽂，必须将发送端的编码⽅式设置为UTF-8，否则会导致中⽂接收异常
        可选参数
        参数名 类型 说明
        isConst int是否匀速复现。
           1表⽰匀速复现，机械臂会按照全局速率匀速复现轨迹；
           0表⽰按照轨迹录制时的原速复现，并可以使⽤multi参数等⽐缩放运
           动速度，此时机械臂的运动速度不受全局速率的影响。
        multi double 复现时的速度倍数，仅当isConst=0时有效；取值范围：[0.25, 2]，默认值为1
        user int  指定轨迹点位对应的⽤⼾坐标系索引，不指定时使⽤轨迹⽂件中记录的⽤⼾坐标系索引
        tool int 指定轨迹点位对应的⼯具坐标系索引，不指定时使⽤轨迹⽂件中记录的⼯具坐标系索引
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
        描述
        沿⼯具坐标系进⾏相对运动，末端运动⽅式为关节运动。
        必选参数
        参数名 类型 说明
        offsetX double X轴⽅向偏移量，单位：mm
        offsetY double Y轴⽅向偏移量，单位：mm
        offsetZ double Z轴⽅向偏移量，单位：mm
        offsetRx double Rx轴⽅向偏移量，单位：度
        offsetRy double Ry轴⽅向偏移量，单位：度
        offsetRz double Rz轴⽅向偏移量，单位：度
        可选参数
        参数名 类型 说明
        user int ⽤⼾坐标系
        tool int ⼯具坐标系
        a int 执⾏该条指令时的机械臂运动加速度⽐例。取值范围：(0,100]
        v int 执⾏该条指令时的机械臂运动速度⽐例。取值范围：(0,100]
        cp int 平滑过渡⽐例。取值范围：[0,100]
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
        描述
        沿⼯具坐标系进⾏相对运动，末端运动⽅式为直线运动。
        此条指令为六轴机械臂特有。
        必选参数
        参数名 类型 说明
        offsetX double X轴⽅向偏移量，单位：mm
        offsetY double Y轴⽅向偏移量，单位：mm
        offsetZ double Z轴⽅向偏移量，单位：mm
        offsetRx double Rx轴⽅向偏移量，单位：度
        offsetRy double Ry轴⽅向偏移量，单位：度
        offsetRz double Rz轴⽅向偏移量，单位：度
        可选参数
        参数名  类型  说明
        user int ⽤⼾坐标系
        tool int ⼯具坐标系
        a int 执⾏该条指令时的机械臂运动加速度⽐例。取值范围：(0,100]
        v int 执⾏该条指令时的机械臂运动速度⽐例。取值范围：(0,100]
        speed int  执⾏该条指令时的机械臂运动⽬标速度，与v互斥，若同时存在以speed为
        准。取值范围：[1, 最⼤运动速度]，单位：mm/s
        cp int 平滑过渡⽐例，与r互斥。取值范围：[0,100]
        r int 平滑过渡半径，与cp互斥，若同时存在以r为准。单位：mm
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
        描述
        沿⽤⼾坐标系进⾏相对运动，末端运动⽅式为关节运动。
        必选参数
        参数名 类型 说明
        offsetX double X轴⽅向偏移量，单位：mm
        offsetY double Y轴⽅向偏移量，单位：mm
        offsetZ double Z轴⽅向偏移量，单位：mm
        offsetRx double Rx轴偏移量，单位：度
        offsetRy double Ry轴偏移量，单位：度
        offsetRz double Rz轴偏移量，单位：度
        可选参数
        参数名 类型 说明
        user int ⽤⼾坐标系
        tool int ⼯具坐标系
        a int 执⾏该条指令时的机械臂运动加速度⽐例。取值范围：(0,100]
        v int 执⾏该条指令时的机械臂运动速度⽐例。取值范围：(0,100]
        cp int 平滑过渡⽐例。取值范围：[0,100]
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
        描述
        沿⽤⼾坐标系进⾏相对运动，末端运动⽅式为直线运动。
        必选参数
        参数名 类型 说明
        offsetX double X轴⽅向偏移量，单位：mm
        offsetY double Y轴⽅向偏移量，单位：mm
        offsetZ double Z轴⽅向偏移量，单位：mm
        offsetRx double Rx轴偏移量，单位：度
        offsetRy double Ry轴偏移量，单位：度
        offsetRz double Rz轴偏移量，单位：度
        可选参数
        参数名  类型说明
        user int ⽤⼾坐标系
        tool int ⼯具坐标系
        a int 执⾏该条指令时的机械臂运动加速度⽐例。取值范围：(0,100]
        v int 执⾏该条指令时的机械臂运动速度⽐例。取值范围：(0,100]
        speed int 执⾏该条指令时的机械臂运动⽬标速度，与v互斥，若同时存在以speed为
        准。取值范围：[1, 最⼤运动速度]，单位：mm/s
        cp int 平滑过渡⽐例，与r互斥。取值范围：[0,100]
        r int 平滑过渡半径，与cp互斥，若同时存在以r为准。单位：mm
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
        描述
        沿关节坐标系进⾏相对运动，末端运动⽅式为关节运动。
        必选参数
        参数名 类型 说明
        offset1 double J1轴偏移量，单位：度
        offset2 double J2轴偏移量，单位：度
        offset3 double J3轴偏移量，单位：度
        offset4 double J4轴偏移量，单位：度
        offset5 double J5轴偏移量，单位：度
        offset6 double J6轴偏移量，单位：度
        可选参数
        参数名 类型 说明
        a int 执⾏该条指令时的机械臂运动加速度⽐例。取值范围：(0,100]
        v int 执⾏该条指令时的机械臂运动速度⽐例。取值范围：(0,100]
        cp int 平滑过渡⽐例。取值范围：[0,100]
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
        获取当前执⾏指令的算法队列ID，可以⽤于判断当前机器⼈执⾏到了哪⼀条指令。
        Get the algorithm queue ID of the currently executed command, which can be used to judge which command is currently being executed by the robot.
        """
        string = "GetCurrentCommandID()"
        return self.sendRecvMsg(string)

    ###################################460新增#############################

    ##轨迹恢复指令
    def SetResumeOffset(self, distance):
        """
        该指令仅用于焊接工艺。设置轨迹恢复的目标点位相对暂停时的点位沿焊缝回退的距离
        """
        string = "SetResumeOffset({:f})".format(distance)
        return self.sendRecvMsg(string)

    def PathRecovery(self):
        """
        开始轨迹恢复：工程暂停后，控制机器人回到暂停时的位姿。
        """
        string = "PathRecovery()"
        return self.sendRecvMsg(string)

    def PathRecoveryStop(self):
        """
        轨迹恢复的过程中停止机器人。
        """
        string = "PathRecoveryStop()"
        return self.sendRecvMsg(string)

    def PathRecoveryStatus(self):
        """
        查询轨迹恢复的状态。
        """
        string = "PathRecoveryStatus()"
        return self.sendRecvMsg(string)

    ##日志导出指令
    def LogExportUSB(self, range):
        """
        将机器人日志导出至插在机器人控制柜USB接口的U盘根目录。
        导出范围。
         0   导出logs/all 和logs/user文件夹的内容。
         1   导出logs文件夹所有内容。
        """
        string = "LogExportUSB({:d})".format(range)
        return self.sendRecvMsg(string)

    def GetExportStatus(self):
        """
        获取日志导出的状态。
        其中status表示日志导出状态。
        0：未开始导出
        1：导出中
        2：导出完成
        3：导出失败，找不到U盘
        4：导出失败，U盘空间不足
        5：导出失败，导出过程中U盘被拔出
        导出完成和导出失败的状态会保持到下次用户使用导出功能
        """
        string = "GetExportStatus()"
        return self.sendRecvMsg(string)

    ##力控指令
    def EnableFTSensor(self, status):
        """
        开启/关闭力传感器。
        """
        string = "EnableFTSensor({:d})".format(status)
        return self.sendRecvMsg(string)

    def SixForceHome(self):
        """
        将力传感器当前数值置0，即以传感器当前受力状态作为零点。
        """
        string = "SixForceHome()"
        return self.sendRecvMsg(string)

    def GetForce(self, tool=-1):
        """
        获取力传感器当前数值。
        tool int 用于指定获取数值时参考的工具坐标系，取值范围：[0,50]。
        不指定时使用全局工具坐标系
        """
        if tool == -1:
            string = "GetForce()"
        else:
            string = "GetForce({:d})".format(tool)
        return self.sendRecvMsg(string)

    def ForceDriveMode(self, x, y, z, rx, ry, rz, user=-1):
        """
        指定可拖拽的方向并进入力控拖拽模式。
        {x,y,z,rx,ry,rz} string
        用于指定可拖拽的方向。
        0代表该方向不能拖拽，1代表该方向可以拖拽。
        例：
        {1,1,1,1,1,1}表示机械臂可在各轴方向上自由拖动
        {1,1,1,0,0,0}表示机械臂仅可在XYZ轴方向上拖动
        {0,0,0,1,1,1}表示机械臂仅可在RxRyRz轴方向上旋转
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
        设置力控拖拽速度比例。
        speed int 力控拖拽速度比例，取值范围：[1,100]。
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
        以用户指定的配置参数开启力控。
        {x,y,z,rx,ry,rz}
            开启/关闭笛卡尔空间某个方向的力控调节。
            0表示关闭该方向的力控。
            1表示开启该方向的力控。
        {fx,fy,fz,frx,fry,frz}
            目标力：是工具末端与作用对象之间接触力的目标值，是一种模拟力，可以由用户自行设定；目标力方向分别对应笛卡尔空间的{x,y,z,rx,ry,rz}方向。
            位移方向的目标力范围[-200,200]，单位N；姿态方向的目标力范围[-12,12]，单位N/m。
            目标力为0时处于柔顺模式，柔顺模式与力控拖动类似。
        如果某个方向未开启力控调节，则该方向的目标力也不会生效。
        reference
            格式为"reference=value"。value表示参考坐标系，默认参考工具坐标系。
            reference=0表示参考工具坐标系，即沿工具坐标系进行力控调节。
            reference=1表示参考用户坐标系，即沿用户坐标系进行力控调节。
        user
            格式为"user=index"，index为已标定的用户坐标系索引。取值范围：[0,50]。
        tool
            格式为"tool=index"，index为已标定的工具坐标系索引。取值范围：[0,50]。
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
        设置力控模式下的位移和姿态偏差，若力控过程中恒力偏移了较大的距离，机器人进会行相应处理。
        x、y、z
        代表力控模式下的位移偏差，单位为mm。取值范围：(0,1000]，默认值100mm。
        rx、ry、rz
        代表力控模式下的姿态偏差，单位为度。取值范围：(0,360]，默认值36度。
        controltype
        表示力控过程中超过规定阈值时，机械臂的处理方式。
        0：超过阈值时，机械臂报警（默认值）。
        1：超过阈值时，机械臂停止搜寻而在原有轨迹上继续运动。
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
        设置各方向的最大力限制（该设置对所有方向均生效，包含未启用力控的方向）。
        """
        string = ""
        string = "FCSetForceLimit(" + "{:d},{:d},{:d},{:d},{:d},{:d}".format(
            x, y, z, rx, ry, rz
        )
        string = string + ")"
        return self.sendRecvMsg(string)

    def FCSetMass(self, x, y, z, rx, ry, rz):
        """
        设置力控模式下各方向的惯性系数。
        """
        string = ""
        string = "FCSetMass(" + "{:d},{:d},{:d},{:d},{:d},{:d}".format(
            x, y, z, rx, ry, rz
        )
        string = string + ")"
        return self.sendRecvMsg(string)

    def FCSetStiffness(self, x, y, z, rx, ry, rz):
        """
        设置力控模式下各方向的弹性系数。
        """
        string = ""
        string = "FCSetStiffness(" + "{:d},{:d},{:d},{:d},{:d},{:d}".format(
            x, y, z, rx, ry, rz
        )
        string = string + ")"
        return self.sendRecvMsg(string)

    def FCSetDamping(self, x, y, z, rx, ry, rz):
        """
        设置力控模式下各方向的阻尼系数。
        """
        string = ""
        string = "FCSetDamping(" + "{:d},{:d},{:d},{:d},{:d},{:d}".format(
            x, y, z, rx, ry, rz
        )
        string = string + ")"
        return self.sendRecvMsg(string)

    def FCOff(self):
        """
        退出力控模式，与FCForceMode配合使用，两者之间的运动指令都会进行力的柔顺控制。
        """
        string = "FCOff()"
        return self.sendRecvMsg(string)

    def FCSetForceSpeedLimit(self, x, y, z, rx, ry, rz):
        """
        设置各方向的力控调节速度。力控速度上限较小时，力控调节速度较慢，适合低速平缓的接触面。
        力控速度上限较大时，力控调节速度快，适合高速力控应用。需要根据具体的应用场景进行调整。
        """
        string = ""
        string = "FCSetForceSpeedLimit(" + "{:d},{:d},{:d},{:d},{:d},{:d}".format(
            x, y, z, rx, ry, rz
        )
        string = string + ")"
        return self.sendRecvMsg(string)

    def FCSetForce(self, x, y, z, rx, ry, rz):
        """
        实时调整各方向的恒力设置。
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

    ## 新增运动指令

    def RelPointTool(self, coordinateMode, a1, b1, c1, d1, e1, f1, x, y, z, rx, ry, rz):
        """
        沿工具坐标系笛卡尔点偏移。
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
        沿用户坐标系笛卡尔点偏移。
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
        圆弧运动过程中并行设置数字输出端口的状态，可设置多组。
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

"""
Dashboard and Control Commands Module

This module contains the DobotApiDashboard class which provides dashboard/control
commands for the Dobot robot, including:
- Robot enable/disable and power control
- Error handling and emergency stop
- Speed and acceleration configuration
- Coordinate system management (User, Tool)
- Payload settings
- Collision detection configuration
- Drag mode control
- Safety features (SafeSkin, safety walls, interference areas)
- IO operations (DI, DO, AI, AO)
- Modbus communication
- Register operations
- Robot status queries

Movement commands (MovJ, MovL, ServoJ, etc.) are in the move module.
"""

from .base import DobotApi


class DobotApiDashboard(DobotApi):

    def __init__(self, ip: str, port: int, *args) -> None:
        super().__init__(ip, port, *args)

    def _fmt(self, v):
        if isinstance(v, (list, tuple)):
            return "{" + ",".join([self._fmt(x) for x in v]) + "}"
        if isinstance(v, float):
            return "{:f}".format(v)
        if isinstance(v, int):
            return "{:d}".format(v)
        return str(v)

    def _build_cmd(self, name, *args, **kwargs):
        parts = []
        for a in args:
            parts.append(self._fmt(a))
        for k, v in kwargs.items():
            parts.append(f"{k}={self._fmt(v)}")
        return f"{name}(" + ",".join(parts) + ")"

    def EnableRobot(
        self,
        load=0.0,
        centerX=0.0,
        centerY=0.0,
        centerZ=0.0,
        isCheck=-1,
    ):
        """
        可选参数
        参数名 类型 说明
        load double
        设置负载重量，取值范围不能超过各个型号机器⼈的负载范围。单位：kg
        centerX double X⽅向偏⼼距离。取值范围：-999~ 999，单位：mm
        centerY double Y⽅向偏⼼距离。取值范围：-999~ 999，单位：mm
        centerZ double Z⽅向偏⼼距离。取值范围：-999~ 999，单位：mm
        isCheck int    是否检查负载。1表⽰检查，0表⽰不检查。如果设置为1，则机械臂
        使能后会检查实际负载是否和设置负载⼀致，如果不⼀致会⾃动下使
        能。默认值为0
        可携带的参数数量如下：
        0：不携带参数，表⽰使能时不设置负载重量和偏⼼参数。
        1：携带⼀个参数，该参数表⽰负载重量。
        4：携带四个参数，分别表⽰负载重量和偏⼼参数。
        5：携带五个参数，分别表⽰负载重量、偏⼼参数和是否检查负载。
        """
        """
            Optional parameter
            Parameter name     Type     Description
            load     double     Load weight. The value range should not exceed the load range of corresponding robot models. Unit: kg.
            centerX     double     X-direction eccentric distance. Range: -999 – 999, unit: mm.
            centerY     double     Y-direction eccentric distance. Range: -999 – 999, unit: mm.
            centerZ     double     Z-direction eccentric distance. Range: -999 – 999, unit: mm.
            isCheck     int     Check the load or not. 1: check, 0: not check. If set to 1, the robot arm will check whether the actual load is the same as the set load after it is enabled, and if not, it will be automatically disabled. 0 by default.
            The number of parameters that can be contained is as follows:
            0: no parameter (not set load weight and eccentric parameters when enabling the robot).
            1: one parameter (load weight).
            4: four parameters (load weight and eccentric parameters).
            5: five parameters (load weight, eccentric parameters, check the load or not).
                """
        string = "EnableRobot("
        if load != 0:
            string = string + "{:f}".format(load)
            if centerX != 0 or centerY != 0 or centerZ != 0:
                string = string + ",{:f},{:f},{:f}".format(centerX, centerY, centerZ)
                if isCheck != -1:
                    string = string + ",{:d}".format(isCheck)
        string = string + ")"
        return self.sendRecvMsg(string)

    def DisableRobot(self):
        """
        Disabled the robot
        下使能机械臂
        """
        string = "DisableRobot()"
        return self.sendRecvMsg(string)

    def ClearError(self):
        """
        Clear controller alarm information
        Clear the alarms of the robot. After clearing the alarm, you can judge whether the robot is still in the alarm status according to RobotMode.
        Some alarms cannot be cleared unless you resolve the alarm cause or restart the controller.
        清除机器⼈报警。清除报警后，⽤⼾可以根据RobotMode来判断机器⼈是否还处于报警状态。部
        分报警需要解决报警原因或者重启控制柜后才能清除。
        """
        string = "ClearError()"
        return self.sendRecvMsg(string)

    def PowerOn(self):
        """
        Powering on the robot
        Note: It takes about 10 seconds for the robot to be enabled after it is powered on.
        """
        string = "PowerOn()"
        return self.sendRecvMsg(string)

    def RunScript(self, project_name):
        """
        Run the script file
        project_name ：Script file name
        """
        string = "RunScript({:s})".format(project_name)
        return self.sendRecvMsg(string)

    def Stop(self):
        """
        停⽌已下发的运动指令队列或者RunScript指令运⾏的⼯程。
        Stop the delivered motion command queue or the RunScript command from running.
        """
        string = "Stop()"
        return self.sendRecvMsg(string)

    def Pause(self):
        """
        暂停已下发的运动指令队列或者RunScript指令运⾏的⼯程。
        Pause the delivered motion command queue or the RunScript command from running.
        """
        string = "Pause()"
        return self.sendRecvMsg(string)

    def Continue(self):
        """
        继续已暂停的运动指令队列或者RunScript指令运⾏的⼯程。
        Continue the paused motion command queue or the RunScript command from running.
        """
        string = "Continue()"
        return self.sendRecvMsg(string)

    def EmergencyStop(self, mode):
        """
        紧急停⽌机械臂。急停后机械臂会下使能并报警，需要松开急停、清除报警后才能重新使能。
        必选参数
        参数名 类型 说明
         mode int 急停操作模式。1表⽰按下急停，0表⽰松开急停
        Stop the robot in an emergency. After the emergency stop, the robot arm will be disabled and then alarm. You need to release the emergency stop and clear the alarm to re-enable the robot arm.
        Required parameter
        Parameter name     Type     Description
         mode     int     E-Stop operation mode. 1: press the E-Stop, 0: release the E-Stop.
        """
        string = "EmergencyStop({:d})".format(mode)
        return self.sendRecvMsg(string)

    def BrakeControl(self, axisID, value):
        """
        描述
        控制指定关节的抱闸。机械臂静⽌时关节会⾃动抱闸，如果⽤⼾需进⾏关节拖拽操作，可开启抱
        闸，即在机械臂下使能状态，⼿动扶住关节后，下发开启抱闸的指令。
        仅能在机器⼈下使能时控制关节抱闸，否则ErrorID会返回-1。
        必选参数
        参数名  类型  说明
        axisID int 关节轴序号，1表⽰J1轴，2表⽰J2轴，以此类推
        value int 设置抱闸状态。0表⽰抱闸锁死（关节不可移动），1表⽰松开抱闸（关节
        可移动）
        Description
        Control the brake of specified joint. The joints automatically brake when the robot is stationary. If you need to drag the joints, you can switch on the brake,
        i.e. hold the joint manually in the disabled status and deliver the command to switch on the brake.
        Joint brake can be controlled only when the robot arm is disabled, otherwise, Error ID will return -1.
        Required parameter:
        Parameter name     Type     Description
        axisID     int     joint ID, 1: J1, 2: J2, and so on
        Value     int     Set the status of brake. 0: switch off brake (joints cannot be dragged). 1: switch on brake (joints can be dragged).
        """
        string = "BrakeControl({:d},{:d})".format(axisID, value)
        return self.sendRecvMsg(string)

    #####################################################################

    def SpeedFactor(self, speed):
        """
        设置全局速度⽐例。
           机械臂点动时实际运动加速度/速度⽐例 = 控制软件点动设置中的值 x 全局速度⽐例。
           例：控制软件设置的关节速度为12°/s，全局速率为50%，则实际点动速度为12°/s x 50% =
           6°/s
           机械臂再现时实际运动加速度/速度⽐例 = 运动指令可选参数设置的⽐例 x 控制软件再现设置
           中的值 x 全局速度⽐例。
           例：控制软件设置的坐标系速度为2000mm/s，全局速率为50%，运动指令设置的速率为
           80%，则实际运动速度为2000mm/s x 50% x 80% = 800mm/s
        未设置时沿⽤进⼊TCP/IP控制模式前控制软件设置的值。
        取值范围：[1, 100]
        Set the global speed ratio.
           Actual robot acceleration/speed ratio in jogging = value in Jog settings × global speed ratio.
           Example: If the joint speed set in the software is 12°/s and the global speed ratio is 50%, then the actual jog speed is 12°/s x 50% =
           6°/s
           Actual robot acceleration/speed ratio in playback = ratio set in motion command × value in Playback settings
            × global speed ratio.
           Example: If the coordinate system speed set in the software is 2000mm/s, the global speed ratio is 50%, and the speed set in the motion command is
           80%, then the actual speed is 2000mm/s x 50% x 80% = 800mm/s.
        If it is not set, the value set by the software before entering TCP/IP control mode will be adopted.
        Range: [1, 100].
        """
        string = "SpeedFactor({:d})".format(speed)
        return self.sendRecvMsg(string)

    def User(self, index):
        """
        设置全局⽤⼾坐标系。⽤⼾下发运动指令时可选择⽤⼾坐标系，如未指定，则会使⽤全局⽤⼾坐标系。
        未设置时默认的全局⽤⼾坐标系为⽤⼾坐标系0。
        Set the global tool coordinate system. You can select a tool coordinate system while delivering motion commands. If you do not specify the tool coordinate system, the global tool coordinate system will be used.
        If it is not set, the default global user coordinate system is User coordinate system 0.
        """
        string = "User({:d})".format(index)
        return self.sendRecvMsg(string)

    def SetUser(self, index, table):
        """
        修改指定的⽤⼾坐标系。
        必选参数：
        参数名 类型 说明
        index int ⽤⼾坐标系索引，取值范围：[0,9]，坐标系0初始值为基坐标系。
        table string  修改后的⽤⼾坐标系，格式为{x, y, z, rx, ry, rz}，建议使⽤CalcUser指令获
        取。
        Modify the specified user coordinate system.
        Required parameter:
        Parameter name     Type     Description
        index    int     user coordinate system index, range: [0,9]. The initial value of coordinate system 0 refers to the base coordinate system.
        table    string     user coordinate system after modification (format: {x, y, z, rx, ry, rz}), which is recommended to obtain through "CalcUser" command.
        """
        string = "SetUser({:d},{:s})".format(index, table)
        return self.sendRecvMsg(string)

    def CalcUser(self, index, matrix_direction, table):
        """
        计算⽤⼾坐标系。
        必选参数：
        参数名 类型 说明
        index int ⽤⼾坐标系索引，取值范围：[0,9]，坐标系0初始值为基坐标系。
        matrix_direction int  计算的⽅向。1表⽰左乘，即index指定的坐标系沿基坐标系偏转table指定的值；
            0表⽰右乘，即index指定的坐标系沿⾃⼰偏转table指定的值。
        table string ⽤⼾坐标系偏移值，格式为{x, y, z, rx, ry, rz}。
        Calculate the user coordinate system.
        Required parameter:
        Parameter name     Type     Description
        Index    int     user coordinate system index, range: [0,9]. The initial value of coordinate system 0 refers to the base coordinate system.
        matrix_direction    int    Calculation method. 1: left multiplication, indicating that the coordinate system specified by "index" deflects the value specified by "table" along the base coordinate system.
            0: right multiplication, indicating that the coordinate system specified by "index" deflects the value specified by "table" along itself.
        table    string     user coordinate system offset (format: {x, y, z, rx, ry, rz}).
        """
        string = "CalcUser({:d},{:d},{:s})".format(index, matrix_direction, table)
        return self.sendRecvMsg(string)

    def Tool(self, index):
        """
        设置全局⼯具坐标系。⽤⼾下发运动指令时可选择⼯具坐标系，如未指定，则会使⽤全局⼯具坐标系。
        未设置时默认的全局⼯具坐标系为⼯具坐标系0。
        Set the global tool coordinate system. You can select a tool coordinate system while delivering motion commands. If you do not specify the tool coordinate system, the global tool coordinate system will be used.
        If it is not set, the default global tool coordinate system is Tool coordinate system 0.
        """
        string = "Tool({:d})".format(index)
        return self.sendRecvMsg(string)

    def SetTool(self, index, table):
        """
        修改指定的⼯具坐标系。
        必选参数：
        参数名 类型 说明
        index int ⼯具坐标系索引，取值范围：[0,9]，坐标系0初始值为法兰坐标系。
        table string  修改后的⼯具坐标系，格式为{x, y, z, rx, ry, rz}，表⽰该坐标系相对默认⼯
        具坐标系的偏移量。
        Modify the specified tool coordinate system.
        Required parameter:
        Parameter name     Type     Description
        Index    int     tool coordinate system index, range: [0,9]. The initial value of coordinate system 0 refers to the flange coordinate system.
        table    string     tool coordinate system after modification (format: {x, y, z, rx, ry, rz})
        """
        string = "SetTool({:d},{:s})".format(index, table)
        return self.sendRecvMsg(string)

    def CalcTool(self, index, matrix_direction, table):
        """
        计算⼯具坐标系。
        必选参数：
        参数名 类型 说明
        index int  ⼯具坐标系索引，取值范围：[0,9]，坐标系0初始值为法兰坐标系。
        matrix_direction int计算的⽅向。
          1表⽰左乘，即index指定的坐标系沿法兰坐标系偏转table指定的值；
          0表⽰右乘，即index指定的坐标系沿⾃⼰偏转table指定的值。
        table string ⼯具坐标系偏移值，格式为{x, y, z, rx, ry, rz}。
        Calculate the tool coordinate system.
        Required parameter:
        Parameter name     Type     Description
        Index    int     tool coordinate system index, range: [0,9]. The initial value of coordinate system 0 refers to the flange coordinate system.
        matrix_direction    int    Calculation method.
          1: left multiplication, indicating that the coordinate system specified by "index" deflects the value specified by "table" along the flange coordinate system.
          0: right multiplication, indicating that the coordinate system specified by "index" deflects the value specified by "table" along itself.
        table    string     tool coordinate system offset (format: {x, y, z, rx, ry, rz}).
        """
        string = "CalcTool({:d},{:d},{:s})".format(index, matrix_direction, table)
        return self.sendRecvMsg(string)

    def SetPayload(self, load=0.0, X=0.0, Y=0.0, Z=0.0, name="F"):
        """设置机械臂末端负载，⽀持两种设置⽅式。
        ⽅式⼀：直接设置负载参数
        必选参数1
        参数名 类型 说明
        load double  设置负载重量，取值范围不能超过各个型号机器⼈的负载范围。单位：kg
        可选参数1
        参数名 类型 说明
        x double 末端负载X轴偏⼼坐标。取值范围：范围：-500~500。单位：mm
        y double 末端负载Y轴偏⼼坐标。取值范围：范围：-500~500。单位：mm
        z double 末端负载Z轴偏⼼坐标。取值范围：范围：-500~500。单位：mm
        需同时设置或不设置这三个参数。偏⼼坐标为负载（含治具）的质⼼在默认⼯具坐标系下的坐标，
        参考下图。

        ⽅式⼆：通过控制软件保存的预设负载参数组设置
        必选参数2
        参数名 类型 说明
        name string 控制软件保存的预设负载参数组的名称
        Set the load of the robot arm.
        Method 1: Set the load parameters directly.
        Required parameter 1
        Parameter name     Type     Description
        load     double     Load weight. The value range should not exceed the load range of corresponding robot models. Unit: kg.
        Optional parameter 1
        Parameter name     Type     Description
        x     double     X-axis eccentric coordinates of the load. Range: -500 – 500. Unit: mm.
        y     double     Y-axis eccentric coordinates of the load. Range: -500 – 500. Unit: mm.
        z     double     Z-axis eccentric coordinates of the load. Range: -500 – 500. Unit: mm.
        The three parameters need to be set or not set at the same time. The eccentric coordinate is the coordinate of the center of mass of the load (including the fixture) under the default tool coordinate system.
        Refer to the figure below.

        Method 2: Set by the preset load parameter group saved by control software
        Required parameter 2
        Parameter name     Type     Description
        name     string     Name of the preset load parameter group saved by control software.
        """
        string = "SetPayload("
        if name != "F":
            string = string + "{:s}".format(name)
        else:
            if load != 0:
                string = string + "{:f}".format(load)
                if X != 0 or Y != 0 or Z != 0:
                    string = string + ",{:f},{:f},{:f}".format(X, Y, Z)
        string = string + ")"
        return self.sendRecvMsg(string)

    def AccJ(self, speed):
        """
        设置关节运动⽅式的加速度⽐例。
        未设置时默认值为100
        Set acceleration ratio of joint motion.
        Defaults to 100 if not set.
        """
        string = "AccJ({:d})".format(speed)
        return self.sendRecvMsg(string)

    def AccL(self, speed):
        """
        设置直线和弧线运动⽅式的加速度⽐例。
        未设置时默认值为100。
        Set acceleration ratio of linear and arc motion.
        Defaults to 100 if not set.
        """
        string = "AccL({:d})".format(speed)
        return self.sendRecvMsg(string)

    def VelJ(self, speed):
        """
        设置关节运动⽅式的速度⽐例。
        未设置时默认值为100。
        Set the speed ratio of joint motion.
        Defaults to 100 if not set.
        """
        string = "VelJ({:d})".format(speed)
        return self.sendRecvMsg(string)

    def VelL(self, speed):
        """
        设置直线和弧线运动⽅式的速度⽐例。
        未设置时默认值为100。
        Set the speed ratio of linear and arc motion.
        Defaults to 100 if not set.
        """
        string = "VelL({:d})".format(speed)
        return self.sendRecvMsg(string)

    def CP(self, ratio):
        """
        设置平滑过渡⽐例，即机械臂连续运动经过多个点时，经过中间点是以直⻆⽅式过渡还是以曲线⽅式过渡。
        未设置时默认值为0。
        平滑过渡⽐例。取值范围：[0, 100]
        Set the continuous path (CP) ratio, that is, when the robot arm moves continuously via multiple points, whether it transitions at a right angle or in a curved way when passing through the through point.
        Defaults to 0 if not set.
        Continuous path ratio. Range: [0, 100].
        """
        string = "CP({:d})".format(ratio)
        return self.sendRecvMsg(string)

    def SetCollisionLevel(self, level):
        """
        设置碰撞检测等级。
        未设置时沿⽤进⼊TCP/IP控制模式前控制软件设置的值。
        必选参数
        参数名 类型 说明
        level int 碰撞检测等级，0表⽰关闭碰撞检测，1~5数字越⼤灵敏度越⾼
        Set the collision detection level.
        If it is not set, the value set by the software before entering TCP/IP control mode will be adopted.
        Required parameter:
        Parameter name     Type     Description
        level     int     collision detection level, 0: switch off collision detection, 1 – 5: the larger the number, the higher the sensitivity.
        """
        string = "SetCollisionLevel({:d})".format(level)
        return self.sendRecvMsg(string)

    def SetBackDistance(self, distance):
        """
        设置机械臂检测到碰撞后原路回退的距离。
        未设置时沿⽤进⼊TCP/IP控制模式前控制软件设置的值。
        必选参数：
        参数名 类型 说明
        distance double 碰撞回退的距离，取值范围：[0,50]，单位：mm
        Set the backoff distance after the robot detects collision.
        If it is not set, the value set by the software before entering TCP/IP control mode will be adopted.
        Required parameter:
        Parameter name     Type     Description
        distance     double     collision backoff distance, range: [0,50], unit: mm.
        """
        string = "SetBackDistance({:d})".format(distance)
        return self.sendRecvMsg(string)

    def SetPostCollisionMode(self, mode):
        """
        设置机械臂检测到碰撞后进⼊的状态。
        未设置时沿⽤进⼊TCP/IP控制模式前控制软件设置的值。
        必选参数：
        参数名  类型 说明
        mode int  碰撞后处理⽅式，0表⽰检测到碰撞后进⼊停⽌状态，1表⽰检测到碰撞后
        进⼊暂停状态
        Set the backoff distance after the robot detects collision.
        If it is not set, the value set by the software before entering TCP/IP control mode will be adopted.
        Required parameter:
        Parameter name     Type     Description
        mode     int     post-collision processing mode, 0: enter the stop status after the collision is detected, 1: enter the pause status after the collision is detected
        """
        string = "SetPostCollisionMode({:d})".format(mode)
        return self.sendRecvMsg(string)

    def StartDrag(self):
        """
        机械臂进⼊拖拽模式。机械臂处于报警状态下时，⽆法通过该指令进⼊拖拽模式。
        The robot arm enters the drag mode. The robot cannot enter the drag mode through this command in error status.
        """
        string = "StartDrag()"
        return self.sendRecvMsg(string)

    def StopDrag(self):
        """
        退出拖拽
        The robot arm enters the drag mode. The robot cannot enter the drag mode through this command in error status.
        """
        string = "StopDrag()"
        return self.sendRecvMsg(string)

    def DragSensivity(self, index, value):
        """
        设置拖拽灵敏度。
        未设置时沿⽤进⼊TCP/IP控制模式前控制软件设置的值。
        必选参数
        参数名 类型 说明
        index int 轴序号，1~6分别表⽰J1~J6轴，0表⽰所有轴同时设置
        value int 拖拽灵敏度，值越⼩，拖拽时的阻⼒越⼤。取值范围：[1, 90]
        Set the drag sensitivity.
        If it is not set, the value set by the software before entering TCP/IP control mode will be adopted.
        Required parameter:
        Parameter name     Type     Description
        index     int      axis ID, 1 – 6: J1 – J6, 0: set all axes at the same time.
        value     int     Drag sensitivity. The smaller the value, the greater the force when dragging. Range: [1, 90].
        """
        string = "DragSensivity({:d},{:d})".format(index, value)
        return self.sendRecvMsg(string)

    def EnableSafeSkin(self, status):
        """
        开启或关闭安全⽪肤功能。仅对安装了安全⽪肤的机械臂有效。
        必选参数
        参数名 类型 说明
        status int 电⼦⽪肤功能开关，0表⽰关闭，1表⽰开启
        Switch on or off the SafeSkin. Valid only for robot arms equipped with SafeSkin.
        Required parameter:
        Parameter name     Type     Description
        status     int     SafeSkin switch, 0: off, 1: on.
        """
        string = "EnableSafeSkin({:d})".format(status)
        return self.sendRecvMsg(string)

    def SetSafeSkin(self, part, status):
        """
        设置安全⽪肤各个部位的灵敏度。仅对安装了安全⽪肤的机械臂有效。
        未设置时沿⽤进⼊TCP/IP控制模式前控制软件设置的值。
        必选参数
        参数名 类型 说明
        part int 要设置的部位，3表⽰⼩臂，4~6分别表⽰J4~J6关节
        status int 灵敏度，0表⽰关闭，1表⽰low，2表⽰middle，3表⽰high
        Set the sensitivity for each part of the SafeSkin. Valid only for robot arms equipped with SafeSkin.
        If it is not set, the value set by the software before entering TCP/IP control mode will be adopted.
        Required parameter:
        Parameter name     Type     Description
        part     int     The part to be set. 3: forearm, 4 – 6: J4 – J6
        status     int     sensitivity, 0: off, 1: low, 2: middle, 3: high
        """
        string = "SetSafeSkin({:d},{:d})".format(part, status)
        return self.sendRecvMsg(string)

    def SetSafeWallEnable(self, index, value):
        """
        开启或关闭指定的安全墙。
        必选参数：
        参数名 类型 说明
        index int 要设置的安全墙索引，需要先在控制软件中添加对应的安全墙。取值范围：[1,8]
        value int 安全墙开关，0表⽰关闭，1表⽰开启
        Switch on/off the specified safety wall.
        Required parameter:
        Parameter name     Type     Description
        index     int     safety wall index, which needs to be added in the software first. Range: [1.8].
        value      int     SafeSkin switch, 0: off, 1: on.
        """
        string = "SetSafeWallEnable({:d},{:d})".format(index, value)
        return self.sendRecvMsg(string)

    def SetWorkZoneEnable(self, index, value):
        """
        开启或关闭指定的⼲涉区。
        必选参数：
        参数名 类型 说明
        index int 要设置的⼲涉区索引，需要先在控制软件中添加对应的⼲涉区。取值范围：[1,6]
        value int ⼲涉区开关，0表⽰关闭，1表⽰开启
        Switch on/off the specified interference area.
        Required parameter:
        Parameter name     Type     Description
        index     int     interference area index, which needs to be added in the software first. Range: [1.6].
        value      int     interference area switch, 0: off, 1: on.
        """
        string = "SetWorkZoneEnable({:d},{:d})".format(index, value)
        return self.sendRecvMsg(string)

    #########################################################################

    def RobotMode(self):
        """
        获取机器⼈当前状态。
        1 ROBOT_MODE_INIT 初始化状态
        2 ROBOT_MODE_BRAKE_OPEN 有任意关节的抱闸松开
        3 ROBOT_MODE_POWEROFF 机械臂下电状态
        4 ROBOT_MODE_DISABLED 未使能（⽆抱闸松开）
        5 ROBOT_MODE_ENABLE 使能且空闲
        6 ROBOT_MODE_BACKDRIVE 拖拽模式
        7 ROBOT_MODE_RUNNING 运⾏状态(⼯程，TCP队列运动等)
        8 ROBOT_MODE_SINGLE_MOVE 单次运动状态（点动、RunTo等）
        9 ROBOT_MODE_ERROR
             有未清除的报警。此状态优先级最⾼，⽆论机械臂
             处于什么状态，有报警时都返回9
        10 ROBOT_MODE_PAUSE ⼯程状态
        11 ROBOT_MODE_COLLISION 碰撞检测触发状态
        Get the current status of the robot.
        1 ROBOT_MODE_INIT  Initialized status
        2 ROBOT_MODE_BRAKE_OPEN  Brake switched on
        3 ROBOT_MODE_POWEROFF  Power-off status
        4 ROBOT_MODE_DISABLED  Disabled (no brake switched on
        5 ROBOT_MODE_ENABLE  Enabled and idle
        6 ROBOT_MODE_BACKDRIVE  Drag mode
        7 ROBOT_MODE_RUNNING  Running status (project, TCP queue)
        8 ROBOT_MODE_SINGLE_MOVE  Single motion status (jog, RunTo)
        9 ROBOT_MODE_ERROR
             There are uncleared alarms. This status has the highest priority. It returns 9 when there is an alarm, regardless of the status of the robot arm.
        10 ROBOT_MODE_PAUSE  Pause status
        11 ROBOT_MODE_COLLISION  Collision status
        """
        string = "RobotMode()"
        return self.sendRecvMsg(string)

    def PositiveKin(self, J1, J2, J3, J4, J5, J6, user=-1, tool=-1):
        """
        描述
        进⾏正解运算：给定机械臂各关节⻆度，计算机械臂末端在给定的笛卡尔坐标系中的坐标值。
        必选参数
        参数名 类型 说明
        J1 double J1轴位置，单位：度
        J2 double J2轴位置，单位：度
        J3 double J3轴位置，单位：度
        J4 double J4轴位置，单位：度
        J5 double J5轴位置，单位：度
        J6 double J6轴位置，单位：度
        可选参数
        参数名 类型 说明
        格式为"user=index"，index为已标定的⽤⼾坐标系索引。
        User string 不指定时使⽤全局⽤⼾坐标系。
        Tool string  格式为"tool=index"，index为已标定的⼯具坐标系索引。不指定时使⽤全局⼯具坐标系。
        Description
        Positive solution. Calculate the coordinates of the end of the robot in the specified Cartesian coordinate system, based on the given angle of each joint.
        Required parameter:
        Parameter name     Type     Description
        J1     double     J1-axis position, unit: °
        J2     double     J2-axis position, unit: °
        J3     double     J3-axis position, unit: °
        J4     double     J4-axis position, unit: °
        J5     double     J5-axis position, unit: °
        J6     double     J6-axis position, unit: °
        Optional parameter:
        Parameter name     Type     Description
        Format: "user=index", index: index of the calibrated user coordinate system.
        User     string     The global user coordinate system will be used if it is not specified.
        Tool     string     Format: "tool=index", index: index of the calibrated tool coordinate system. The global tool coordinate system will be used if it is not set.
        """
        string = "PositiveKin({:f},{:f},{:f},{:f},{:f},{:f}".format(
            J1, J2, J3, J4, J5, J6
        )
        params = []
        if user != -1:
            params.append("user={:d}".format(user))
        if tool != -1:
            params.append("tool={:d}".format(tool))
        for ii in params:
            string = string + "," + ii
        string = string + ")"
        return self.sendRecvMsg(string)

    def InverseKin(
        self, X, Y, Z, Rx, Ry, Rz, user=-1, tool=-1, useJointNear=-1, JointNear=""
    ):
        """
        描述
        进⾏逆解运算：给定机械臂末端在给定的笛卡尔坐标系中的坐标值，计算机械臂各关节⻆度。
        由于笛卡尔坐标仅定义了TCP的空间坐标与倾斜⻆，所以机械臂可以通过多种不同的姿态到达同⼀
        个位姿，意味着⼀个位姿变量可以对应多个关节变量。为得出唯⼀的解，系统需要⼀个指定的关节
        坐标，选择最接近该关节坐标的解作为逆解结果。
        必选参数
        参数名 类型 说明
        X double X轴位置，单位：mm
        Y double Y轴位置，单位：mm
        Z double Z轴位置，单位：mm
        Rx double Rx轴位置，单位：度
        Ry double Ry轴位置，单位：度
        Rz double Rz轴位置，单位：度
        可选参数
        参数名 类型 说明
        User string  格式为"user=index"，index为已标定的⽤⼾坐标系索引。不指定时使⽤全局⽤⼾坐标系。
        Tool string  格式为"tool=index"，index为已标定的⼯具坐标系索引。不指定时使⽤全局⼯具坐标系。
        useJointNear string  ⽤于设置JointNear参数是否有效。
            "useJointNear=0"或不携带表⽰JointNear⽆效，系统根据机械臂当前关节⻆度就近选解。
            "useJointNear=1"表⽰根据JointNear就近选解。
        jointNear string 格式为"jointNear={j1,j2,j3,j4,j5,j6}"，⽤于就近选解的关节坐标。
        Description
        Inverse solution. Calculate the joint angles of the robot, based on the given coordinates in the specified Cartesian coordinate system.
        As Cartesian coordinates only define the spatial coordinates and tilt angle of the TCP, the robot arm can reach the same posture through different gestures, which means that one posture variable can correspond to multiple joint variables.
        To get a unique solution, the system requires a specified joint coordinate, and the solution closest to this joint coordinate is selected as the inverse solution。
        Required parameter:
        Parameter name     Type     Description
        X     double     X-axis position, unit: mm
        Y     double     Y-axis position, unit: mm
        Z     double     Z-axis position, unit: mm
        Rx     double     Rx-axis position, unit: °
        Ry     double     Ry-axis position, unit: °
        Rz     double     Rz-axis position, unit: °
        Optional parameter:
        Parameter name     Type     Description
        User      string     Format: "user=index", index: index of the calibrated user coordinate system. The global user coordinate system will be used if it is not set.
        Tool     string     Format: "tool=index", index: index of the calibrated tool coordinate system. The global tool coordinate system will be used if it is not set.
        useJointNear     string     used to set whether JointNear is effective.
            "useJointNear=0" or null: JointNear data is ineffective. The algorithm selects the joint angles according to the current angle.
            "useJointNear=1": the algorithm selects the joint angles according to JointNear data.
        jointNear     string     Format: "jointNear={j1,j2,j3,j4,j5,j6}", joint coordinates for selecting joint angles.
        """
        string = "InverseKin({:f},{:f},{:f},{:f},{:f},{:f}".format(X, Y, Z, Rx, Ry, Rz)
        params = []
        if user != -1:
            params.append("user={:d}".format(user))
        if tool != -1:
            params.append("tool={:d}".format(tool))
        if useJointNear != -1:
            params.append("useJointNear={:d}".format(useJointNear))
        if JointNear != "":
            params.append("JointNear={:s}".format(JointNear))
        for ii in params:
            string = string + "," + ii
        string = string + ")"
        return self.sendRecvMsg(string)

    def GetAngle(self):
        """
        获取机械臂当前位姿的关节坐标。
        Get the joint coordinates of current posture.
        """
        string = "GetAngle()"
        return self.sendRecvMsg(string)

    def GetPose(self, user=-1, tool=-1):
        """
        获取机械臂当前位姿在指定的坐标系下的笛卡尔坐标。
        可选参数
        参数名 类型 说明
        User string 格式为"user=index"，index为已标定的⽤⼾坐标系索引。
        Tool string 格式为"tool=index"，index为已标定的⽤⼾坐标系索引。
        必须同时传或同时不传，不传时默认为全局⽤⼾和⼯具坐标系。
        Get the Cartesian coordinates of the current posture under the specific coordinate system.
        Optional parameter:
        Parameter name     Type     Description
        User      string     Format: "user=index", index: index of the calibrated user coordinate system.
        Tool     string     Format: "tool=index", index: index of the calibrated tool coordinate system.
        They need to be set or not set at the same time. They are global user coordinate system and global tool coordinate system if not set.
        """
        string = "GetPose("
        params = []
        state = True
        if user != -1:
            params.append("user={:d}".format(user))
            state = not state
        if tool != -1:
            params.append("tool={:d}".format(tool))
            state = not state
        if not state:
            return "need to be set or not set at the same time. They are global user coordinate system and global tool coordinate system if not set"  # 必须同时传或同时不传坐标系，不传时默认为全局⽤⼾和⼯具坐标系

        for i, param in enumerate(params):
            if i == len(params) - 1:
                string = string + param
            else:
                string = string + param + ","

        string = string + ")"
        return self.sendRecvMsg(string)

    def GetErrorID(self):
        """
        获取机械臂当前位姿的关节坐标。
        Get the joint coordinates of current posture.
        """
        string = "GetErrorID()"
        return self.sendRecvMsg(string)

    #################################################################

    def DO(self, index, status, time=-1):
        """
        设置数字输出端⼝状态（队列指令）。
        必选参数
        参数名 类型 说明
        index int DO端⼦的编号
        status int DO端⼦的状态，1：ON；0：OFF
        可选参数
        参数名 类型  说明
        time int 持续输出时间，取值范围：[25, 60000]。单位：ms
        如果设置了该参数，系统会在指定时间后对DO⾃动取反。取反为异步动作，
        不会阻塞指令队列，系统执⾏了DO输出后就会执⾏下⼀条指令。
        Set the status of digital output port (queue command).
        Required parameter:
        Parameter name     Type     Description
        index     int     DO index
        status     int     DO index, 1: ON, 0: OFF
        Optional parameter:
        Parameter name     Type     Description
        time     int     continuous output time, range: [25,60000]. Unit: ms.
        If this parameter is set, the system will automatically invert the DO after the specified time.
        The inversion is an asynchronous action, which will not block the command queue. After the DO output is executed, the system will execute the next command.
        """
        string = "DO({:d},{:d}".format(index, status)
        params = []
        if time != -1:
            params.append("{:d}".format(time))
        for ii in params:
            string = string + "," + ii
        string = string + ")"
        return self.sendRecvMsg(string)

    def DOInstant(self, index, status):
        """
        设置数字输出端⼝状态（⽴即指令）。
        必选参数
        参数名 类型 说明
        index int DO端⼦的编号
        status int DO端⼦的状态，1：ON；0：OFF
        Set the status of digital output port (immediate command).
        Required parameter:
        Parameter name     Type     Description
        index     int     DO index
        status     int     DO index, 1: ON, 0: OFF
        """
        string = "DOInstant({:d},{:d})".format(index, status)
        return self.sendRecvMsg(string)

    def GetDO(self, index):
        """
        获取数字输出端⼝状态。
        必选参数
        参数名 类型 说明
        index int DO端⼦的编号
        Get the status of digital output port.
        Required parameter:
        Parameter name     Type     Description
        index     int     DO index
        """
        string = "GetDO({:d})".format(index)
        return self.sendRecvMsg(string)

    def DOGroup(self, *index_value):
        """
        设置多个数字输出端⼝状态（队列指令）。
        必选参数
        参数名 类型 说明
        index1 int 第⼀个DO端⼦的编号
        value1 int 第⼀个DO端⼦的状态，1：ON；0：OFF
        ... ... ...
        indexN int 第N个DO端⼦的编号
        valueN int 第N个DO端⼦的状态，1：ON；0：OFF
        返回
        ErrorID,{ResultID},DOGroup(index1,value1,index2,value2,...,indexN,valueN);
        ResultID为算法队列ID，可⽤于判断指令执⾏顺序。
        ⽰例
        DOGroup(4,1,6,0,2,1,7,0)
        设置DO_4为ON，DO_6为OFF，DO_2为ON，DO_7为OFF。
        Set the status of multiple digital output ports (queue command).
        Required parameter:
        Parameter name     Type     Description
        index1     int     index of the first DO
        value1      int     status of the first DO, 1: ON, 0: OFF
        ... ... ...
        indexN     int     index of the last DO
        valueN      int     status of the last DO, 1: ON, 0: OFF
        Return
        ErrorID,{ResultID},DOGroup(index1,value1,index2,value2,...,indexN,valueN);
        ResultID is algorithm queue ID, used to judge the order in which commands are executed.
        Example
        DOGroup(4,1,6,0,2,1,7,0)
        Set DO_4 to ON, DO_6 to OFF, DO_2 to ON, DO_7 to OFF.
        """
        string = "DOGroup({:d}".format(index_value[0])
        for ii in index_value[1:]:
            string = string + "," + str(ii)
        string = string + ")"

        return self.sendRecvMsg(string)

    def GetDOGroup(self, *index_value):
        """
        获取多个数字输出端⼝状态。
        必选参数
        参数名 类型 说明
        index int 第⼀个DO端⼦的编号
        ... ... ...
        indexN int 第N个DO端⼦的编号
        返回
        ErrorID,{value1,value2,...,valueN},GetDOGroup(index1,index2,...,indexN);
        {value1,value2,...,valueN}分别表⽰DO_1到DO_N的状态，0为OFF，1为ON
        ⽰例
        GetDOGroup(1,2)
        获取DO_1和DO_2的状态。
        Get the status of multiple digital output ports.
        Required parameter:
        Parameter name     Type     Description
        index     int     index of the first DO
        ... ... ...
        indexN     int     index of the last DO
        Return
        ErrorID,{value1,value2,...,valueN},GetDOGroup(index1,index2,...,indexN);
        {value1,value2,...,valueN}: status of DO_1 – DO_N. 0: OFF, 1: ON.
        Example
        GetDOGroup(1,2)
        Get the status of DO_1 and DO_2.
        """
        string = "GetDOGroup({:d}".format(index_value[0])
        for ii in index_value[1:]:
            string = string + "," + str(ii)
        string = string + ")"
        return self.sendRecvMsg(string)

    def ToolDO(self, index, status):
        """
        设置末端数字输出端⼝状态（队列指令）。
        必选参数
        参数名 类型 说明
        index int 末端DO端⼦的编号
        status int 末端DO端⼦的状态，1：ON；0：OFF
        Set the status of tool digital output port (queue command).
        Required parameter:
        Parameter name     Type     Description
        index     int     index of the tool DO
        status     int     status of the tool DO, 1: ON, 0: OFF
        """
        string = "ToolDO({:d},{:d})".format(index, status)
        return self.sendRecvMsg(string)

    def ToolDOInstant(self, index, status):
        """
        设置末端数字输出端⼝状态（⽴即指令）
        必选参数
        参数名 类型 说明
        index int 末端DO端⼦的编号
        status int 末端DO端⼦的状态，1：ON；0：OFF
        Set the status of tool digital output port (immediate command)
        Required parameter:
        Parameter name     Type     Description
        index     int     index of the tool DO
        status     int     status of the tool DO, 1: ON, 0: OFF
        """
        string = "ToolDOInstant({:d},{:d})".format(index, status)
        return self.sendRecvMsg(string)

    def GetToolDO(self, index):
        """
        设置末端数字输出端⼝状态（⽴即指令）
        必选参数
        参数名 类型 说明
        index int 末端DO端⼦的编号
        status int 末端DO端⼦的状态，1：ON；0：OFF
        Set the status of tool digital output port (immediate command)
        Required parameter:
        Parameter name     Type     Description
        index     int     index of the tool DO
        status     int     status of the tool DO, 1: ON, 0: OFF
        """
        string = "GetToolDO({:d})".format(index)
        return self.sendRecvMsg(string)

    def AO(self, index, value):
        """
        设置模拟输出端⼝的值（队列指令）。
        必选参数
        参数
        名
        类型 说明
        index int AO端⼦的编号
        value double AO端⼦的输出值，电压取值范围：[0,10]，单位：V；电流取值范围：[4,20]，单位：mA
        Set the value of analog output port (queue command).
        Required parameter:
        Parameter name     Type     Description
        index     int     AO index
        value     double     AO output, voltage range: [0,10], unit: V; current range: [4,20], unit: mA
        """
        string = "AO({:d},{:f})".format(index, value)
        return self.sendRecvMsg(string)

    def AOInstant(self, index, value):
        """
        设置模拟输出端⼝的值（⽴即指令）。
        必选参数
        参数名 类型 说明
        index int AO端⼦的编号
        value double AO端⼦的输出值，电压取值范围：[0,10]，单位：V；电流取值范围：
        [4,20]，单位：mA
        Set the value of analog output port (immediate command).
        Required parameter:
        Parameter name     Type     Description
        index     int     AO index
        value     double     AO output, voltage range: [0,10], unit: V; current range:
        [4,20], unit: mA
        """
        string = "AOInstant({:d},{:f})".format(index, value)
        return self.sendRecvMsg(string)

    def GetAO(self, index):
        """
        获取模拟量输出端⼝的值。
        必选参数
        参数名 类型 说明
        index int AO端⼦的编号
        Get the value of analog output port.
        Required parameter:
        Parameter name     Type     Description
        index     int     AO index
        """
        string = "GetAO({:d})".format(index)
        return self.sendRecvMsg(string)

    def DI(self, index):
        """
        获取DI端⼝的状态。
        必选参数
        参数名 类型 说明
        index int DI端⼦的编号
        Get status of DI port.
        Required parameter:
        Parameter name     Type     Description
        index     int     DI index
        """
        string = "DI({:d})".format(index)
        return self.sendRecvMsg(string)

    def DIGroup(self, *index_value):
        """
        获取多个DI端⼝的状态。
        必选参数
        参数名 类型 说明
        index1 int 第⼀个DI端⼦的编号
        ... ... ...
        indexN int 第N个DI端⼦的编号
        返回
        ErrorID,{value1,value2,...,valueN},DIGroup(index1,index2,...,indexN);
        {value1,value2,...,valueN}分别表⽰DI_1到DI_N的状态，0为OFF，1为ON
        ⽰例
        DIGroup(4,6,2,7)
        获取DI_4，DI_6，DI_2，DI_7的状态。
        Get status of multiple DI ports.
        Required parameter:
        Parameter name     Type     Description
        index1     int     index of the first DI
        ... ... ...
        indexN     int     index of the last DI
        Return
        ErrorID,{value1,value2,...,valueN},DIGroup(index1,index2,...,indexN);
        {value1,value2,...,valueN}: status of DI_1 – DI_N. 0: OFF, 1: ON.
        Example
        DIGroup(4,6,2,7)
        Get the status of DI_4, DI_6, DI_2 and DI_7.
        """
        string = "DIGroup({:d}".format(index_value[0])
        for ii in index_value[1:]:
            string = string + "," + str(ii)
        string = string + ")"
        return self.sendRecvMsg(string)

    def ToolDI(self, index):
        """
        获取末端DI端⼝的状态。
        必选参数
        参数名 类型 说明
        index int 末端DI端⼦的编号
        Get the status of tool digital input port.
        Required parameter:
        Parameter name     Type     Description
        index     int     index of the tool DI
        """
        string = "ToolDI({:d})".format(index)
        return self.sendRecvMsg(string)

    def AI(self, index):
        """
        获取AI端⼝的值。
        必选参数
        参数名 类型 说明
        index int AI端⼦的编号
        Get the value of analog input port.
        Required parameter:
        Parameter name     Type     Description
        index     int     AI index
        """
        string = "AI({:d})".format(index)
        return self.sendRecvMsg(string)

    def ToolAI(self, index):
        """
        获取末端AI端⼝的值。使⽤前需要通过SetToolMode将端⼦设置为模拟输⼊模式。
        必选参数
        参数名 类型 说明
        index int 末端AI端⼦的编号
        Get the value of tool analog input port. You need to set the port to analog-input mode through SetToolMode before use.
        Required parameter:
        Parameter name     Type     Description
        index     int     index of the tool AI
        """
        string = "ToolAI({:d})".format(index)
        return self.sendRecvMsg(string)

    def SetTool485(self, index, parity="", stopbit=-1, identify=-1):
        """
        描述:
        设置末端⼯具的RS485接⼝对应的数据格式。
        必选参数
        参数名 类型 说明
        baud int RS485接⼝的波特率
        可选参数
        参数名 类型 说明
        parity string
        是否有奇偶校验位。"O"表⽰奇校验，"E"表⽰偶校验，"N"表⽰⽆奇偶
        校验位。默认值为"N"。
        stopbit int 停⽌位⻓度。取值范围：1，2。默认值为1。
        identify int 当机械臂为多航插机型时，⽤于指定设置的航插。1：航插1；2：航插2
        返回
        ErrorID,{},SetTool485(baud,parity,stopbit);
        ⽰例：
        SetTool485(115200,"N",1)
        将末端⼯具的RS485接⼝对应的波特率设置为115200Hz，⽆奇偶校验位，停⽌位⻓度为1。
        Description:
        Set the data type corresponding to the RS485 interface of the end tool.
        Required parameter:
        Parameter name     Type     Description
        baud     int     baud rate of RS485 interface
        Optional parameter:
        Parameter name     Type     Description
        parity string     Whether there are parity bits. "O" means odd, "E" means even, and "N" means no parity bit. "N" by default.
        stopbit     int     stop bit length Range: 1, 2 1 by default.
        identify     int     If the robot is equipped with multiple aviation sockets, you need to specify them. 1: aviation 1; 2: aviation 2
        Return
        ErrorID,{},SetTool485(baud,parity,stopbit);
        Example
        SetTool485(115200,"N",1)
        Set the baud rate corresponding to the tool RS485 interface to 115200Hz, parity bit to N, and stop bit length to 1.
        """
        string = "SetTool485({:d}".format(index)
        params = []
        if parity != "":
            params.append(parity)
        if string != -1:
            params.append("{:d}".format(stopbit))
            if identify != -1:
                params.append("{:d}".format(identify))
        else:
            if identify != -1:
                params.append(
                    "1,{:d}".format(identify)
                )  # 选择航插没设停止位，默认为1  no stop bit, 1 by default
        for ii in params:
            string = string + "," + ii
        string = string + ")"
        return self.sendRecvMsg(string)

    def SetToolPower(self, status, identify=-1):
        """
        设置末端⼯具供电状态，⼀般⽤于重启末端电源，例如对末端夹⽖重新上电初始化。如需连续调⽤
        该接⼝，建议⾄少间隔4ms以上。
        说明：
        Magician E6机器⼈不⽀持该指令，调⽤⽆效果。
        必选参数
        参数名 类型 说明
        status int 末端⼯具供电状态，0：关闭电源；1：打开电源
        可选参数
        参数名 类型 说明
        identify int 当机械臂为多航插机型时，⽤于指定设置的航插。1：航插1；2：航插2
        返回
        ErrorID,{},SetToolPower(status);
        ⽰例：
        SetToolPower(0)
        关闭末端电源。
        Set the power status of the end tool, generally used for restarting the end power, such as re-powering and re-initializing the gripper.
        If you need to call the interface continuously, it is recommended to keep an interval of at least 4 ms.
        NOTE:
        This command is not supported on Magician E6 robot, and there is no effect when calling it.
        Required parameter:
        Parameter name     Type     Description
        status    int     power status of end tool. 0: power off; 1: power on.
        Optional parameter:
        Parameter name     Type     Description
        identify     int     If the robot is equipped with multiple aviation sockets, you need to specify them. 1: aviation 1; 2: aviation 2
        Return
        ErrorID,{},SetToolPower(status);
        Example
        SetToolPower(0)
        Power off the tool.
        """
        string = "SetToolPower({:d}".format(status)
        params = []
        if identify != -1:
            params.append("{:d}".format(identify))
        for ii in params:
            string = string + "," + ii
        string = string + ")"
        return self.sendRecvMsg(string)

    def SetToolMode(self, mode, type, identify=-1):
        """
        描述:
        机械臂末端AI接⼝与485接⼝复⽤端⼦时，可通过此接⼝设置末端复⽤端⼦的模式。默认模式为
        485模式。
        说明：
        不⽀持末端模式切换的机械臂调⽤此接⼝⽆效果。
        必选参数
        参数名 类型 说明
        mode int 复⽤端⼦的模式，1：485模式，2：模拟输⼊模式
        type int  当mode为1时，该该参数⽆效。当mode为2时，可设置模拟输⼊的模式。
                  个位表⽰AI1的模式，⼗位表⽰AI2的模式，⼗位为0时可仅输⼊个位。
        模式：
        0：0~10V电压输⼊模式
        1：电流采集模式
        2：0~5V电压输⼊模式
        例⼦：
        0：AI1与AI2均为0~10V电压输⼊模式
        1：AI2是0~10V电压输⼊模式，AI1是电流采集模式
        11：AI2和AI1都是电流采集模式
        12：AI2是电流采集模式，AI1是0~5V电压输⼊模式
        20：AI2是0~5V电压输⼊模式，AI1是0~10V电压输⼊模式
        可选参数
        参数名 类型 说明
        identify int 当机械臂为多航插机型时，⽤于指定设置的航插。1：航插1；2：航插2
        返回
        ErrorID,{},SetToolMode(mode,type);
        ⽰例：
        SetToolMode(2,0)
        设置末端复⽤端⼦为模拟输⼊，两路都是0~10V电压输⼊模式。
        Description:
        If the AI interface on the end of the robot arm is multiplexed with the 485 interface, you can set the mode of the end multiplex terminal via this interface.
        485 mode by default.
        NOTE:
        The robot arm without tool RS485 interface has no effect when calling this interface.
        Required parameter:
        Parameter name     Type     Description
        mode     int     mode of the multiplex terminal, 1: 485 mode, 2: AI mode
        type     int     When mode is 1, this parameter is invalid. When mode is 2, you can set the mode of AI.
                  The single digit indicates the mode of AI1, the tens digit indicates the mode of AI2. When the tens digit is 0, you can enter only the single digit.
        Mode:
        0: 0 – 10V voltage input mode
        1: Current collection mode
        2: 0 – 5V voltage input mode
        Example:
        0: AI1 and AI2 are 0 – 10V voltage input mode
        1: AI2 is 0 – 10V voltage input mode, AI1 is current collection mode
        11: AI2 and AI1 are current collection mode
        12: AI2 is current collection mode, AI1 is 0 – 5V voltage input mode
        20: AI2 is 0 – 5V voltage input mode, AI1 is 0 – 10V voltage input mode
        Optional parameter:
        Parameter name     Type     Description
        identify     int     If the robot is equipped with multiple aviation sockets, you need to specify them. 1: aviation 1; 2: aviation 2
        Return
        ErrorID,{},SetToolMode(mode,type);
        Example
        SetToolMode(2,0)
        Set the mode of the end multiplex terminal to AI, both are 0 – 10V voltage input mode.
        """
        string = "SetToolMode({:d},{:d}".format(mode, type)
        params = []
        if identify != -1:
            params.append("{:d}".format(identify))
        for ii in params:
            string = string + "," + ii
        string = string + ")"
        return self.sendRecvMsg(string)

    ##################################################################

    def ModbusCreate(self, ip, port, slave_id, isRTU=-1):
        """
        创建Modbus主站，并和从站建⽴连接。最多⽀持同时连接5个设备。
        必选参数
        参数名 类型 说明
        ip string 从站IP地址
        port int 从站端⼝
        slave_id int 从站ID
        可选参数
        参数名 类型 说明
        isRTU int 如果不携带或为0，建⽴modbusTCP通信； 如果为1，建⽴modbusRTU通信
        Create Modbus master, and establish connection with the slave. (support connecting to at most 5 devices).
        Required parameter:
        Parameter name     Type     Description
        ip     string     slave IP address
        port     int     slave port
        slave_id     int     slave ID
        Optional parameter:
        Parameter name     Type     Description
        isRTU     int     null or 0: establish ModbusTCP communication; 1: establish ModbusRTU communication
        """
        string = "ModbusCreate({:s},{:d},{:d}".format(ip, port, slave_id)
        params = []
        if isRTU != -1:
            params.append("{:d}".format(isRTU))
        for ii in params:
            string = string + "," + ii
        string = string + ")"
        return self.sendRecvMsg(string)

    def ModbusRTUCreate(self, slave_id, baud, parity="", data_bit=8, stop_bit=-1):
        """
        创建基于RS485接⼝的Modbus主站，并和从站建⽴连接。最多⽀持同时连接5个设备。
        必选参数
        参数名 类型 说明
        slave_id int 从站ID
        baud int RS485接⼝的波特率。
        可选参数
        参数名 类型 说明
        parity string
        是否有奇偶校验位。"O"表⽰奇校验，"E"表⽰偶校验，"N"表⽰⽆奇偶
        校验位。默认值为"E"。
        data_bit int 数据位⻓度。取值范围：8。默认值为8。
        stop_bit int 停⽌位⻓度。取值范围：1，2。默认值为1。
        Create Modbus master station based on RS485, and establish connection with slave station (support connecting to at most 5 devices).
        Required parameter:
        Parameter name     Type     Description
        slave_id     int     slave ID
        baud     int     baud rate of RS485 interface.
        Optional parameter:
        Parameter name     Type     Description
        parity string     Whether there are parity bits. "O" means odd, "E" means even, and "N" means no parity bit. "E" by default.
        data_bit     int     data bit length Range: 8 (8 by default).
        stop_bit     int     stop bit length Range: 1, 2 (1 by default).
        """
        string = "ModbusRTUCreate({:d},{:d}".format(slave_id, baud)
        params = []
        if parity != "":
            params.append("{:s}".format(parity))
        if data_bit != 8:
            params.append("{:d}".format(data_bit))
        if stop_bit != -1:
            params.append("{:d}".format(stop_bit))
        for ii in params:
            string = string + "," + ii
        string = string + ")"
        return self.sendRecvMsg(string)

    def ModbusClose(self, index):
        """
        和Modbus从站断开连接，释放主站。
        必选参数
        参数名 类型 说明
        index int 创建主站时返回的主站索引
        Disconnect with Modbus slave and release the master.
        Required parameter:
        Parameter name     Type     Description
        index     int     master index
        """
        string = "ModbusClose({:d})".format(index)
        return self.sendRecvMsg(string)

    def GetInBits(self, index, addr, count):
        """
        读取Modbus从站触点寄存器（离散输⼊）地址的值。
        必选参数
        参数名 类型 说明
        index int 创建主站时返回的主站索引
        addr int 触点寄存器起始地址
        count int 连续读取触点寄存器的值的数量。取值范围：[1, 16]
        Read the contact register (discrete input) value from the Modbus slave.
        Required parameter:
        Parameter name     Type     Description
        index     int     master index
        addr     int     starting address of the contact register
        count     int     number of contact registers Range: [1, 16].
        """
        string = "GetInBits({:d},{:d},{:d})".format(index, addr, count)
        return self.sendRecvMsg(string)

    def GetInRegs(self, index, addr, count, valType=""):
        """
        按照指定的数据类型，读取Modbus从站输⼊寄存器地址的值。
        必选参数
        参数名 类型 说明
        index int 创建主站时返回的主站索引
        addr int 输⼊寄存器起始地址
        count int 连续读取输⼊寄存器的值的数量。取值范围：[1, 4]
        可选参数
        参数名 类型 说明
        valType string
        读取的数据类型：
        U16：16位⽆符号整数（2个字节，占⽤1个寄存器）；
        U32：32位⽆符号整数（4个字节，占⽤2个寄存器）
        F32：32位单精度浮点数（4个字节，占⽤2个寄存器）
        F64：64位双精度浮点数（8个字节，占⽤4个寄存器）
        默认为U16
        Read the input register value with the specified data type from the Modbus slave.
        Required parameter:
        Parameter name     Type     Description
        index     int     master index
        addr     int     starting address of the input register
        count     int     number of input registers Range: [1, 4].
        Optional parameter:
        Parameter name     Type     Description
        valType string
        Data type:
        U16: 16-bit unsigned integer (two bytes, occupy one register)
        U32: 32-bit unsigned integer (four bytes, occupy two register).
        F32: 32-bit single-precision floating-point number (four bytes, occupy two registers)
        F64: 64-bit double-precision floating-point number (eight bytes, occupy four registers)
        U16 by default.
        """
        string = "GetInRegs({:d},{:d},{:d}".format(index, addr, count)
        params = []
        if valType != "":
            params.append("{:s}".format(valType))
        for ii in params:
            string = string + "," + ii
        string = string + ")"
        return self.sendRecvMsg(string)

    def GetCoils(self, index, addr, count):
        """
        读取Modbus从站线圈寄存器地址的值。
        必选参数
        参数名 类型 说明
        index int 创建主站时返回的主站索引
        addr int 线圈寄存器起始地址
        count int 连续读取线圈寄存器的值的数量。取值范围：[1, 16]
        Read the coil register value from the Modbus slave.
        Required parameter:
        Parameter name     Type     Description
        index     int     master index
        addr     int     starting address of the coil register
        count     int     number of coil registers Range: [1, 16].
        """
        string = "GetCoils({:d},{:d},{:d})".format(index, addr, count)
        return self.sendRecvMsg(string)

    def SetCoils(self, index, addr, count, valTab):
        """
        描述
        将指定的值写⼊线圈寄存器指定的地址。
        必选参数
        参数名 类型 说明
        index int 创建主站时返回的主站索引
        addr int 线圈寄存器起始地址
        count int 连续写⼊线圈寄存器的值的数量。取值范围：[1, 16]
        valTab string 要写⼊的值，数量与count相同
        返回
        ErrorID,{},SetCoils(index,addr,count,valTab);
        ⽰例
        SetCoils(0,1000,3,{1,0,1})
        从地址为1000的线圈寄存器开始连续写⼊3个值，分别为1，0，1。
        Description
        Write the specified value to the specified address of coil register.
        Required parameter:
        Parameter name     Type     Description
        index     int     master index
        addr     int     starting address of the coil register
        count     int     number of values to be written to the coil register. Range: [1, 16].
        valTab     string     values to be written to the register (number of values equals to count)
        Return
        ErrorID,{},SetCoils(index,addr,count,valTab);
        Example
        SetCoils(0,1000,3,{1,0,1})
        Write three values (1 , 0, 1) to the coil register starting from address 1000.
        """
        string = "SetCoils({:d},{:d},{:d},{:s})".format(index, addr, count, valTab)
        return self.sendRecvMsg(string)

    def GetHoldRegs(self, index, addr, count, valType=""):
        """
        按照指定的数据类型，读取Modbus从站保持寄存器地址的值。
        必选参数
        参数名 类型 说明
        index int 创建主站时返回的主站索引
        addr int 保持寄存器起始地址
        count int 连续读取保持寄存器的值的数量。取值范围：[1, 4]
        可选参数
        参数名 类型 说明
        valType string
        读取的数据类型：
        U16：16位⽆符号整数（2个字节，占⽤1个寄存器）；
        U32：32位⽆符号整数（4个字节，占⽤2个寄存器）
        F32：32位单精度浮点数（4个字节，占⽤2个寄存器）
        F64：64位双精度浮点数（8个字节，占⽤4个寄存器）
        默认为U16
        Write the specified value according to the specified data type to the specified address of holding register.
        Required parameter:
        Parameter name     Type     Description
        index     int     master index
        addr     int     starting address of the holding register
        count     int     number of values to be written to the holding register. Range: [1, 4].
        Optional parameter:
        Parameter name     Type     Description
        valType string
        Data type:
        U16: 16-bit unsigned integer (two bytes, occupy one register)
        U32: 32-bit unsigned integer (four bytes, occupy two register)
        F32: 32-bit single-precision floating-point number (four bytes, occupy two registers)
        F64: 64-bit double-precision floating-point number (eight bytes, occupy four registers)
        U16 by default.
        """
        string = "GetHoldRegs({:d},{:d},{:d}".format(index, addr, count)
        params = []
        if valType != "":
            params.append("{:s}".format(valType))
        for ii in params:
            string = string + "," + ii
        string = string + ")"
        return self.sendRecvMsg(string)

    def SetHoldRegs(self, index, addr, count, valTab, valType=""):
        """
        将指定的值以指定的数据类型写⼊Modbus从站保持寄存器指定的地址。
        必选参数
        参数名 类型 说明
        index int 创建主站时返回的主站索引
        addr int 保持寄存器起始地址
        count int 连续写⼊保持寄存器的值的数量。取值范围：[1, 4]
        valTab string 要写⼊的值，数量与count相同。
        可选参数
        参数名 类型 说明
        valType string
        写⼊的数据类型：
        U16：16位⽆符号整数（2个字节，占⽤1个寄存器）；
        U32：32位⽆符号整数（4个字节，占⽤2个寄存器）
        F32：32位单精度浮点数（4个字节，占⽤2个寄存器）
        F64：64位双精度浮点数（8个字节，占⽤4个寄存器）
        默认为U16
        Write the specified value with specified data type to the specified address of holding register.
        Required parameter:
        Parameter name     Type     Description
        index     int     master index
        addr     int     starting address of the holding register
        count     int     number of values to be written to the holding register. Range: [1, 4].
        valTab     string     values to be written to the register (number of values equals to count).
        Optional parameter:
        Parameter name     Type     Description
        valType string
        Data type:
        U16: 16-bit unsigned integer (two bytes, occupy one register)
        U32: 32-bit unsigned integer (four bytes, occupy two register)
        F32: 32-bit single-precision floating-point number (four bytes, occupy two registers)
        F64: 64-bit double-precision floating-point number (eight bytes, occupy four registers)
        U16 by default.
        """
        string = "SetHoldRegs({:d},{:d},{:d},{:s}".format(index, addr, count, valTab)
        params = []
        if valType != "":
            params.append("{:s}".format(valType))
        for ii in params:
            string = string + "," + ii
        string = string + ")"
        return self.sendRecvMsg(string)

    ########################################################################

    def GetInputBool(self, address):
        """
        获取输⼊寄存器指定地址的bool类型的数值。
        必选参数
        参数名 类型 说明
        address int 寄存器地址，取值范围[0-63]
        Get the value in bool type from the specified address of input register.
        Required parameter:
        Parameter name     Type     Description
        address     int     register address, range: [0-63]
        """
        string = "GetInputBool({:d})".format(address)
        return self.sendRecvMsg(string)

    def GetInputInt(self, address):
        """
        获取输⼊寄存器指定地址的int类型的数值。
        必选参数
        参数名 类型 说明
        address int 寄存器地址，取值范围[0-23]
        Get the value in int type from the specified address of input register.
        Required parameter:
        Parameter name     Type     Description
        address     int     register address, range: [0-23]
        """
        string = "GetInputInt({:d})".format(address)
        return self.sendRecvMsg(string)

    def GetInputFloat(self, address):
        """
        获取输⼊寄存器指定地址的float类型的数值。
        必选参数
        参数名 类型 说明
        address int 寄存器地址，取值范围[0-23]
        Get the value in float type from the specified address of input register.
        Required parameter:
        Parameter name     Type     Description
        address     int     register address, range: [0-23]
        """
        string = "GetInputFloat({:d})".format(address)
        return self.sendRecvMsg(string)

    def GetOutputBool(self, address):
        """
        获取输出寄存器指定地址的bool类型的数值。
        必选参数
        参数名 类型 说明
        address int 寄存器地址，取值范围[0-63]
        Get the value in bool type from the specified address of output register.
        Required parameter:
        Parameter name     Type     Description
        address     int     register address, range: [0-63]
        """
        string = "GetOutputBool({:d})".format(address)
        return self.sendRecvMsg(string)

    def GetOutputInt(self, address):
        """
        获取输出寄存器指定地址的int类型的数值。
        必选参数
        参数名 类型 说明
        address int 寄存器地址，取值范围[0-23]
        Get the value in int type from the specified address of output register.
        Required parameter:
        Parameter name     Type     Description
        address     int     register address, range: [0-23]
        """
        string = "GetOutputInt({:d})".format(address)
        return self.sendRecvMsg(string)

    def GetOutputFloat(self, address):
        """
        获取输出寄存器指定地址的float类型的数值。
        必选参数
        参数名 类型 说明
        address int 寄存器地址，取值范围[0-23]
        Get the value in float type from the specified address of output register.
        Required parameter:
        Parameter name     Type     Description
        address     int     register address, range: [0-23]
        """
        string = "GetInputFloat({:d})".format(address)
        return self.sendRecvMsg(string)

    def SetOutputBool(self, address, value):
        """
        设置输出寄存器指定地址的bool类型的数值。
        必选参数
        参数名 类型 说明
        address int 寄存器地址，取值范围[0-63]
        value int 要设置的值，⽀持0或1
        Set the value in bool type at the specified address of output register.
        Required parameter:
        Parameter name     Type     Description
        address     int     register address, range: [0-63]
        value     int     value to be set (0 or 1)
        """
        string = "GetInputFloat({:d},{:d})".format(address, value)
        return self.sendRecvMsg(string)

    def SetOutputInt(self, address, value):
        """
        设置输出寄存器指定地址的int类型的数值。
        必选参数
        参数名 类型 说明
        address int 寄存器地址，取值范围[0-23]
        value int 要设置的值，⽀持整型数
        Set the value in int type at the specified address of output register.
        Required parameter:
        Parameter name     Type     Description
        address     int     register address, range: [0-23]
        value     int     value to be set (integer)
        """
        string = "SetOutputInt({:d},{:d})".format(address, value)
        return self.sendRecvMsg(string)

    def SetOutputFloat(self, address, value):
        """
        设置输出寄存器指定地址的int类型的数值。
        必选参数
        参数名 类型 说明
        address int 寄存器地址，取值范围[0-23]
        value int 要设置的值，⽀持整型数
        Set the value in int type at the specified address of output register.
        Required parameter:
        Parameter name     Type     Description
        address     int     register address, range: [0-23]
        value     int     value to be set (integer)
        """
        string = "SetOutputFloat({:d},{:d})".format(address, value)
        return self.sendRecvMsg(string)

    #######################################################################

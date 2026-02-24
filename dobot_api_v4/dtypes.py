"""
Feedback data types for Dobot V4 protocol.

This module defines the numpy dtype for parsing binary feedback packets
and a frozen dataclass for convenient typed access to feedback fields.
"""

import numpy as np
from dataclasses import dataclass
from typing import Tuple

# ---------------------------------------------------------------------------
# Numpy dtype for the 1440-byte feedback packet
# ---------------------------------------------------------------------------

FeedbackDtype = np.dtype(
    [
        ("len", np.uint16),
        ("reserve", np.byte, (6,)),
        ("digital_inputs", np.uint64),
        ("digital_outputs", np.uint64),
        ("robot_mode", np.uint64),
        ("time_stamp", np.uint64),
        ("run_time", np.uint64),
        ("test_value", np.uint64),
        ("reserve2", np.byte, (8,)),
        ("speed_scaling", np.float64),
        ("reserve3", np.byte, (16,)),
        ("v_robot", np.float64),
        ("i_robot", np.float64),
        ("program_state", np.float64),
        ("safety_o_in", np.uint16),
        ("safety_o_out", np.uint16),
        ("reserve4", np.byte, (76,)),
        ("q_target", np.float64, (6,)),
        ("qd_target", np.float64, (6,)),
        ("qdd_target", np.float64, (6,)),
        ("i_target", np.float64, (6,)),
        ("m_target", np.float64, (6,)),
        ("q_actual", np.float64, (6,)),
        ("qd_actual", np.float64, (6,)),
        ("i_actual", np.float64, (6,)),
        ("actual_tcp_force", np.float64, (6,)),
        ("tool_vector_actual", np.float64, (6,)),
        ("tcp_speed_actual", np.float64, (6,)),
        ("tcp_force", np.float64, (6,)),
        ("tool_vector_target", np.float64, (6,)),
        ("tcp_speed_target", np.float64, (6,)),
        ("motor_temperatures", np.float64, (6,)),
        ("joint_modes", np.float64, (6,)),
        ("v_actual", np.float64, (6,)),
        ("hand_type", np.byte, (4,)),
        ("user", np.byte),
        ("tool", np.byte),
        ("run_queued_cmd", np.byte),
        ("pause_cmd_flag", np.byte),
        ("velocity_ratio", np.byte),
        ("acceleration_ratio", np.byte),
        ("reserve5", np.byte),
        ("xyz_velocity_ratio", np.byte),
        ("r_velocity_ratio", np.byte),
        ("xyz_acceleration_ratio", np.byte),
        ("r_acceleration_ratio", np.byte),
        ("reserve6", np.byte, (2,)),
        ("brake_status", np.byte),
        ("enable_status", np.byte),
        ("drag_status", np.byte),
        ("running_status", np.byte),
        ("error_status", np.byte),
        ("jog_status_cr", np.byte),
        ("cr_robot_type", np.byte),
        ("drag_button_signal", np.byte),
        ("enable_button_signal", np.byte),
        ("record_button_signal", np.byte),
        ("reappear_button_signal", np.byte),
        ("jaw_button_signal", np.byte),
        ("six_force_online", np.byte),
        ("collision_state", np.byte),
        ("arm_approach_state", np.byte),
        ("j4_approach_state", np.byte),
        ("j5_approach_state", np.byte),
        ("j6_approach_state", np.byte),
        ("reserve7", np.byte, (61,)),
        ("vibration_dis_z", np.float64),
        ("current_command_id", np.uint64),
        ("m_actual", np.float64, (6,)),
        ("load", np.float64),
        ("center_x", np.float64),
        ("center_y", np.float64),
        ("center_z", np.float64),
        ("user_coords", np.float64, (6,)),
        ("tool_coords", np.float64, (6,)),
        ("reserve8", np.byte, (8,)),
        ("six_force_value", np.float64, (6,)),
        ("target_quaternion", np.float64, (4,)),
        ("actual_quaternion", np.float64, (4,)),
        ("auto_manual_mode", np.uint16),
        ("export_status", np.uint16),
        ("safety_state", np.byte),
        ("reserve9", np.byte, (19,)),
    ]
)

assert (
    FeedbackDtype.itemsize == 1440
), f"FeedbackDtype size mismatch: expected 1440, got {FeedbackDtype.itemsize}"


# ---------------------------------------------------------------------------
# Mapping from original protocol field names to new snake_case names
# ---------------------------------------------------------------------------

PROTOCOL_FIELD_MAP: dict[str, str] = {
    "DigitalInputs": "digital_inputs",
    "DigitalOutputs": "digital_outputs",
    "RobotMode": "robot_mode",
    "TimeStamp": "time_stamp",
    "RunTime": "run_time",
    "TestValue": "test_value",
    "SpeedScaling": "speed_scaling",
    "VRobot": "v_robot",
    "IRobot": "i_robot",
    "ProgramState": "program_state",
    "SafetyOIn": "safety_o_in",
    "SafetyOOut": "safety_o_out",
    "QTarget": "q_target",
    "QDTarget": "qd_target",
    "QDDTarget": "qdd_target",
    "ITarget": "i_target",
    "MTarget": "m_target",
    "QActual": "q_actual",
    "QDActual": "qd_actual",
    "IActual": "i_actual",
    "ActualTCPForce": "actual_tcp_force",
    "ToolVectorActual": "tool_vector_actual",
    "TCPSpeedActual": "tcp_speed_actual",
    "TCPForce": "tcp_force",
    "ToolVectorTarget": "tool_vector_target",
    "TCPSpeedTarget": "tcp_speed_target",
    "MotorTemperatures": "motor_temperatures",
    "JointModes": "joint_modes",
    "VActual": "v_actual",
    "HandType": "hand_type",
    "User": "user",
    "Tool": "tool",
    "RunQueuedCmd": "run_queued_cmd",
    "PauseCmdFlag": "pause_cmd_flag",
    "VelocityRatio": "velocity_ratio",
    "AccelerationRatio": "acceleration_ratio",
    "XYZVelocityRatio": "xyz_velocity_ratio",
    "RVelocityRatio": "r_velocity_ratio",
    "XYZAccelerationRatio": "xyz_acceleration_ratio",
    "RAccelerationRatio": "r_acceleration_ratio",
    "BrakeStatus": "brake_status",
    "EnableStatus": "enable_status",
    "DragStatus": "drag_status",
    "RunningStatus": "running_status",
    "ErrorStatus": "error_status",
    "JogStatusCR": "jog_status_cr",
    "CRRobotType": "cr_robot_type",
    "DragButtonSignal": "drag_button_signal",
    "EnableButtonSignal": "enable_button_signal",
    "RecordButtonSignal": "record_button_signal",
    "ReappearButtonSignal": "reappear_button_signal",
    "JawButtonSignal": "jaw_button_signal",
    "SixForceOnline": "six_force_online",
    "CollisionState": "collision_state",
    "ArmApproachState": "arm_approach_state",
    "J4ApproachState": "j4_approach_state",
    "J5ApproachState": "j5_approach_state",
    "J6ApproachState": "j6_approach_state",
    "VibrationDisZ": "vibration_dis_z",
    "CurrentCommandId": "current_command_id",
    "MActual": "m_actual",
    "Load": "load",
    "CenterX": "center_x",
    "CenterY": "center_y",
    "CenterZ": "center_z",
    "UserValue[6]": "user_coords",
    "ToolValue[6]": "tool_coords",
    "SixForceValue": "six_force_value",
    "TargetQuaternion": "target_quaternion",
    "ActualQuaternion": "actual_quaternion",
    "AutoManualMode": "auto_manual_mode",
    "ExportStatus": "export_status",
    "SafetyState": "safety_state",
}


# ---------------------------------------------------------------------------
# Frozen dataclass for typed access
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class FeedbackData:
    """Typed, immutable representation of one feedback packet.

    All scalar protocol fields become ``int`` or ``float``.
    Multi-element fields become ``tuple[float, ...]`` or ``tuple[int, ...]``.
    Reserve/padding fields are excluded.
    """

    # Scalars – unsigned integers
    len: int
    digital_inputs: int
    digital_outputs: int
    robot_mode: int
    time_stamp: int
    run_time: int
    test_value: int

    # Scalars – floats
    speed_scaling: float
    v_robot: float
    i_robot: float
    program_state: float

    # Scalars – unsigned 16-bit
    safety_o_in: int
    safety_o_out: int

    # 6-element float arrays
    q_target: Tuple[float, ...]
    qd_target: Tuple[float, ...]
    qdd_target: Tuple[float, ...]
    i_target: Tuple[float, ...]
    m_target: Tuple[float, ...]
    q_actual: Tuple[float, ...]
    qd_actual: Tuple[float, ...]
    i_actual: Tuple[float, ...]
    actual_tcp_force: Tuple[float, ...]
    tool_vector_actual: Tuple[float, ...]
    tcp_speed_actual: Tuple[float, ...]
    tcp_force: Tuple[float, ...]
    tool_vector_target: Tuple[float, ...]
    tcp_speed_target: Tuple[float, ...]
    motor_temperatures: Tuple[float, ...]
    joint_modes: Tuple[float, ...]
    v_actual: Tuple[float, ...]

    # Small scalars (byte-sized)
    hand_type: Tuple[int, ...]
    user: int
    tool: int
    run_queued_cmd: int
    pause_cmd_flag: int
    velocity_ratio: int
    acceleration_ratio: int
    xyz_velocity_ratio: int
    r_velocity_ratio: int
    xyz_acceleration_ratio: int
    r_acceleration_ratio: int
    brake_status: int
    enable_status: int
    drag_status: int
    running_status: int
    error_status: int
    jog_status_cr: int
    cr_robot_type: int
    drag_button_signal: int
    enable_button_signal: int
    record_button_signal: int
    reappear_button_signal: int
    jaw_button_signal: int
    six_force_online: int
    collision_state: int
    arm_approach_state: int
    j4_approach_state: int
    j5_approach_state: int
    j6_approach_state: int

    # Larger scalars
    vibration_dis_z: float
    current_command_id: int

    # 6-element float arrays (continued)
    m_actual: Tuple[float, ...]
    load: float
    center_x: float
    center_y: float
    center_z: float
    user_coords: Tuple[float, ...]
    tool_coords: Tuple[float, ...]
    six_force_value: Tuple[float, ...]

    # 4-element float arrays (quaternions)
    target_quaternion: Tuple[float, ...]
    actual_quaternion: Tuple[float, ...]

    # Final scalars
    auto_manual_mode: int
    export_status: int
    safety_state: int

    @classmethod
    def from_numpy(cls, arr: np.ndarray) -> "FeedbackData":
        """Create a ``FeedbackData`` from a numpy structured array.

        Args:
            arr: Array with dtype ``FeedbackDtype``, typically shape ``(1,)``.

        Returns:
            A new frozen ``FeedbackData`` instance.
        """
        row = arr[0]
        return cls(
            len=int(row["len"]),
            digital_inputs=int(row["digital_inputs"]),
            digital_outputs=int(row["digital_outputs"]),
            robot_mode=int(row["robot_mode"]),
            time_stamp=int(row["time_stamp"]),
            run_time=int(row["run_time"]),
            test_value=int(row["test_value"]),
            speed_scaling=float(row["speed_scaling"]),
            v_robot=float(row["v_robot"]),
            i_robot=float(row["i_robot"]),
            program_state=float(row["program_state"]),
            safety_o_in=int(row["safety_o_in"]),
            safety_o_out=int(row["safety_o_out"]),
            q_target=tuple(row["q_target"].tolist()),
            qd_target=tuple(row["qd_target"].tolist()),
            qdd_target=tuple(row["qdd_target"].tolist()),
            i_target=tuple(row["i_target"].tolist()),
            m_target=tuple(row["m_target"].tolist()),
            q_actual=tuple(row["q_actual"].tolist()),
            qd_actual=tuple(row["qd_actual"].tolist()),
            i_actual=tuple(row["i_actual"].tolist()),
            actual_tcp_force=tuple(row["actual_tcp_force"].tolist()),
            tool_vector_actual=tuple(row["tool_vector_actual"].tolist()),
            tcp_speed_actual=tuple(row["tcp_speed_actual"].tolist()),
            tcp_force=tuple(row["tcp_force"].tolist()),
            tool_vector_target=tuple(row["tool_vector_target"].tolist()),
            tcp_speed_target=tuple(row["tcp_speed_target"].tolist()),
            motor_temperatures=tuple(row["motor_temperatures"].tolist()),
            joint_modes=tuple(row["joint_modes"].tolist()),
            v_actual=tuple(row["v_actual"].tolist()),
            hand_type=tuple(int(x) for x in row["hand_type"].tolist()),
            user=int(row["user"]),
            tool=int(row["tool"]),
            run_queued_cmd=int(row["run_queued_cmd"]),
            pause_cmd_flag=int(row["pause_cmd_flag"]),
            velocity_ratio=int(row["velocity_ratio"]),
            acceleration_ratio=int(row["acceleration_ratio"]),
            xyz_velocity_ratio=int(row["xyz_velocity_ratio"]),
            r_velocity_ratio=int(row["r_velocity_ratio"]),
            xyz_acceleration_ratio=int(row["xyz_acceleration_ratio"]),
            r_acceleration_ratio=int(row["r_acceleration_ratio"]),
            brake_status=int(row["brake_status"]),
            enable_status=int(row["enable_status"]),
            drag_status=int(row["drag_status"]),
            running_status=int(row["running_status"]),
            error_status=int(row["error_status"]),
            jog_status_cr=int(row["jog_status_cr"]),
            cr_robot_type=int(row["cr_robot_type"]),
            drag_button_signal=int(row["drag_button_signal"]),
            enable_button_signal=int(row["enable_button_signal"]),
            record_button_signal=int(row["record_button_signal"]),
            reappear_button_signal=int(row["reappear_button_signal"]),
            jaw_button_signal=int(row["jaw_button_signal"]),
            six_force_online=int(row["six_force_online"]),
            collision_state=int(row["collision_state"]),
            arm_approach_state=int(row["arm_approach_state"]),
            j4_approach_state=int(row["j4_approach_state"]),
            j5_approach_state=int(row["j5_approach_state"]),
            j6_approach_state=int(row["j6_approach_state"]),
            vibration_dis_z=float(row["vibration_dis_z"]),
            current_command_id=int(row["current_command_id"]),
            m_actual=tuple(row["m_actual"].tolist()),
            load=float(row["load"]),
            center_x=float(row["center_x"]),
            center_y=float(row["center_y"]),
            center_z=float(row["center_z"]),
            user_coords=tuple(row["user_coords"].tolist()),
            tool_coords=tuple(row["tool_coords"].tolist()),
            six_force_value=tuple(row["six_force_value"].tolist()),
            target_quaternion=tuple(row["target_quaternion"].tolist()),
            actual_quaternion=tuple(row["actual_quaternion"].tolist()),
            auto_manual_mode=int(row["auto_manual_mode"]),
            export_status=int(row["export_status"]),
            safety_state=int(row["safety_state"]),
        )

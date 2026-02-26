"""Unit tests for dobot_api_v4.commands._motion_mixin module."""

import pytest


@pytest.mark.unit
class TestMotionMixin:
    """Tests verifying exact protocol strings for motion commands."""

    # ------------------------------------------------------------------
    # MovJ
    # ------------------------------------------------------------------

    def test_mov_j_pose_mode(self, mock_dashboard):
        dashboard, sent = mock_dashboard
        dashboard.mov_j(100, 200, 300, 0, 90, 0, coordinate_mode=0)
        cmd = sent[-1]
        assert cmd.startswith("MovJ(pose={")
        assert "100.000000" in cmd
        assert "200.000000" in cmd

    def test_mov_j_joint_mode(self, mock_dashboard):
        dashboard, sent = mock_dashboard
        dashboard.mov_j(10, 20, 30, 40, 50, 60, coordinate_mode=1)
        cmd = sent[-1]
        assert cmd.startswith("MovJ(joint={")

    def test_mov_j_invalid_coordinate_mode(self, mock_dashboard):
        dashboard, sent = mock_dashboard
        with pytest.raises(ValueError, match="coordinateMode"):
            dashboard.mov_j(0, 0, 0, 0, 0, 0, coordinate_mode=2)

    def test_mov_j_with_optional_params(self, mock_dashboard):
        dashboard, sent = mock_dashboard
        dashboard.mov_j(0, 0, 0, 0, 0, 0, coordinate_mode=0, user=0, tool=0, v=50)
        cmd = sent[-1]
        assert "user=0" in cmd
        assert "tool=0" in cmd
        assert "v=50" in cmd

    # ------------------------------------------------------------------
    # MovL
    # ------------------------------------------------------------------

    def test_mov_l_pose_mode(self, mock_dashboard):
        dashboard, sent = mock_dashboard
        dashboard.mov_l(100, 200, 300, 0, 90, 0, coordinate_mode=0)
        cmd = sent[-1]
        assert cmd.startswith("MovL(pose={")

    def test_mov_l_joint_mode(self, mock_dashboard):
        dashboard, sent = mock_dashboard
        dashboard.mov_l(10, 20, 30, 40, 50, 60, coordinate_mode=1)
        cmd = sent[-1]
        assert cmd.startswith("MovL(joint={")

    def test_mov_l_with_speed(self, mock_dashboard):
        dashboard, sent = mock_dashboard
        dashboard.mov_l(0, 0, 0, 0, 0, 0, coordinate_mode=0, speed=50)
        cmd = sent[-1]
        assert "speed=50" in cmd

    # ------------------------------------------------------------------
    # ServoJ
    # ------------------------------------------------------------------

    def test_servo_j(self, mock_dashboard):
        dashboard, sent = mock_dashboard
        dashboard.servo_j(10, 20, 30, 40, 50, 60)
        cmd = sent[-1]
        assert cmd.startswith("ServoJ(")
        assert "10.000000" in cmd

    def test_servo_j_custom_time(self, mock_dashboard):
        dashboard, sent = mock_dashboard
        dashboard.servo_j(0, 0, 0, 0, 0, 0, t=0.016)
        cmd = sent[-1]
        assert "ServoJ(" in cmd

    # ------------------------------------------------------------------
    # ServoP
    # ------------------------------------------------------------------

    def test_servo_p(self, mock_dashboard):
        dashboard, sent = mock_dashboard
        dashboard.servo_p(100, 200, 300, 0, 90, 0)
        cmd = sent[-1]
        assert cmd.startswith("ServoP(")

    # ------------------------------------------------------------------
    # MoveJog
    # ------------------------------------------------------------------

    def test_move_jog_no_params(self, mock_dashboard):
        dashboard, sent = mock_dashboard
        dashboard.move_jog()
        assert sent[-1] == "MoveJog()"

    def test_move_jog_with_axis(self, mock_dashboard):
        dashboard, sent = mock_dashboard
        dashboard.move_jog(axis_id="j1+")
        assert "MoveJog(j1+" in sent[-1]

    # ------------------------------------------------------------------
    # Arc
    # ------------------------------------------------------------------

    def test_arc(self, mock_dashboard):
        dashboard, sent = mock_dashboard
        dashboard.arc(
            10,
            20,
            30,
            0,
            0,
            0,  # via point
            40,
            50,
            60,
            0,
            0,
            0,  # target point
            coordinate_mode=0,
        )
        cmd = sent[-1]
        assert cmd.startswith("Arc(pose={")

    # ------------------------------------------------------------------
    # Circle
    # ------------------------------------------------------------------

    def test_circle(self, mock_dashboard):
        dashboard, sent = mock_dashboard
        dashboard.circle(
            10,
            20,
            30,
            0,
            0,
            0,
            40,
            50,
            60,
            0,
            0,
            0,
            count=1,
            coordinate_mode=0,
        )
        cmd = sent[-1]
        assert cmd.startswith("Circle(pose={")

    # ------------------------------------------------------------------
    # RelMovJTool / RelMovLTool
    # ------------------------------------------------------------------

    def test_rel_mov_j_tool(self, mock_dashboard):
        dashboard, sent = mock_dashboard
        dashboard.rel_mov_j_tool(10, 20, 30, 0, 0, 0)
        cmd = sent[-1]
        assert cmd.startswith("RelMovJTool(")

    def test_rel_mov_l_tool(self, mock_dashboard):
        dashboard, sent = mock_dashboard
        dashboard.rel_mov_l_tool(10, 20, 30, 0, 0, 0)
        cmd = sent[-1]
        assert cmd.startswith("RelMovLTool(")

    # ------------------------------------------------------------------
    # RelMovJUser / RelMovLUser
    # ------------------------------------------------------------------

    def test_rel_mov_j_user(self, mock_dashboard):
        dashboard, sent = mock_dashboard
        dashboard.rel_mov_j_user(10, 20, 30, 0, 0, 0)
        cmd = sent[-1]
        assert cmd.startswith("RelMovJUser(")

    def test_rel_mov_l_user(self, mock_dashboard):
        dashboard, sent = mock_dashboard
        dashboard.rel_mov_l_user(10, 20, 30, 0, 0, 0)
        cmd = sent[-1]
        assert cmd.startswith("RelMovLUser(")

    # ------------------------------------------------------------------
    # RelJointMovJ
    # ------------------------------------------------------------------

    def test_rel_joint_mov_j(self, mock_dashboard):
        dashboard, sent = mock_dashboard
        dashboard.rel_joint_mov_j(1, 2, 3, 4, 5, 6)
        cmd = sent[-1]
        assert cmd.startswith("RelJointMovJ(")

    # ------------------------------------------------------------------
    # GetStartPose / StartPath
    # ------------------------------------------------------------------

    def test_get_start_pose(self, mock_dashboard):
        dashboard, sent = mock_dashboard
        dashboard.get_start_pose("trace_name")
        assert sent[-1] == "GetStartPose(trace_name)"

    def test_start_path(self, mock_dashboard):
        dashboard, sent = mock_dashboard
        dashboard.start_path("trace_name")
        assert "StartPath(trace_name" in sent[-1]

    # ------------------------------------------------------------------
    # MovLIO / MovJIO
    # ------------------------------------------------------------------

    def test_mov_l_io(self, mock_dashboard):
        dashboard, sent = mock_dashboard
        dashboard.mov_l_io(
            100,
            200,
            300,
            0,
            90,
            0,
            coordinate_mode=0,
            mode=0,
            distance=50,
            index=1,
            status=1,
        )
        cmd = sent[-1]
        assert cmd.startswith("MovLIO(pose={")

    def test_mov_j_io(self, mock_dashboard):
        dashboard, sent = mock_dashboard
        dashboard.mov_j_io(
            100,
            200,
            300,
            0,
            90,
            0,
            coordinate_mode=0,
            mode=0,
            distance=80,
            index=2,
            status=1,
        )
        cmd = sent[-1]
        assert cmd.startswith("MovJIO(pose={")


@pytest.mark.unit
class TestMotionMixinBackwardCompat:
    """Verify PascalCase aliases exist."""

    def test_mov_j_alias(self, mock_dashboard):
        dashboard, sent = mock_dashboard
        dashboard.MovJ(0, 0, 0, 0, 0, 0, 0)
        assert "MovJ(" in sent[-1]

    def test_mov_l_alias(self, mock_dashboard):
        dashboard, sent = mock_dashboard
        dashboard.MovL(0, 0, 0, 0, 0, 0, 0)
        assert "MovL(" in sent[-1]

    def test_move_jog_alias(self, mock_dashboard):
        dashboard, sent = mock_dashboard
        dashboard.MoveJog()
        assert sent[-1] == "MoveJog()"

    def test_servo_j_alias(self, mock_dashboard):
        dashboard, sent = mock_dashboard
        dashboard.ServoJ(0, 0, 0, 0, 0, 0)
        assert "ServoJ(" in sent[-1]

"""Unit tests for dobot_api_v4.commands._parse module."""

import pytest

from dobot_api_v4.commands._parse import (
    DobotApiError,
    parse_ack,
    parse_error_ids,
    parse_int,
    parse_pose,
    parse_response,
)
from dobot_api_v4.dtypes import Pose

# ── parse_response (low-level) ──────────────────────────────────────────────


@pytest.mark.unit
class TestParseResponse:
    """Tests for the low-level parse_response function."""

    def test_3field_returns_command_id_and_payload(self):
        cid, payload = parse_response("0,1,5;")
        assert cid == 1
        assert payload == "5"

    def test_3field_trailing_whitespace(self):
        cid, payload = parse_response("0,42,;  \n")
        assert cid == 42
        assert payload == ""

    def test_v4_brace_returns_zero_command_id(self):
        cid, payload = parse_response("0,{},EnableRobot();")
        assert cid == 0
        assert payload == ""

    def test_v4_brace_with_payload(self):
        cid, payload = parse_response("0,{5},RobotMode();")
        assert cid == 0
        assert payload == "5"

    def test_legacy_brace(self):
        cid, payload = parse_response("0,{101,202};")
        assert cid == 0
        assert payload == "101,202"

    def test_unrecognized_format_raises(self):
        with pytest.raises(ValueError, match="Unrecognized"):
            parse_response("garbage data")

    def test_empty_string_raises(self):
        with pytest.raises(ValueError):
            parse_response("")


# ── parse_ack ────────────────────────────────────────────────────────────────


@pytest.mark.unit
class TestParseAck:
    """Tests for parse_ack."""

    def test_simple_ack(self):
        assert parse_ack("0,1,;") is None

    def test_v4_brace_ack(self):
        assert parse_ack("0,{},EnableRobot();") is None

    def test_no_semicolon(self):
        assert parse_ack("0,10,") is None

    def test_nonzero_error_raises(self):
        with pytest.raises(DobotApiError) as exc_info:
            parse_ack("1,10,some error;")
        assert exc_info.value.error_code == 1

    def test_v4_negative_error_raises(self):
        with pytest.raises(DobotApiError) as exc_info:
            parse_ack("-1,{},EnableRobot();")
        assert exc_info.value.error_code == -1


# ── parse_int ────────────────────────────────────────────────────────────────


@pytest.mark.unit
class TestParseInt:
    """Tests for parse_int."""

    def test_int_value(self):
        assert parse_int("0,1,5;") == 5

    def test_empty_payload_defaults_to_zero(self):
        assert parse_int("0,1,;") == 0

    def test_large_value(self):
        assert parse_int("0,99,12345;") == 12345

    def test_v4_brace_int(self):
        assert parse_int("0,{5},RobotMode();") == 5

    def test_v4_brace_queue_id(self):
        assert parse_int("0,{1},MovL(pose={-500,100,200,150,0,90});") == 1

    def test_v4_brace_large_queue_id(self):
        assert parse_int("0,{42},JointMovJ();") == 42


# ── parse_pose ───────────────────────────────────────────────────────────────


@pytest.mark.unit
class TestParsePose:
    """Tests for parse_pose."""

    def test_3field_six_floats(self):
        pose = parse_pose("0,1,100.5,200.3,300.1,0.0,90.0,45.0;")
        assert isinstance(pose, Pose)
        assert abs(pose.x - 100.5) < 1e-9
        assert abs(pose.y - 200.3) < 1e-9
        assert abs(pose.z - 300.1) < 1e-9
        assert abs(pose.rx - 0.0) < 1e-9
        assert abs(pose.ry - 90.0) < 1e-9
        assert abs(pose.rz - 45.0) < 1e-9

    def test_negative_values(self):
        pose = parse_pose("0,1,-1.0,-2.0,-3.0,-4.0,-5.0,-6.0;")
        assert pose.x == -1.0

    def test_v4_brace_pose(self):
        raw = "0,{-280.9191,-211.0103,380.6188,-175.6129,2.9980,135.5864},GetPose();"
        pose = parse_pose(raw)
        assert abs(pose.x - (-280.9191)) < 1e-4
        assert abs(pose.y - (-211.0103)) < 1e-4
        assert abs(pose.z - 380.6188) < 1e-4
        assert abs(pose.rx - (-175.6129)) < 1e-4
        assert abs(pose.ry - 2.9980) < 1e-4
        assert abs(pose.rz - 135.5864) < 1e-4

    def test_v4_brace_positive_values(self):
        raw = "0,{100.5,200.3,300.1,0.0,90.0,45.0},GetPose();"
        pose = parse_pose(raw)
        assert abs(pose.x - 100.5) < 1e-9
        assert abs(pose.rz - 45.0) < 1e-9

    def test_insufficient_floats_raises(self):
        with pytest.raises(ValueError, match="requires 6 floats"):
            parse_pose("0,1,1.0,2.0,3.0;")


# ── parse_error_ids ──────────────────────────────────────────────────────────


@pytest.mark.unit
class TestParseErrorIds:
    """Tests for parse_error_ids."""

    def test_with_error_ids(self):
        assert parse_error_ids("0,1,101,202,303;") == (101, 202, 303)

    def test_zeros_filtered(self):
        assert parse_error_ids("0,1,0,101,0,202,0;") == (101, 202)

    def test_all_zeros(self):
        assert parse_error_ids("0,1,0,0,0;") == ()

    def test_empty_payload(self):
        assert parse_error_ids("0,1,;") == ()

    def test_v4_brace_error_ids(self):
        assert parse_error_ids("0,{101,202,303},GetErrorID();") == (101, 202, 303)


# ── DobotApiError ────────────────────────────────────────────────────────────


@pytest.mark.unit
class TestDobotApiError:
    """Tests for error handling."""

    def test_nonzero_error_code_raises(self):
        with pytest.raises(DobotApiError) as exc_info:
            parse_ack("1,10,some error;")
        err = exc_info.value
        assert err.error_code == 1
        assert err.command_id == 10
        assert "1,10,some error;" in err.raw

    def test_error_attributes(self):
        with pytest.raises(DobotApiError) as exc_info:
            parse_ack("3,5,fail;")
        err = exc_info.value
        assert err.error_code == 3
        assert err.command_id == 5

    def test_negative_error_code_3field(self):
        with pytest.raises(DobotApiError) as exc_info:
            parse_ack("-1,5,fail;")
        err = exc_info.value
        assert err.error_code == -1
        assert err.command_id == 5

    def test_brace_error(self):
        with pytest.raises(DobotApiError):
            parse_ack("2,{err};")

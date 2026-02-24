"""Unit tests for dobot_api_v4.responses module."""

import pytest

from dobot_api_v4.responses import (
    AckResponse,
    DobotApiError,
    ErrorIdResponse,
    IntResponse,
    PoseResponse,
    parse_response,
)


@pytest.mark.unit
class TestAckResponse:
    """Tests for parsing AckResponse."""

    def test_simple_ack(self):
        resp = parse_response("0,1,;", AckResponse)
        assert isinstance(resp, AckResponse)
        assert resp.command_id == 1

    def test_trailing_whitespace(self):
        resp = parse_response("0,42,;  \n", AckResponse)
        assert resp.command_id == 42

    def test_no_semicolon(self):
        resp = parse_response("0,10,", AckResponse)
        assert resp.command_id == 10


@pytest.mark.unit
class TestIntResponse:
    """Tests for parsing IntResponse."""

    def test_int_value(self):
        resp = parse_response("0,1,5;", IntResponse)
        assert isinstance(resp, IntResponse)
        assert resp.command_id == 1
        assert resp.value == 5

    def test_empty_payload_defaults_to_zero(self):
        resp = parse_response("0,1,;", IntResponse)
        assert resp.value == 0

    def test_large_value(self):
        resp = parse_response("0,99,12345;", IntResponse)
        assert resp.value == 12345


@pytest.mark.unit
class TestPoseResponse:
    """Tests for parsing PoseResponse."""

    def test_six_floats(self):
        resp = parse_response("0,1,100.5,200.3,300.1,0.0,90.0,45.0;", PoseResponse)
        assert isinstance(resp, PoseResponse)
        assert resp.command_id == 1
        assert abs(resp.x - 100.5) < 1e-9
        assert abs(resp.y - 200.3) < 1e-9
        assert abs(resp.z - 300.1) < 1e-9
        assert abs(resp.rx - 0.0) < 1e-9
        assert abs(resp.ry - 90.0) < 1e-9
        assert abs(resp.rz - 45.0) < 1e-9

    def test_negative_values(self):
        resp = parse_response("0,1,-1.0,-2.0,-3.0,-4.0,-5.0,-6.0;", PoseResponse)
        assert resp.x == -1.0

    def test_insufficient_floats_raises(self):
        with pytest.raises(ValueError, match="requires 6 floats"):
            parse_response("0,1,1.0,2.0,3.0;", PoseResponse)


@pytest.mark.unit
class TestErrorIdResponse:
    """Tests for parsing ErrorIdResponse."""

    def test_with_error_ids(self):
        resp = parse_response("0,1,101,202,303;", ErrorIdResponse)
        assert isinstance(resp, ErrorIdResponse)
        assert resp.error_ids == (101, 202, 303)

    def test_zeros_filtered(self):
        resp = parse_response("0,1,0,101,0,202,0;", ErrorIdResponse)
        assert resp.error_ids == (101, 202)

    def test_all_zeros(self):
        resp = parse_response("0,1,0,0,0;", ErrorIdResponse)
        assert resp.error_ids == ()

    def test_empty_payload(self):
        resp = parse_response("0,1,;", ErrorIdResponse)
        assert resp.error_ids == ()


@pytest.mark.unit
class TestBraceFormat:
    """Tests for the 2-field brace format."""

    def test_brace_ack(self):
        resp = parse_response("0,{};", AckResponse)
        assert resp.command_id == 0

    def test_brace_error_ids(self):
        resp = parse_response("0,{101,202};", ErrorIdResponse)
        assert resp.error_ids == (101, 202)


@pytest.mark.unit
class TestDobotApiError:
    """Tests for error handling in parse_response."""

    def test_nonzero_error_code_raises(self):
        with pytest.raises(DobotApiError) as exc_info:
            parse_response("1,10,some error;", AckResponse)
        err = exc_info.value
        assert err.error_code == 1
        assert err.command_id == 10
        assert "1,10,some error;" in err.raw

    def test_error_attributes(self):
        # The regex uses \d+ so negative error codes don't match the 3-field
        # format.  Use a positive non-zero error code instead.
        with pytest.raises(DobotApiError) as exc_info:
            parse_response("3,5,fail;", AckResponse)
        err = exc_info.value
        assert err.error_code == 3
        assert err.command_id == 5

    def test_brace_error(self):
        with pytest.raises(DobotApiError):
            parse_response("2,{err};", AckResponse)


@pytest.mark.unit
class TestParseResponseEdgeCases:
    """Edge cases for parse_response."""

    def test_unrecognized_format_raises_value_error(self):
        with pytest.raises(ValueError, match="Unrecognized"):
            parse_response("garbage data", AckResponse)

    def test_empty_string_raises(self):
        with pytest.raises(ValueError):
            parse_response("", AckResponse)

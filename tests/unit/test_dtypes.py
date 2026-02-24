"""Unit tests for dobot_api_v4.dtypes module."""

import numpy as np
import pytest

from dobot_api_v4.dtypes import FeedbackData, FeedbackDtype, PROTOCOL_FIELD_MAP


@pytest.mark.unit
class TestFeedbackDtype:
    """Tests for the numpy dtype definition."""

    def test_itemsize_is_1440(self):
        assert FeedbackDtype.itemsize == 1440

    def test_dtype_has_expected_fields(self):
        names = FeedbackDtype.names
        assert names is not None
        assert "robot_mode" in names
        assert "q_actual" in names
        assert "tool_vector_actual" in names
        assert "digital_inputs" in names
        assert "speed_scaling" in names

    def test_q_actual_shape(self):
        """q_actual should be 6 float64 values."""
        sub = FeedbackDtype["q_actual"]
        assert sub.shape == (6,)
        assert sub.base == np.float64

    def test_target_quaternion_shape(self):
        """target_quaternion should be 4 float64 values."""
        sub = FeedbackDtype["target_quaternion"]
        assert sub.shape == (4,)

    def test_can_create_zero_buffer(self):
        arr = np.zeros(1, dtype=FeedbackDtype)
        assert arr.nbytes == 1440

    def test_can_parse_from_bytes(self):
        buf = np.zeros(1, dtype=FeedbackDtype).tobytes()
        arr = np.frombuffer(buf, dtype=FeedbackDtype)
        assert arr.shape == (1,)


@pytest.mark.unit
class TestFeedbackData:
    """Tests for the FeedbackData frozen dataclass."""

    def test_from_numpy_roundtrip(self):
        arr = np.zeros(1, dtype=FeedbackDtype)
        arr["robot_mode"] = 5
        arr["speed_scaling"] = 80.0
        arr["q_actual"] = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0]

        fd = FeedbackData.from_numpy(arr)

        assert fd.robot_mode == 5
        assert fd.speed_scaling == 80.0
        assert fd.q_actual == (1.0, 2.0, 3.0, 4.0, 5.0, 6.0)

    def test_from_numpy_all_zeros(self):
        arr = np.zeros(1, dtype=FeedbackDtype)
        fd = FeedbackData.from_numpy(arr)

        assert fd.robot_mode == 0
        assert fd.speed_scaling == 0.0
        assert fd.load == 0.0
        assert fd.q_actual == (0.0, 0.0, 0.0, 0.0, 0.0, 0.0)

    def test_frozen(self):
        arr = np.zeros(1, dtype=FeedbackDtype)
        fd = FeedbackData.from_numpy(arr)
        with pytest.raises(AttributeError):
            fd.robot_mode = 99  # type: ignore[misc]

    def test_scalar_types(self):
        arr = np.zeros(1, dtype=FeedbackDtype)
        arr["robot_mode"] = 7
        arr["load"] = 3.5
        fd = FeedbackData.from_numpy(arr)

        assert isinstance(fd.robot_mode, int)
        assert isinstance(fd.load, float)

    def test_tuple_types(self):
        arr = np.zeros(1, dtype=FeedbackDtype)
        arr["q_actual"] = [10, 20, 30, 40, 50, 60]
        fd = FeedbackData.from_numpy(arr)

        assert isinstance(fd.q_actual, tuple)
        assert len(fd.q_actual) == 6

    def test_hand_type_is_int_tuple(self):
        arr = np.zeros(1, dtype=FeedbackDtype)
        arr["hand_type"] = [1, 2, 3, 4]
        fd = FeedbackData.from_numpy(arr)

        assert fd.hand_type == (1, 2, 3, 4)
        assert all(isinstance(x, int) for x in fd.hand_type)

    def test_quaternion_fields(self):
        arr = np.zeros(1, dtype=FeedbackDtype)
        arr["target_quaternion"] = [0.1, 0.2, 0.3, 0.4]
        arr["actual_quaternion"] = [0.5, 0.6, 0.7, 0.8]
        fd = FeedbackData.from_numpy(arr)

        assert len(fd.target_quaternion) == 4
        assert len(fd.actual_quaternion) == 4
        assert abs(fd.target_quaternion[0] - 0.1) < 1e-9


@pytest.mark.unit
class TestProtocolFieldMap:
    """Tests for the PROTOCOL_FIELD_MAP dictionary."""

    def test_is_nonempty_dict(self):
        assert isinstance(PROTOCOL_FIELD_MAP, dict)
        assert len(PROTOCOL_FIELD_MAP) > 30

    def test_known_mappings(self):
        assert PROTOCOL_FIELD_MAP["RobotMode"] == "robot_mode"
        assert PROTOCOL_FIELD_MAP["QActual"] == "q_actual"
        assert PROTOCOL_FIELD_MAP["TCPForce"] == "tcp_force"
        assert PROTOCOL_FIELD_MAP["ToolVectorActual"] == "tool_vector_actual"
        assert PROTOCOL_FIELD_MAP["UserValue[6]"] == "user_coords"
        assert PROTOCOL_FIELD_MAP["ToolValue[6]"] == "tool_coords"

    def test_all_values_are_valid_dtype_fields(self):
        dtype_names = set(FeedbackDtype.names or [])
        # Not all mapped names correspond directly (reserve fields excluded)
        for snake_name in PROTOCOL_FIELD_MAP.values():
            assert snake_name in dtype_names, f"{snake_name} not in dtype"

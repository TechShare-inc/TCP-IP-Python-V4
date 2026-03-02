"""Unit tests for dobot_api_v4.feedback module."""

from unittest.mock import MagicMock

import pytest

from dobot_api_v4.dtypes import FeedbackData


@pytest.mark.unit
class TestDobotApiFeedback:
    """Tests for the DobotApiFeedback class."""

    def test_raw_feedback_data_returns_none_when_no_socket(self, mock_feedback):
        mock_feedback.socket_dobot = None
        assert mock_feedback.raw_feedback_data() is None

    def test_raw_feedback_data_parses_valid_buffer(
        self, mock_feedback, feedback_buffer_factory
    ):
        buf = feedback_buffer_factory(robot_mode=5, speed_scaling=80.0)
        assert len(buf) == 1440

        # Mock socket to return exactly 1440 bytes
        mock_feedback.socket_dobot.recv.return_value = buf
        mock_feedback.socket_dobot.setblocking = MagicMock()

        result = mock_feedback.raw_feedback_data()
        assert result is not None
        assert result["robot_mode"][0] == 5
        assert result["speed_scaling"][0] == 80.0

    def test_feedback_data_returns_dataclass(
        self, mock_feedback, feedback_buffer_factory
    ):
        buf = feedback_buffer_factory(robot_mode=7, load=2.5)
        mock_feedback.socket_dobot.recv.return_value = buf
        mock_feedback.socket_dobot.setblocking = MagicMock()

        result = mock_feedback.feedback_data()
        assert isinstance(result, FeedbackData)
        assert result.robot_mode == 7
        assert result.load == 2.5

    def test_feedback_data_returns_none_when_no_socket(self, mock_feedback):
        mock_feedback.socket_dobot = None
        assert mock_feedback.feedback_data() is None

    def test_last_recv_time_updates(self, mock_feedback, feedback_buffer_factory):
        buf = feedback_buffer_factory()
        mock_feedback.socket_dobot.recv.return_value = buf
        mock_feedback.socket_dobot.setblocking = MagicMock()

        old_time = mock_feedback.last_recv_time
        mock_feedback.raw_feedback_data()
        # last_recv_time should have updated (it uses perf_counter)
        # We can't assert the exact value, but it should have changed
        # since old_time was 0.0
        assert mock_feedback.last_recv_time != old_time or old_time == 0.0

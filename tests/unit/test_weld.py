"""Unit tests for dobot_api_v4.commands._weld_mixin module."""

import pytest


@pytest.mark.unit
class TestWeldMixin:
    """Tests verifying exact protocol strings for weld commands."""

    def test_arc_track_start(self, mock_dashboard):
        dashboard, sent = mock_dashboard
        dashboard.arc_track_start()
        assert sent[-1] == "ArcTrackStart()"

    def test_arc_track_params(self, mock_dashboard):
        dashboard, sent = mock_dashboard
        dashboard.arc_track_params(100, 0, -5.0, 5.0, 0.0, -3.0, 3.0, 0.0)
        cmd = sent[-1]
        assert cmd.startswith("ArcTrackParams(100,0,")

    def test_arc_track_end(self, mock_dashboard):
        dashboard, sent = mock_dashboard
        dashboard.arc_track_end()
        assert sent[-1] == "ArcTrackEnd()"

    def test_set_arc_track_offset(self, mock_dashboard):
        dashboard, sent = mock_dashboard
        dashboard.set_arc_track_offset(1.0, 2.0, 3.0, 0.1, 0.2, 0.3)
        cmd = sent[-1]
        assert cmd.startswith("SetArcTrackOffset(")

    def test_weave_start(self, mock_dashboard):
        dashboard, sent = mock_dashboard
        dashboard.weave_start()
        assert sent[-1] == "WeaveStart()"

    def test_weave_params(self, mock_dashboard):
        dashboard, sent = mock_dashboard
        dashboard.weave_params(
            1,
            10.0,
            5.0,
            5.0,
            0,
            0,
            0,
            0,
            0,
            0,
            0.0,
            0.0,
        )
        cmd = sent[-1]
        assert cmd.startswith("WeaveParams(1,")

    def test_weave_end(self, mock_dashboard):
        dashboard, sent = mock_dashboard
        dashboard.weave_end()
        assert sent[-1] == "WeaveEnd()"

    def test_weld_arc_speed_start(self, mock_dashboard):
        dashboard, sent = mock_dashboard
        dashboard.weld_arc_speed_start()
        assert sent[-1] == "WeldArcSpeedStart()"

    def test_weld_arc_speed(self, mock_dashboard):
        dashboard, sent = mock_dashboard
        dashboard.weld_arc_speed(100.0)
        assert "WeldArcSpeed(" in sent[-1]

    def test_weld_arc_speed_end(self, mock_dashboard):
        dashboard, sent = mock_dashboard
        dashboard.weld_arc_speed_end()
        assert sent[-1] == "WeldArcSpeedEnd()"

    def test_weld_weave_start(self, mock_dashboard):
        dashboard, sent = mock_dashboard
        dashboard.weld_weave_start(
            1,
            1.5,
            3.0,
            3.0,
            0,
            0,
            0,
            0,
            0,
            0,
            0.0,
            0.0,
        )
        assert "WeldWeaveStart(" in sent[-1]

    def test_rel_point_weld_line(self, mock_dashboard):
        dashboard, sent = mock_dashboard
        dashboard.rel_point_weld_line(
            0.0,
            100.0,
            50.0,
            10.0,
            15.0,
            0.0,
            [1, 2, 3, 4, 5, 6],
            [7, 8, 9, 10, 11, 12],
        )
        cmd = sent[-1]
        assert cmd.startswith("RelPointWeldLine(")

    def test_rel_point_weld_arc(self, mock_dashboard):
        dashboard, sent = mock_dashboard
        dashboard.rel_point_weld_arc(
            0.0,
            100.0,
            50.0,
            10.0,
            15.0,
            0.0,
            [1, 2, 3, 4, 5, 6],
            [7, 8, 9, 10, 11, 12],
            [13, 14, 15, 16, 17, 18],
        )
        cmd = sent[-1]
        assert cmd.startswith("RelPointWeldArc(")


@pytest.mark.unit
class TestWeldMixinBackwardCompat:
    """Verify PascalCase aliases exist."""

    def test_arc_track_start_alias(self, mock_dashboard):
        dashboard, sent = mock_dashboard
        dashboard.ArcTrackStart()
        assert sent[-1] == "ArcTrackStart()"

    def test_weave_start_alias(self, mock_dashboard):
        dashboard, sent = mock_dashboard
        dashboard.WeaveStart()
        assert sent[-1] == "WeaveStart()"

    def test_weave_end_alias(self, mock_dashboard):
        dashboard, sent = mock_dashboard
        dashboard.WeaveEnd()
        assert sent[-1] == "WeaveEnd()"

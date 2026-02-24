"""Unit tests for dobot_api_v4.commands._conveyor_mixin module."""

import pytest


@pytest.mark.unit
class TestConveyorMixin:
    """Tests verifying exact protocol strings for conveyor commands."""

    def test_cnv_init(self, mock_dashboard):
        dashboard, sent = mock_dashboard
        dashboard.cnv_init(0)
        assert sent[-1] == "CnvInit(0)"

    def test_cnv_mov_l_basic(self, mock_dashboard):
        dashboard, sent = mock_dashboard
        dashboard.cnv_mov_l(100, 200, 300, 0, 90, 0)
        cmd = sent[-1]
        assert cmd.startswith("CnvMovL(pose={")
        assert "100.000000" in cmd

    def test_cnv_mov_l_with_params(self, mock_dashboard):
        dashboard, sent = mock_dashboard
        dashboard.cnv_mov_l(100, 200, 300, 0, 90, 0, user=0, tool=0, v=50)
        cmd = sent[-1]
        assert "user=0" in cmd
        assert "tool=0" in cmd
        assert "v=50" in cmd

    def test_cnv_mov_c(self, mock_dashboard):
        dashboard, sent = mock_dashboard
        dashboard.cnv_mov_c(
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
        )
        cmd = sent[-1]
        assert cmd.startswith("CnvMovC(pose={")

    def test_get_cnv_object(self, mock_dashboard):
        dashboard, sent = mock_dashboard
        dashboard.get_cnv_object(0)
        assert sent[-1] == "GetCnvObject(0)"

    def test_set_cnv_point_offset(self, mock_dashboard):
        dashboard, sent = mock_dashboard
        dashboard.set_cnv_point_offset(1.0, 2.0)
        assert "SetCnvPointOffset(" in sent[-1]

    def test_set_cnv_time_compensation(self, mock_dashboard):
        dashboard, sent = mock_dashboard
        dashboard.set_cnv_time_compensation(100)
        assert "SetCnvTimeCompensation(100)" == sent[-1]

    def test_start_sync_cnv(self, mock_dashboard):
        dashboard, sent = mock_dashboard
        dashboard.start_sync_cnv()
        assert sent[-1] == "StartSyncCnv()"

    def test_stop_sync_cnv(self, mock_dashboard):
        dashboard, sent = mock_dashboard
        dashboard.stop_sync_cnv()
        assert sent[-1] == "StopSyncCnv()"


@pytest.mark.unit
class TestConveyorMixinBackwardCompat:
    """Verify PascalCase aliases exist."""

    def test_cnv_init_alias(self, mock_dashboard):
        dashboard, sent = mock_dashboard
        dashboard.CnvInit(0)
        assert sent[-1] == "CnvInit(0)"

    def test_cnv_mov_l_alias(self, mock_dashboard):
        dashboard, sent = mock_dashboard
        dashboard.CnvMovL(0, 0, 0, 0, 0, 0)
        assert "CnvMovL(" in sent[-1]

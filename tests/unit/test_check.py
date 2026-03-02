"""Unit tests for dobot_api_v4.commands._check_mixin module."""

import pytest


@pytest.mark.unit
class TestCheckMixin:
    """Tests verifying exact protocol strings for check commands."""

    def test_check_mov_c(self, mock_dashboard):
        dashboard, sent = mock_dashboard
        dashboard.check_mov_c(
            1,
            2,
            3,
            4,
            5,
            6,  # via point 1
            7,
            8,
            9,
            10,
            11,
            12,  # via point 2
            13,
            14,
            15,
            16,
            17,
            18,  # target
        )
        cmd = sent[-1]
        assert cmd.startswith("CheckMovC(joint={")

    def test_check_mov_j(self, mock_dashboard):
        """check_mov_j takes 12 joint floats (two joint groups), no coordinate_mode."""
        dashboard, sent = mock_dashboard
        dashboard.check_mov_j(
            10,
            20,
            30,
            0,
            90,
            0,  # point A
            40,
            50,
            60,
            0,
            0,
            0,  # point B
        )
        cmd = sent[-1]
        assert cmd.startswith("CheckMovJ(joint={")

    def test_check_mov_j_with_params(self, mock_dashboard):
        dashboard, sent = mock_dashboard
        dashboard.check_mov_j(
            10,
            20,
            30,
            40,
            50,
            60,
            70,
            80,
            90,
            0,
            0,
            0,
            user=0,
            tool=0,
        )
        cmd = sent[-1]
        assert "user=0" in cmd
        assert "tool=0" in cmd

    def test_check_mov_l(self, mock_dashboard):
        """check_mov_l takes 12 joint floats (two joint groups), no coordinate_mode."""
        dashboard, sent = mock_dashboard
        dashboard.check_mov_l(
            100,
            200,
            300,
            0,
            90,
            0,  # point A
            400,
            500,
            600,
            0,
            0,
            0,  # point B
        )
        cmd = sent[-1]
        assert cmd.startswith("CheckMovL(joint={")

    def test_check_mov_l_with_params(self, mock_dashboard):
        dashboard, sent = mock_dashboard
        dashboard.check_mov_l(
            100,
            200,
            300,
            0,
            90,
            0,
            400,
            500,
            600,
            0,
            0,
            0,
            user=0,
            tool=0,
        )
        cmd = sent[-1]
        assert "user=0" in cmd
        assert "tool=0" in cmd

    def test_check_odd_mov_c(self, mock_dashboard):
        dashboard, sent = mock_dashboard
        dashboard.check_odd_mov_c(
            1,
            2,
            3,
            4,
            5,
            6,
            7,  # via 1
            8,
            9,
            10,
            11,
            12,
            13,
            14,  # via 2
            15,
            16,
            17,
            18,
            19,
            20,
            21,  # target
        )
        cmd = sent[-1]
        assert cmd.startswith("CheckOddMovC(joint={")

    def test_check_odd_mov_j(self, mock_dashboard):
        """check_odd_mov_j takes 12 joint floats (two groups of 6)."""
        dashboard, sent = mock_dashboard
        dashboard.check_odd_mov_j(
            1,
            2,
            3,
            4,
            5,
            6,  # point A
            7,
            8,
            9,
            10,
            11,
            12,  # point B
        )
        cmd = sent[-1]
        assert cmd.startswith("CheckOddMovJ(joint={")

    def test_check_odd_mov_l(self, mock_dashboard):
        """check_odd_mov_l takes 12 joint floats (two groups of 6)."""
        dashboard, sent = mock_dashboard
        dashboard.check_odd_mov_l(
            1,
            2,
            3,
            4,
            5,
            6,  # point A
            7,
            8,
            9,
            10,
            11,
            12,  # point B
        )
        cmd = sent[-1]
        assert cmd.startswith("CheckOddMovL(joint={")

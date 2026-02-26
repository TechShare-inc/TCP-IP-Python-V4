"""Hardware-in-the-loop test configuration.

These tests require a real Dobot robot connected on the network.
Set the ``DOBOT_TEST_IP`` environment variable to the robot's IP address
to enable these tests.
"""

import os

import pytest

DOBOT_TEST_IP = os.environ.get("DOBOT_TEST_IP")

pytestmark = pytest.mark.skipif(not DOBOT_TEST_IP, reason="DOBOT_TEST_IP not set")


@pytest.fixture(scope="module")
def real_dashboard():
    """Connect to a real robot dashboard on port 29999."""
    from dobot_api_v4.commands.dashboard import DobotApiDashboard

    if DOBOT_TEST_IP is None:
        pytest.skip("DOBOT_TEST_IP not set")

    dashboard = DobotApiDashboard(DOBOT_TEST_IP, 29999)
    yield dashboard
    dashboard.close()


@pytest.fixture(scope="module")
def real_robot():
    """Connect to a real robot via DobotRobot façade."""
    from dobot_api_v4.robot import DobotRobot

    if DOBOT_TEST_IP is None:
        pytest.skip("DOBOT_TEST_IP not set")

    robot = DobotRobot(DOBOT_TEST_IP)
    yield robot
    robot.close()

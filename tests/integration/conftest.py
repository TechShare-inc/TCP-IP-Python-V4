"""Integration test fixtures using stub TCP servers."""

import pytest

from .stub_server import StubServer


@pytest.fixture(scope="module")
def stub_server():
    """A basic stub server that responds to common commands."""
    responses = {
        "EnableRobot": "0,1,;",
        "DisableRobot": "0,2,;",
        "ClearError": "0,3,;",
        "RobotMode": "0,4,5;",
        "GetPose": "0,5,100.0,200.0,300.0,0.0,90.0,45.0;",
        "GetErrorID": "0,6,0;",
        "SpeedFactor": "0,7,;",
    }
    with StubServer(response_map=responses) as srv:
        yield srv

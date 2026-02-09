"""
Utility functions for Dobot API V4
"""

import os
import json

alarmControllerFile = "files/alarmController.json"
alarmServoFile = "files/alarmServo.json"


def alarmAlarmJsonFile():
    """
    Read controller and servo alarm files.

    Returns:
        tuple: (dataController, dataServo) - JSON data from alarm files
    """
    currrntDirectory = os.path.dirname(__file__)
    jsonContrellorPath = os.path.join(currrntDirectory, alarmControllerFile)
    jsonServoPath = os.path.join(currrntDirectory, alarmServoFile)

    with open(jsonContrellorPath, encoding="utf-8") as f:
        dataController = json.load(f)
    with open(jsonServoPath, encoding="utf-8") as f:
        dataServo = json.load(f)
    return dataController, dataServo

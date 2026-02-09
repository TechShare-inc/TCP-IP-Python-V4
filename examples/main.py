# Updated for V4.0.0: Using monolithic architecture with all commands in DobotApiDashboard

from basic_demo import DobotDemo

if __name__ == "__main__":
    dobot = DobotDemo("192.168.5.1")
    dobot.start()

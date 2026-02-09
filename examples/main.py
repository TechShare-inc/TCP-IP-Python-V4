# Updated for V4.0.0: Using updated basic_demo with separate DobotApiMove class

from basic_demo import DobotDemo

if __name__ == "__main__":
    dobot = DobotDemo("192.168.5.1")
    dobot.start()

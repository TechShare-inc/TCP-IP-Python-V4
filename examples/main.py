# Updated for V4.0.0: Using updated basic_demo with separate DobotApiMove class
# V4.0.0更新：使用更新的basic_demo，带有独立的DobotApiMove类

from basic_demo import DobotDemo

if __name__ == "__main__":
    dobot = DobotDemo("192.168.5.1")
    dobot.start()

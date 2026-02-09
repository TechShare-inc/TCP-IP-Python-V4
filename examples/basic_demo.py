# Updated for V4.0.0: Movement commands now use separate DobotApiMove class

from dobot_api import DobotApiFeedBack, DobotApiDashboard, DobotApiMove
import threading
from time import sleep
import re


class DobotDemo:
    def __init__(self, ip):
        self.ip = ip
        self.dashboardPort = 29999
        self.feedPortFour = 30004
        self.dashboard = None
        self.move = None  # V4: Separate movement API
        self.feedInfo = []
        self.__globalLockValue = threading.Lock()

        class item:
            def __init__(self):
                self.robotMode = -1  #
                self.robotCurrentCommandID = 0
                self.MessageSize = -1
                self.DigitalInputs = -1
                self.DigitalOutputs = -1
                self.robotCurrentCommandID = -1

        self.feedData = item()

    def start(self):
        self.dashboard = DobotApiDashboard(self.ip, self.dashboardPort)
        self.move = DobotApiMove(
            self.ip, self.dashboardPort
        )  # V4: Separate movement API
        self.feedFour = DobotApiFeedBack(self.ip, self.feedPortFour)
        if self.parseResultId(self.dashboard.EnableRobot())[0] != 0:
            print("Enable failed: Check if port 29999 is occupied")
            return
        print("Enable successful")

        feed_thread = threading.Thread(target=self.GetFeed)
        feed_thread.daemon = True
        feed_thread.start()

        point_a = [146.3759, -283.4321, 332.3956, 177.7879, -1.8540, 147.5821]
        point_b = [146.3759, -283.4321, 432.3956, 177.7879, -1.8540, 147.5821]

        while True:
            print(
                "DI:",
                self.feedData.DigitalInputs,
                "2DI:",
                bin(self.feedData.DigitalInputs),
                "--16:",
                hex(self.feedData.DigitalInputs),
            )
            print(
                "DO:",
                self.feedData.DigitalOutputs,
                "2DO:",
                bin(self.feedData.DigitalOutputs),
                "--16:",
                hex(self.feedData.DigitalOutputs),
            )
            print("robomode", self.feedData.robotMode)
            sleep(2)

    def GetFeed(self):
        while True:
            feedInfo = self.feedFour.feedBackData()
            with self.__globalLockValue:
                if feedInfo is not None:
                    if hex((feedInfo["TestValue"][0])) == "0x123456789abcdef":
                        self.feedData.MessageSize = feedInfo["len"][0]
                        self.feedData.robotMode = feedInfo["RobotMode"][0]
                        self.feedData.DigitalInputs = feedInfo["DigitalInputs"][0]
                        self.feedData.DigitalOutputs = feedInfo["DigitalOutputs"][0]
                        self.feedData.robotCurrentCommandID = feedInfo[
                            "CurrentCommandId"
                        ][0]
                        """
                        self.feedData.DigitalOutputs = int(feedInfo['DigitalOutputs'][0])
                        self.feedData.RobotMode = int(feedInfo['RobotMode'][0])
                        self.feedData.TimeStamp = int(feedInfo['TimeStamp'][0])
                        """

    def RunPoint(self, point_list):
        recvmovemess = self.move.MovJ(
            *point_list, coordinateMode=0
        )  # V4: Use separate move instance
        print("MovJ:", recvmovemess)
        print(self.parseResultId(recvmovemess))
        currentCommandID = self.parseResultId(recvmovemess)[1]
        print("Command ID:", currentCommandID)
        # sleep(0.02)
        while True:

            print(self.feedData.robotMode)
            if (
                self.feedData.robotMode == 5
                and self.feedData.robotCurrentCommandID == currentCommandID
            ):
                print("Motion completed")
                break
            sleep(0.1)

    def parseResultId(self, valueRecv):
        if "Not Tcp" in valueRecv:
            print("Control Mode Is Not Tcp")
            return [1]
        return [int(num) for num in re.findall(r"-?\d+", valueRecv)] or [2]

    def __del__(self):
        del self.dashboard
        del self.move
        del self.feedFour

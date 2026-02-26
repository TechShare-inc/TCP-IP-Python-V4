#!/usr/bin/env python3
"""Entry point for the basic Dobot demo."""

from basic_demo import DobotDemo

if __name__ == "__main__":
    demo = DobotDemo("192.168.5.1")
    try:
        demo.start()
    except KeyboardInterrupt:
        demo.close()

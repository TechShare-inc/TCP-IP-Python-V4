#!/usr/bin/env python3
"""Basic usage example.

Difficulty: Beginner
Prerequisites: Installed package and valid local/dev configuration
"""

from package_name import Client


def main() -> None:
    client = Client.connect("endpoint")
    print(client.ping())


if __name__ == "__main__":
    main()

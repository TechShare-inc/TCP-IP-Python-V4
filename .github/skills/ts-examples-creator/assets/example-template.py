#!/usr/bin/env python3
"""Template tutorial example.

Difficulty: Beginner
Prerequisites: Installed package and valid local/dev configuration
"""

from package_name import Client

CONFIG_VALUE = "example"


def main() -> None:
    client = Client(CONFIG_VALUE)
    result = client.run()
    print(result)


if __name__ == "__main__":
    main()

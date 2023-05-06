# Copyright Amethyst Reese
# Licensed under the MIT license

import sys
from pathlib import Path

from rich import print

from .tail import tail


def main():
    log_path = Path(sys.argv[1])
    for event in tail(log_path):
        print(event)


if __name__ == "__main__":
    main()

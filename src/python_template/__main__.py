import argparse
import sys
from typing import Optional


def get_args_parser():
    parser = argparse.ArgumentParser(description="Python Template")
    return parser


def main(args: Optional[str] = None) -> Optional[int]:
    parser = get_args_parser()
    args = parser.parse_args(args)
    return 0


if __name__ == "__main__":
    sys.exit(main())

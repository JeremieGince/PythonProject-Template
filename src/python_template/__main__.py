import argparse
import sys


def get_args_parser():
    parser = argparse.ArgumentParser(description="Python Template")
    return parser


def main():
    parser = get_args_parser()
    args = parser.parse_args()
    return 0


if __name__ == "__main__":
    sys.exit(main())

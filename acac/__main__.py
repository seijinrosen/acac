import sys

from . import cli


def main() -> None:
    cli.main(sys.argv[1:])


if __name__ == "__main__":
    main()

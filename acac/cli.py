from __future__ import annotations

import platform
import shutil

from . import __version__, core
from .util import console, includes

HELP_MESSAGE = """\
競プロ便利ツール。

[bold]Usage:[/bold]
  acac

[bold]Options:[/bold]
  [blue]-j[/blue]              judge.

[bold]Global options:[/bold]
  [blue]-h, --help[/blue]      Show this help message and exit.
  [blue]-V, --version[/blue]   Show program's version number and exit.

See https://github.com/seijinrosen/acac for more information.\
"""


def print_help_message() -> None:
    console.print(HELP_MESSAGE)


def print_version() -> None:
    print("acac:", __version__)
    print("Python:", platform.python_version())
    print("which:", shutil.which("acac"))


def main(args: list[str]) -> None:
    if not args or includes(args, {"-h", "--help"}):
        print_help_message()
        return

    if includes(args, {"-V", "--version"}):
        print_version()
        return

    core.main(args)

from __future__ import annotations

import platform
from pathlib import Path

from acac import __version__, core
from acac.config import load_config
from acac.util import console, includes

HELP_MESSAGE = """\
競プロ便利ツール。

[bold]Usage:[/bold]
  acac <url> \\[options]

[bold]Options:[/bold]
  [blue]-c, --create[/blue]           Create environment mode. (default)
  [blue]-j, --judge[/blue]            Judge mode.

  [blue]-f, --file, file=FILE[/blue]  ソースファイル名を指定する。
  [blue]-l, --lang, lang=LANG[/blue]  言語を指定する。

[bold]Global options:[/bold]
  [blue]-h, --help[/blue]             Show this help message and exit.
  [blue]-V, --version[/blue]          Show program's version number and exit.

See https://github.com/seijinrosen/acac for more information.\
"""


def print_help_message() -> None:
    console.print(HELP_MESSAGE)


def print_version() -> None:
    console.print("acac:  ", __version__)
    console.print("Python:", platform.python_version())
    console.print("from:  ", Path(__file__).parent)


def main(args: list[str]) -> None:
    if not args or includes(args, {"-h", "--help"}):
        print_help_message()
        return

    if includes(args, {"-V", "--version"}):
        print_version()
        return

    if args[0] == "init":
        return

    core.main(args, load_config())

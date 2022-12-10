from __future__ import annotations

import platform
from pathlib import Path

from acac import __version__, config, core
from acac.util import console, includes

HELP_MESSAGE = """\
競プロ便利ツール。

[bold]Usage:[/bold]
  acac <url> \\[options]
  acac init                              Create configuration file "acac.toml".

[bold]Options:[/bold]
  [blue]-c, --create[/blue]                           Create environment mode. (default)
  [blue]-j, --judge[/blue]                            Judge mode.
  [blue]-m, --manual[/blue]                           URL にアクセスせず、HTML ファイルを手動で配置してテストケースを作成するモード。

  [blue]-l, --lang,   lang=LANG_NAME[/blue]           言語を指定する。
  [blue]-s, --source, source=SOURCE_FILE_NAME[/blue]  ソースファイル名を指定する。

[bold]Global options:[/bold]
  [blue]-h, --help[/blue]                             Show this help message and exit.
  [blue]-V, --version[/blue]                          Show program's version number and exit.

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
        config.init()
        return

    core.main(args, config.load())

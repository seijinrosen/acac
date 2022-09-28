from __future__ import annotations

import os
import subprocess
import time
import webbrowser
from pathlib import Path

import pyperclip
from pydantic import BaseModel
from rich.markup import escape
from rich.table import Table

from acac import algo_method, atcoder
from acac.config import Config
from acac.share import Folder, ProblemType
from acac.util import UTF_8, confirm_yN, console, run_with_log


class IOSample(BaseModel):
    in_file: Path
    in_text: str
    out_text: str


class Result(BaseModel):
    name: str
    input: str
    expected: str
    actual: str
    error: str
    is_accepted: bool
    execution_ms: int


def main(
    url: str, folder: Folder, problem_type: ProblemType, lang_name: str, config: Config
) -> None:
    lang_setting = config.language.settings[lang_name]

    if lang_setting.commands.version:
        run_with_log(
            [*map(os.path.expanduser, lang_setting.commands.version.split())],
            check=True,
        )

    if lang_setting.commands.compile:
        compile_command = expand_command(
            lang_setting.commands.compile, folder.path, folder.source_file
        )
        run_with_log(compile_command, check=True)

    execute_command = expand_command(
        lang_setting.commands.execute, folder.path, folder.source_file
    )
    results = get_results(execute_command, load_io_samples(folder.in_, folder.out))

    console.print(create_table(results))

    if all(r.is_accepted for r in results):
        console.print("All Completed! AC!!!:thumbs_up:", style="green")

        source_code = folder.source_file.read_text(encoding=UTF_8)
        pyperclip.copy(source_code)  # type: ignore
        console.print("[bold]Copied source code to clipboard:", folder.source_file)

        if problem_type in {"algo_method", "atcoder"} and confirm_yN("他の人の提出を確認しますか？"):
            ac_url = get_ac_url(problem_type, url, lang_name)
            webbrowser.open(ac_url)
            console.print("[bold]Opened:", ac_url)

        if config.judge.clipboard_message:
            clipboard_message = config.judge.clipboard_message.replace(
                "${url}", url
            ).replace("${lang}", lang_name)
            pyperclip.copy(clipboard_message)  # type: ignore
            console.print("[bold]Copied to clipboard:", escape(clipboard_message))
    else:
        console.print("WA...:", end=" ", style="red")
        console.print(*[r.name for r in results if not r.is_accepted])


def expand_command(command: str, dir: Path, source_file: Path) -> list[str]:
    return [
        *map(
            os.path.expanduser,
            command.replace("${dir}", str(dir))
            .replace("${source_file}", str(source_file))
            .split(),
        )
    ]


def load_io_samples(i_dir: Path, o_dir: Path) -> list[IOSample]:
    return [
        IOSample(
            in_file=i_file,
            in_text=i_file.read_text(encoding=UTF_8),
            out_text=o_file.read_text(encoding=UTF_8),
        )
        for i_file, o_file in zip(sorted(i_dir.iterdir()), sorted(o_dir.iterdir()))
    ]


def get_results(execute_command: list[str], io_samples: list[IOSample]) -> list[Result]:
    def get_result(io_sample: IOSample) -> Result:
        start = time.time()
        console.print("[bold]Running:", *execute_command, "<", io_sample.in_file)
        cp = subprocess.run(
            execute_command, capture_output=True, input=io_sample.in_text, text=True
        )
        return Result(
            name=io_sample.in_file.name,
            input=io_sample.in_text,
            expected=io_sample.out_text,
            actual=cp.stdout,
            error=cp.stderr,
            is_accepted=io_sample.out_text == cp.stdout,
            execution_ms=int((time.time() - start) * 1000),
        )

    return [get_result(x) for x in io_samples]


def create_table(results: list[Result]) -> Table:
    table = Table(
        "name", "input", "expected", "actual", "error", header_style="bold magenta"
    )
    table.add_column("result", style="bold", justify="center")
    table.add_column("time(ms)", justify="right")
    for r in results:
        table.add_row(
            r.name,
            r.input,
            r.expected,
            r.actual,
            escape(r.error),
            "[green]AC" if r.is_accepted else "[red]WA",
            str(r.execution_ms),
        )
    return table


def get_ac_url(problem_type: ProblemType, url: str, lang: str) -> str:
    if problem_type == "algo_method":
        return algo_method.get_ac_url(url, lang)
    if problem_type == "atcoder":
        return atcoder.get_ac_url(url, lang)
    return ""

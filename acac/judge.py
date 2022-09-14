from __future__ import annotations

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
    name: str
    in_: str
    out: str


class Result(BaseModel):
    name: str
    input: str
    expected: str
    actual: str
    error: str
    is_accepted: bool
    execution_ms: int


def main(
    url: str, folder: Folder, problem_type: ProblemType, lang: str, config: Config
) -> None:
    lang_command = get_lang_command(config.lang[lang].command)
    run_with_log([lang_command, "--version"], check=True)
    io_samples = load_io_samples(folder.in_, folder.out)

    if lang == "cpp":
        a_out = folder.path / "a.out"
        run_with_log([lang_command, folder.exec_file, "-o", a_out], check=True)
        results = get_results([a_out], io_samples)
    else:
        results = get_results([lang_command, folder.exec_file], io_samples)

    console.print(create_table(results))

    if all(r.is_accepted for r in results):
        console.print("All Completed! AC!!!:thumbs_up:", style="green")
        if config.judge.clipboard_message:
            clipboard_message = config.judge.clipboard_message.replace(
                "${url}", url
            ).replace("${lang}", lang)
            pyperclip.copy(clipboard_message)  # type: ignore
            console.print("以下の文字列がクリップボードにコピーされました。")
            console.print(clipboard_message)
        if problem_type in {"algo_method", "atcoder"} and confirm_yN("他の人の提出を確認しますか？"):
            webbrowser.open(get_ac_url(problem_type, url, lang))
    else:
        console.print("WA...:", end=" ", style="red")
        console.print(*[r.name for r in results if not r.is_accepted])


def get_lang_command(command: str) -> str | Path:
    if command.startswith("~"):
        return Path(command).expanduser()
    return command


def load_io_samples(i_dir: Path, o_dir: Path) -> list[IOSample]:
    return [
        IOSample(
            name=i_file.stem,
            in_=i_file.read_text(encoding=UTF_8),
            out=o_file.read_text(encoding=UTF_8),
        )
        for i_file, o_file in zip(sorted(i_dir.iterdir()), sorted(o_dir.iterdir()))
    ]


def get_results(cmd_args: list[str | Path], io_samples: list[IOSample]) -> list[Result]:
    def get_result(io_sample: IOSample) -> Result:
        start = time.time()
        console.print(f"[bold]Running {io_sample.name}:", *cmd_args)
        cp = subprocess.run(
            cmd_args, capture_output=True, input=io_sample.in_, text=True
        )
        return Result(
            name=io_sample.name,
            input=io_sample.in_,
            expected=io_sample.out,
            actual=cp.stdout,
            error=cp.stderr,
            is_accepted=io_sample.out == cp.stdout,
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

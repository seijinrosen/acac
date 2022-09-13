from __future__ import annotations

import time
from pathlib import Path

from pydantic import BaseModel
from rich.markup import escape
from rich.table import Table

from acac import config
from acac.share import Folder
from acac.util import console, run_with_log


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


def main(folder: Folder, lang: str) -> None:
    lang_command = get_lang_command(config.lang_settings[lang].command)
    run_with_log([lang_command, "--version"], check=True)
    io_samples = load_io_samples(folder.in_, folder.out)

    if lang == "cpp":
        a_out = folder.path / "a.out"
        run_with_log([lang_command, folder.exec_file, "-o", a_out], check=True)
        results = get_results([a_out], io_samples)
    else:
        results = get_results([lang_command, folder.exec_file], io_samples)

    console.print(create_table(results))


def get_lang_command(command: str) -> str | Path:
    if command.startswith("~"):
        return Path(command).expanduser()
    return command


def load_io_samples(i_dir: Path, o_dir: Path) -> list[IOSample]:
    return [
        IOSample(name=i_file.stem, in_=i_file.read_text(), out=o_file.read_text())
        for i_file, o_file in zip(sorted(i_dir.iterdir()), sorted(o_dir.iterdir()))
    ]


def get_results(cmd_args: list[str | Path], io_samples: list[IOSample]) -> list[Result]:
    def get_result(io_sample: IOSample) -> Result:
        start = time.time()
        stdout, stderr = run_with_log(
            cmd_args, capture_output=True, input=io_sample.in_, text=True
        )
        return Result(
            name=io_sample.name,
            input=io_sample.in_,
            expected=io_sample.out,
            actual=stdout,
            error=stderr,
            is_accepted=io_sample.out == stdout,
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

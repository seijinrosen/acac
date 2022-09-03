from __future__ import annotations

import subprocess
from pathlib import Path
from shutil import copy

from pydantic import BaseModel

from acac import algo_method, atcoder, config
from acac.share import Folder, ProblemType
from acac.util import console, dump_to_toml, get_soup, get_title, request_bytes

TEMPLATES_DIR = Path("templates")


class Metadata(BaseModel):
    title: str
    url: str


def main(url: str, folder: Folder, problem_type: ProblemType) -> None:
    folder.path.mkdir(parents=True, exist_ok=True)

    if not folder.exec_file.exists():
        copy(TEMPLATES_DIR / folder.exec_file.name, folder.path)
        console.print(
            "[bold]Copied:",
            TEMPLATES_DIR / folder.exec_file.name,
            "->",
            folder.exec_file,
        )

    if not folder.cache_html.exists():
        folder.cache_html.write_bytes(request_bytes(url))
        console.print("[bold]Dumped:", folder.cache_html)

    soup = get_soup(folder.cache_html.read_bytes())
    dump_to_toml(Metadata(title=get_title(soup), url=url), folder.metadata_toml)

    if problem_type == "algo_method":
        i_samples = algo_method.get_samples(soup, "入")
        o_samples = algo_method.get_samples(soup, "出")
        dump_samples(i_samples, folder.in_)
        dump_samples(o_samples, folder.out)
    else:
        get_samples = atcoder.compose_get_samples(soup)
        dump_samples(get_samples("入"), folder.in_)
        dump_samples(get_samples("出"), folder.out)

    if config.new.auto_git_add:
        subprocess.run(
            ["git", "add", folder.in_, folder.out, folder.metadata_toml], check=True
        )

    if config.new.auto_editor_open:
        subprocess.run([config.editor_command, ".", folder.exec_file], check=True)


def dump_samples(samples: list[str], io_dir: Path) -> None:
    if not samples:
        return
    io_dir.mkdir(exist_ok=True)
    for i, sample_str in enumerate(samples, start=1):
        file = io_dir / f"{i:02}.txt"
        if sample_str == "":
            file.touch()
        else:
            file.write_text(sample_str + "\n", encoding="utf-8")

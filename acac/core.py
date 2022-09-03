from __future__ import annotations

import os
from pathlib import Path

from acac import algo_method, atcoder, config, judge, new
from acac.share import Folder, ProblemType
from acac.util import includes


def main(args: list[str]) -> None:
    url = args[0]
    problem_type = get_problem_type(url)
    folder = get_folder(url, config.lang_settings[config.default_lang].file_name)

    if includes(args, {"-j", "--judge"}):
        judge.main(url)
    else:
        new.main(url, folder, problem_type)


def get_problem_type(url: str) -> ProblemType:
    if url.startswith(algo_method.BASE_URL):
        return "algo_method"
    if url.startswith(atcoder.BASE_URL):
        return "atcoder"
    return "else"


def get_folder(url: str, lang_file_name: str) -> Folder:
    folder_path = Path(os.path.join(*url.split("/")[2:]))
    return Folder(
        path=folder_path,
        in_=folder_path / "in",
        out=folder_path / "out",
        cache_html=folder_path / "cache.html",
        metadata_toml=folder_path / "metadata.toml",
        exec_file=folder_path / lang_file_name,
    )

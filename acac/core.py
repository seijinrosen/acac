from __future__ import annotations

import os
from pathlib import Path

from acac import algo_method, atcoder, config, judge, new
from acac.share import Folder, ProblemType
from acac.util import includes


def main(args: list[str]) -> None:
    url = args[0]
    problem_type = get_problem_type(url)
    lang = get_lang(args, config.default_lang)
    folder = get_folder(url, config.lang_settings[lang].file_name)

    if includes(args, {"-j", "--judge"}):
        judge.main(folder, lang)
    else:
        new.main(url, folder, problem_type)


def get_problem_type(url: str) -> ProblemType:
    if url.startswith(algo_method.BASE_URL):
        return "algo_method"
    if url.startswith(atcoder.BASE_URL):
        return "atcoder"
    return "else"


def get_lang(args: list[str], default_lang: str) -> str:
    for x in args:
        if x.startswith(("-l=", "--lang=", "lang=")):
            return x.split("=")[1]
    return default_lang


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

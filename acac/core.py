from __future__ import annotations

import os
from pathlib import Path

from typing_extensions import Literal

from acac import algo_method, atcoder, create, judge
from acac.config import Config
from acac.share import Folder, ProblemType


def main(args: list[str], config: Config) -> None:
    url = args[0]
    problem_type = get_problem_type(url)
    lang_name = get_lang_name(args, config.language.default)
    source_file_name = get_source_file_name(
        args, config.language.settings[lang_name].source_file_name
    )
    folder = get_folder(url, source_file_name)
    clipboard_replace_map = {
        "${lang}": lang_name,
        "${url}": url,
    }

    if get_mode(args) == "create":
        create.main(url, folder, problem_type, lang_name, config, clipboard_replace_map)
    else:
        judge.main(url, folder, problem_type, lang_name, config, clipboard_replace_map)


def get_problem_type(url: str) -> ProblemType:
    if url.startswith(algo_method.BASE_URL):
        return "algo_method"
    if url.startswith(atcoder.BASE_URL):
        return "atcoder"
    return "else"


def get_lang_name(args: list[str], default_lang: str) -> str:
    for x in args[::-1]:
        if x.startswith(("-l=", "--lang=", "lang=")):
            return x.split("=")[1]
    return default_lang


def get_source_file_name(args: list[str], default_file_name: str) -> str:
    for x in args[::-1]:
        if x.startswith(("-f=", "--file=", "file=")):
            return x.split("=")[1]
    return default_file_name


def get_folder(url: str, source_file_name: str) -> Folder:
    folder_path = Path(os.path.join(*url.split("/")[2:]))
    return Folder(
        path=folder_path,
        in_=folder_path / "in",
        out=folder_path / "out",
        cache_html=folder_path / "cache.html",
        metadata_toml=folder_path / "metadata.toml",
        source_file=folder_path / source_file_name,
    )


def get_mode(args: list[str]) -> Literal["create", "judge"]:
    for x in args[::-1]:
        if x in {"-c", "--create"}:
            return "create"
        elif x in {"-j", "--judge"}:
            return "judge"
    return "create"

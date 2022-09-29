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
    dir_path = Path(get_dir_path(url))

    folder = Folder(
        dir_path=dir_path,
        in_=dir_path / "in",
        out=dir_path / "out",
        cache_html=dir_path / "cache.html",
        metadata_toml=dir_path / "metadata.toml",
        source_file=dir_path / source_file_name,
    )

    replace_map = {
        "${dir_path}": str(dir_path),
        "${lang}": lang_name,
        "${source_file_name}": source_file_name,
        "${source_file_path}": str(folder.source_file),
        "${url}": url,
    }

    if get_mode(args) == "create":
        create.main(url, folder, problem_type, lang_name, config, replace_map)
    else:
        judge.main(url, folder, problem_type, lang_name, config, replace_map)


def get_problem_type(url: str) -> ProblemType:
    if url.startswith(algo_method.BASE_URL):
        return "algo_method"
    if url.startswith(atcoder.BASE_URL):
        return "atcoder"
    return "else"


def get_after_equal_option(
    args: list[str], prefix: tuple[str, ...], default: str
) -> str:
    return next((x.split("=")[1] for x in args[::-1] if x.startswith(prefix)), default)


def get_lang_name(args: list[str], default: str) -> str:
    return get_after_equal_option(args, ("-l=", "--lang=", "lang="), default)


def get_source_file_name(args: list[str], default: str) -> str:
    return get_after_equal_option(args, ("-s=", "--source=", "source="), default)


def get_dir_path(url: str) -> str:
    if url.startswith(("http://", "https://")):
        return os.path.join(*url.split("/")[2:])
    else:
        return os.path.join(*url.split("/"))


def get_mode(args: list[str]) -> Literal["create", "judge"]:
    for x in args[::-1]:
        if x in {"-c", "--create"}:
            return "create"
        elif x in {"-j", "--judge"}:
            return "judge"
    return "create"

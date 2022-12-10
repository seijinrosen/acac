from __future__ import annotations

import shutil
from pathlib import Path

from pydantic import BaseModel

from acac import algo_method, atcoder
from acac.config import Config
from acac.share import Folder, ProblemType, expand_command
from acac.util import (
    UTF_8,
    confirm_yN,
    console,
    copy2clip_with_log,
    dump_to_toml,
    get_soup,
    get_title,
    replaced,
    request_bytes,
    run_with_log,
)


class Metadata(BaseModel):
    title: str
    url: str


def main(
    url: str,
    folder: Folder,
    problem_type: ProblemType,
    lang_name: str,
    config: Config,
    replace_map: dict[str, str],
    manual: bool = False,
) -> None:
    if not folder.dir_path.exists():
        folder.dir_path.mkdir(parents=True)
        console.print("[bold]mkdir:", folder.dir_path)

    if not folder.source_file.exists():
        template_file = config.language.settings[lang_name].template_file_path
        if template_file and template_file.expanduser().exists():
            shutil.copy(template_file.expanduser(), folder.source_file)
            console.print("[bold]Copied:", template_file, "->", folder.source_file)
        else:
            folder.source_file.touch()
            console.print("[bold]touch:", folder.source_file)

    if not folder.cache_html.exists():
        if manual:
            console.print("マニュアルモード")
            if confirm_yN("HTML ファイルを配置しましたか？"):
                html_file = next(folder.dir_path.glob("*.html"))
                html_file.rename(folder.cache_html)
                console.print("[bold]Renamed:", html_file, "->", folder.cache_html)
        elif problem_type == "atcoder":
            folder.cache_html.write_bytes(request_bytes(url + "?lang=ja"))
            console.print("[bold]Dumped:", folder.cache_html)
        else:
            folder.cache_html.write_bytes(request_bytes(url))
            console.print("[bold]Dumped:", folder.cache_html)

    soup = get_soup(folder.cache_html.read_bytes())

    if not folder.metadata_toml.exists():
        dump_to_toml(Metadata(title=get_title(soup), url=url), folder.metadata_toml)
        console.print("[bold]Created:", folder.metadata_toml)

    if problem_type == "algo_method":
        i_samples = algo_method.get_samples(soup, "入")
        o_samples = algo_method.get_samples(soup, "出")
        dump_samples(i_samples, folder.in_)
        dump_samples(o_samples, folder.out)
    else:
        get_samples = atcoder.compose_get_samples(soup)
        dump_samples(get_samples("入"), folder.in_)
        dump_samples(get_samples("出"), folder.out)

    for cmd in config.create.post_create_commands:
        run_with_log(expand_command(cmd, replace_map), check=True)

    if config.create.clipboard_message:
        copy2clip_with_log(replaced(config.create.clipboard_message, replace_map))


def dump_samples(samples: list[str], io_dir: Path) -> None:
    if not io_dir.exists():
        io_dir.mkdir()
        console.print("[bold]mkdir:", io_dir)

    for i, sample_str in enumerate(samples, start=1):
        file = io_dir / f"{i:02}.txt"
        if not file.exists():
            if sample_str == "":
                file.touch()
                console.print("[bold]touch:", file)
            else:
                file.write_text(sample_str + "\n", encoding=UTF_8)
                console.print("[bold]Created:", file)

from __future__ import annotations

import json
import subprocess
from pathlib import Path

import requests
import tomli_w
from bs4 import BeautifulSoup, ResultSet, Tag
from pydantic import BaseModel
from rich.console import Console

console = Console()


def includes(args: list[str], flags: set[str]) -> bool:
    return any(s in args for s in flags)


# subprocess
def run_with_log(
    cmd_args: list[str | Path],
    capture_output: bool = False,
    check: bool = False,
    input: str | None = None,
    text: bool = False,
) -> tuple[str, str]:
    console.print("[bold]Running:", *cmd_args)
    cp = subprocess.run(
        args=cmd_args,
        capture_output=capture_output,
        check=check,
        input=input,
        text=text,
    )
    return cp.stdout, cp.stderr


# tomli
def dump_to_toml(obj: BaseModel, toml_path: Path) -> None:
    toml_path.write_text(tomli_w.dumps(json.loads(obj.json())), encoding="utf-8")


# requests
def request_bytes(url: str, with_log: bool = True) -> bytes:
    if with_log:
        console.print("[bold]Requesting...:", url)
    response = requests.get(url)
    response.raise_for_status()
    if with_log:
        console.print("Success!:thumbs_up:", style="bold green")
    response.encoding = response.apparent_encoding
    return response.content.replace(b"\r\n", b"\n")


# bs4
def get_soup(markup: str | bytes) -> BeautifulSoup:
    return BeautifulSoup(markup, "lxml")


def get_title(soup: BeautifulSoup) -> str:
    return soup.title.text.strip() if soup.title else ""


def get_tags(soup: BeautifulSoup, tag_name: str) -> ResultSet[Tag]:
    return soup(tag_name)


def get_next_tag_text(tag: Tag, next_tag_name: str) -> str:
    next_tag = tag.find_next(next_tag_name)
    return next_tag.text.strip() if next_tag else ""

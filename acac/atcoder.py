from __future__ import annotations

from functools import partial
from typing import Callable

from bs4 import BeautifulSoup, Tag

from acac.share import IorO
from acac.util import get_next_tag_text, get_tags

BASE_URL = "https://atcoder.jp/contests/"


def compose_get_samples(soup: BeautifulSoup) -> Callable[[IorO], list[str]]:
    def gs(
        soup: BeautifulSoup,
        tag_name: str,
        next_tag_name: str,
        func: Callable[[Tag, str], str],
        i_or_o: IorO,
    ) -> list[str]:
        return [
            func(tag, next_tag_name)
            for tag in get_tags(soup, tag_name)
            if f"{i_or_o}力例" in tag.text
            # if f"Sample {'Input' if i_or_o=='入' else 'Output'}" in tag.text
        ]

    return partial(gs, soup, "h3", "pre", get_next_tag_text)


def get_ac_url(url: str, lang: str) -> str:
    language_name = {
        "bash": "Bash",
        "c": "C",
        "cpp": "C%2B%2B",
        "cs": "C%23",
        "csharp": "C%23",
        "go": "Go",
        "golang": "Go",
        "haskell": "Haskell",
        "hs": "Haskell",
        "java": "Java",
        "javascript": "JavaScript",
        "js": "JavaScript",
        "php": "PHP",
        "py": "Python3",
        "pypy": "Python3",
        "pypy2": "Python2",
        "pypy3": "Python3",
        "python": "Python3",
        "python2": "Python2",
        "python3": "Python3",
        "rb": "Ruby",
        "rs": "Rust",
        "ruby": "Ruby",
        "rust": "Rust",
        "ts": "TypeScript",
        "typescript": "TypeScript",
        "zsh": "Zsh",
    }.get(lang, "")
    return f"{BASE_URL}{get_contest_name(url)}/submissions?f.Task={get_task_name(url)}&f.LanguageName={language_name}&f.Status=AC&f.User="


def get_contest_name(url: str) -> str:
    return url.split("/")[4]


def get_task_name(url: str) -> str:
    return url.split("/")[-1]

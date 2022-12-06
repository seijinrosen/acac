from __future__ import annotations

import json
from itertools import takewhile

from bs4 import BeautifulSoup

from acac.share import IorO

BASE_URL = "https://algo-method.com/tasks/"


def get_samples(soup: BeautifulSoup, i_or_o: IorO) -> list[str]:
    it = iter(extract_script_body(soup).splitlines())
    ret: list[str] = []
    for row in it:
        if not row.startswith(f"#### {i_or_o}力例"):
            continue
        next(it)
        sample_texts = takewhile(lambda x: not x.startswith("```"), it)
        ret.append("\n".join(sample_texts))
    return ret


def extract_script_body(soup: BeautifulSoup) -> str:
    script_tag = soup.find("script", {"id": "__NEXT_DATA__"})
    script_text = script_tag.text if script_tag else ""
    script_json = json.loads(script_text)
    return script_json["props"]["pageProps"]["tasks"]["body"]


def get_ac_url(url: str, lang: str) -> str:
    language = {
        "c": 5,
        "cpp": 1,
        "cs": 7,
        "csharp": 7,
        "go": 9,
        "golang": 9,
        "haskell": 15,
        "hs": 15,
        "java": 6,
        "javascript": 8,
        "js": 8,
        "php": 17,
        "py": 2,
        "pypy": 16,
        "pypy3": 16,
        "python": 2,
        "python3": 2,
        "rb": 3,
        "rs": 13,
        "ruby": 3,
        "ruby3": 3,
        "rust": 13,
        "ts": 11,
        "typescript": 11,
    }.get(lang)
    if language is None:
        return f"{url}/submissions?id={get_task_id(url)}&status=AC&page=0"
    return (
        f"{url}/submissions?id={get_task_id(url)}&language={language}&status=AC&page=0"
    )


def get_task_id(url: str) -> str:
    return url.split("/")[-1]

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

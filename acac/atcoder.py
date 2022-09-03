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

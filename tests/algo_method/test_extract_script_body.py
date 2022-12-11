from pathlib import Path

from acac.algo_method import extract_script_body
from acac.util import get_soup

CACHE_HTML = Path("tests/algo_method/cache.html")


def test():
    soup = get_soup(CACHE_HTML.read_bytes())
    assert extract_script_body(soup) == "アルゴ式 テストスクリプトボディ"

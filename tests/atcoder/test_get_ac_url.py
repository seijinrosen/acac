from acac.atcoder import get_ac_url

URL = "https://atcoder.jp/contests/abc283/tasks/abc283_a"


def test():
    assert (
        get_ac_url(URL, "python3")
        == "https://atcoder.jp/contests/abc283/submissions?f.Task=abc283_a&f.LanguageName=Python3&f.Status=AC&f.User="
    )


def test_none():
    assert (
        get_ac_url(URL, "not_exist_lang")
        == "https://atcoder.jp/contests/abc283/submissions?f.Task=abc283_a&f.LanguageName=&f.Status=AC&f.User="
    )

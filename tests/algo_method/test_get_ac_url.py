from acac.algo_method import get_ac_url


def test():
    assert (
        get_ac_url("https://algo-method.com/tasks/411", "python3")
        == "https://algo-method.com/tasks/411/submissions?id=411&language=2&status=AC&page=0"
    )


def test_none():
    assert (
        get_ac_url("https://algo-method.com/tasks/411", "not_exist_lang")
        == "https://algo-method.com/tasks/411/submissions?id=411&status=AC&page=0"
    )

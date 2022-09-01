from __future__ import annotations

from enum import Enum, auto

from . import judge, new
from .util import includes


def main(args: list[str]) -> None:
    new_or_judge = (
        NewOrJudge.JUDGE if includes(args, {"-j", "--judge"}) else NewOrJudge.NEW
    )
    url = args[0]

    if new_or_judge == NewOrJudge.NEW:
        new.main(url)
    elif new_or_judge == NewOrJudge.JUDGE:
        judge.main(url)


class NewOrJudge(Enum):
    NEW = auto()
    JUDGE = auto()

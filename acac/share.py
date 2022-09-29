from __future__ import annotations

import os
from pathlib import Path

from pydantic import BaseModel
from typing_extensions import Literal

from acac.util import replaced

IorO = Literal["入", "出"]
ProblemType = Literal["algo_method", "atcoder", "else"]


class Folder(BaseModel):
    path: Path
    in_: Path
    out: Path
    cache_html: Path
    metadata_toml: Path
    source_file: Path


def expand_command(command: str, replace_map: dict[str, str]) -> list[str]:
    return [*map(os.path.expanduser, replaced(command, replace_map).split())]

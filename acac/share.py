from pathlib import Path

from pydantic import BaseModel
from typing_extensions import Literal

IorO = Literal["入", "出"]
ProblemType = Literal["algo_method", "atcoder", "else"]


class Folder(BaseModel):
    path: Path
    in_: Path
    out: Path
    cache_html: Path
    metadata_toml: Path
    exec_file: Path

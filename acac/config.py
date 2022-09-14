from pathlib import Path
from typing import Dict

import tomli
from pydantic import BaseModel

from acac.util import UTF_8, console

ACAC_TOML = Path("acac.toml")

DEFAULT_ACAC_TOML = """\
default_lang = "pypy3"
editor_command = "code"
templates_dir = "templates"

[create]
auto_editor_open = true
auto_git_add = false

[lang.cpp]
command = "g++"
file_name = "main.cpp"

[lang.pypy3]
command = "pypy3"
file_name = "main.py"

[lang.python3]
command = "python3"
file_name = "main.py"

[lang.ts]
command = "ts-node"
file_name = "main.ts"
"""


class Create(BaseModel):
    auto_editor_open: bool
    auto_git_add: bool


class LangSetting(BaseModel):
    command: str
    file_name: str


class Config(BaseModel):
    default_lang: str
    editor_command: str
    templates_dir: Path
    create: Create
    lang: Dict[str, LangSetting]


if not ACAC_TOML.exists():
    ACAC_TOML.write_text(DEFAULT_ACAC_TOML, encoding=UTF_8)
    console.print("Created:", ACAC_TOML, "\n")


_config = Config(**tomli.loads(ACAC_TOML.read_text(encoding=UTF_8)))

default_lang = _config.default_lang
editor_command = _config.editor_command
templates_dir = _config.templates_dir

create = _config.create
lang_settings = _config.lang

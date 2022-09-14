import shutil
from pathlib import Path
from typing import Dict

import tomli
from pydantic import BaseModel

from acac.util import UTF_8, console

ACAC_TOML = Path("acac.toml")
DEFAULT_ACAC_TOML = Path(__file__).parent / "default_acac.toml"


class Create(BaseModel):
    auto_editor_open: bool
    auto_git_add: bool
    clipboard_message: str


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
    shutil.copy(DEFAULT_ACAC_TOML, ACAC_TOML)
    console.print("Created:", ACAC_TOML, "\n")


_config = Config(**tomli.loads(ACAC_TOML.read_text(encoding=UTF_8)))

default_lang = _config.default_lang
editor_command = _config.editor_command
templates_dir = _config.templates_dir

create = _config.create
lang_settings = _config.lang

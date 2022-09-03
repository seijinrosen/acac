from pathlib import Path
from typing import Dict

import tomli
from pydantic import BaseModel


class New(BaseModel):
    auto_editor_open: bool
    auto_git_add: bool


class LangSetting(BaseModel):
    command: str
    file_name: str


class Config(BaseModel):
    default_lang: str
    editor_command: str
    new: New
    lang: Dict[str, LangSetting]


_config = Config(**tomli.loads(Path("acac.toml").read_text()))

default_lang = _config.default_lang
editor_command = _config.editor_command
new = _config.new
lang_settings = _config.lang

import shutil
import sys
from pathlib import Path
from typing import Dict

import tomli
from pydantic import BaseModel

from acac.util import UTF_8, confirm_yN, console

ACAC_TOML = Path("acac.toml")
DEFAULT_ACAC_TOML = Path(__file__).parent / "default_acac.toml"


class Editor(BaseModel):
    command: str


class Create(BaseModel):
    auto_editor_open: bool
    auto_git_add: bool
    clipboard_message: str


class Judge(BaseModel):
    clipboard_message: str


class LangSetting(BaseModel):
    command: str
    file_name: str


class Config(BaseModel):
    default_lang: str
    templates_dir: Path
    editor: Editor
    create: Create
    judge: Judge
    lang: Dict[str, LangSetting]


def load_config() -> Config:
    if not ACAC_TOML.exists():
        console.print("このディレクトリ内に acac.toml が見つかりませんでした。")
        if confirm_yN("acac.toml を作成しますか？"):
            shutil.copy(DEFAULT_ACAC_TOML, ACAC_TOML)
            console.print("Created:", ACAC_TOML, "\n")
        else:
            sys.exit("Bye.")

    return Config(**tomli.loads(ACAC_TOML.read_text(encoding=UTF_8)))

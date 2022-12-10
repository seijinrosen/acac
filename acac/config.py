import shutil
import sys
from pathlib import Path
from typing import Dict, List, Optional

import tomli
from pydantic import BaseModel

from acac.util import UTF_8, confirm_yN, console

ACAC_TOML = Path("acac.toml")
DEFAULT_ACAC_TOML = Path(__file__).parent / "default_acac.toml"


class Create(BaseModel):
    post_create_commands: List[str] = []
    clipboard_message = ""


class Judge(BaseModel):
    copy_source_code_when_ac = False
    clipboard_message = ""


class LanguageSetting(BaseModel):
    class Commands(BaseModel):
        pre_execute: List[str] = []
        execute: str
        post_execute: List[str] = []

    source_file_name: str
    template_file_path: Optional[Path]
    commands: Commands


class Language(BaseModel):
    default: str
    settings: Dict[str, LanguageSetting]


class Config(BaseModel):
    create: Create
    judge: Judge
    language: Language


def init() -> None:
    if ACAC_TOML.exists():
        console.print("acac.toml がこのディレクトリ内に既に存在します。")
        return
    shutil.copy(DEFAULT_ACAC_TOML, ACAC_TOML)
    console.print("[bold]Created:", ACAC_TOML)


def load() -> Config:
    if not ACAC_TOML.exists():
        console.print("acac.toml がこのディレクトリ内に見つかりませんでした。")
        if confirm_yN("acac.toml を作成しますか？"):
            init()
        else:
            sys.exit("Bye.")
    return Config(**tomli.loads(ACAC_TOML.read_text(encoding=UTF_8)))

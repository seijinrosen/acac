import subprocess
from pathlib import Path

import pyperclip

UTF_8 = "utf-8"
TARGET_FILES = [
    "acac/__init__.py",
    "tests/test_acac.py",
    "pyproject.toml",
]

current_version = subprocess.run(
    ["poetry", "version"], capture_output=True, check=True, text=True
).stdout.split()[1]

print("current_version:", current_version)

new_version = input("? new_version: ")

for file in TARGET_FILES:
    p = Path(file)
    p.write_text(
        p.read_text(encoding=UTF_8).replace(current_version, new_version),
        encoding=UTF_8,
    )

commit_message = f"Bump version from {current_version} to {new_version}"
pyperclip.copy(commit_message)  # type: ignore
print("Copied:", commit_message)

from __future__ import annotations

from unittest.mock import MagicMock

import pytest
from pytest import CaptureFixture
from pytest_mock import MockerFixture

from acac import __version__, cli, core


@pytest.fixture
def mock_print_help_message(mocker: MockerFixture):
    yield mocker.patch.object(cli, cli.print_help_message.__name__, autospec=True)


@pytest.fixture
def mock_print_version(mocker: MockerFixture):
    yield mocker.patch.object(cli, cli.print_version.__name__, autospec=True)


@pytest.fixture
def mock_core_main(mocker: MockerFixture):
    yield mocker.patch.object(core, core.main.__name__, autospec=True)


@pytest.mark.parametrize(
    "args",
    [
        ["-h"],
        ["--help"],
        ["-V", "--help"],
        ["-h", "--version"],
    ],
)
def test_with_help_option(
    args: list[str],
    mock_print_help_message: MagicMock,
    mock_print_version: MagicMock,
    mock_core_main: MagicMock,
):
    assert cli.main(args) is None
    assert mock_print_help_message.call_count == 1
    assert mock_print_version.call_count == 0
    assert mock_core_main.call_count == 0


@pytest.mark.parametrize(
    "args",
    [
        ["-V"],
        ["--version"],
    ],
)
def test_with_version_option(
    args: list[str],
    mock_print_help_message: MagicMock,
    mock_print_version: MagicMock,
    mock_core_main: MagicMock,
):
    assert cli.main(args) is None
    assert mock_print_help_message.call_count == 0
    assert mock_print_version.call_count == 1
    assert mock_core_main.call_count == 0


def test_with_no_args(
    mock_print_help_message: MagicMock,
    mock_print_version: MagicMock,
    mock_core_main: MagicMock,
):
    assert cli.main([]) is None
    assert mock_print_help_message.call_count == 1
    assert mock_print_version.call_count == 0
    assert mock_core_main.call_count == 0


def test_print_help_message(capsys: CaptureFixture[str]):
    cli.print_help_message()
    out, err = capsys.readouterr()
    assert err == ""
    assert "競プロ便利ツール。" in out


def test_print_version(capsys: CaptureFixture[str]):
    cli.print_version()
    out, err = capsys.readouterr()
    assert err == ""
    assert __version__ in out

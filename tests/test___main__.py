from unittest.mock import MagicMock

import pytest
from pytest_mock import MockerFixture

from acac import __main__, cli


@pytest.fixture
def mock_cli_main(mocker: MockerFixture):
    yield mocker.patch.object(cli, cli.main.__name__, autospec=True)


def test_main(mock_cli_main: MagicMock):
    assert __main__.main() is None
    assert mock_cli_main.call_count == 1

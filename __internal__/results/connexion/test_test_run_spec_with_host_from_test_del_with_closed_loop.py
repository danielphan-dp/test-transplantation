import contextlib
import io
import logging
from unittest.mock import MagicMock, patch
import pytest
from connexion.cli import main
from connexion.exceptions import ResolverError
from connexion.options import SwaggerUIOptions
from conftest import FIXTURES_FOLDER

@pytest.fixture()
def mock_app_run_with_error(app_class, monkeypatch):
    mocked_app = MagicMock(name='mocked_app', wraps=app_class(__name__))

    def mocked_run(*args, **kwargs):
        mocked_app.middleware._build_middleware_stack()
        raise RuntimeError("Mocked run error")

    mocked_app.run = MagicMock(name='mocked_app.run', side_effect=mocked_run)

    def get_mocked_app(*args, **kwargs):
        return mocked_app
    mocked_app_class = MagicMock(name='mocked_app_class', side_effect=get_mocked_app)

    def get_mocked_app_class(*args, **kwargs):
        return mocked_app_class
    monkeypatch.setattr('connexion.cli.connexion.utils.get_function_from_name', get_mocked_app_class)
    return mocked_app_class

def test_run_spec_with_host_error(mock_app_run_with_error, spec_file):
    with pytest.raises(RuntimeError, match="Mocked run error"):
        main(["run", spec_file, "--host", "custom.host"])

def test_run_spec_with_invalid_host(mock_app_run, spec_file):
    with pytest.raises(SystemExit):
        main(["run", spec_file, "--host", "invalid.host"])

def test_run_spec_with_no_spec_file(mock_app_run):
    with pytest.raises(SystemExit):
        main(["run", "--host", "custom.host"])

def test_run_spec_with_empty_host(mock_app_run, spec_file):
    with pytest.raises(SystemExit):
        main(["run", spec_file, "--host", ""])
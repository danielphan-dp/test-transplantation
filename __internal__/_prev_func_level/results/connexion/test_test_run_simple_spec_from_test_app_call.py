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
def mock_app_run_with_error_handling(app_class, monkeypatch):
    mocked_app = MagicMock(name='mocked_app', wraps=app_class(__name__))

    def mocked_run(*args, **kwargs):
        mocked_app.middleware._build_middleware_stack()
    mocked_app.run = MagicMock(name='mocked_app.run', side_effect=mocked_run)

    def get_mocked_app(*args, **kwargs):
        return mocked_app
    mocked_app_class = MagicMock(name='mocked_app_class', side_effect=get_mocked_app)

    def get_mocked_app_class(*args, **kwargs):
        return mocked_app_class
    monkeypatch.setattr('connexion.cli.connexion.utils.get_function_from_name', get_mocked_app_class)
    return mocked_app_class

def test_run_with_invalid_spec(mock_app_run_with_error_handling):
    with pytest.raises(ResolverError):
        main(["run", "invalid_spec_file.yaml"])

def test_run_with_no_spec(mock_app_run_with_error_handling):
    with pytest.raises(SystemExit):
        main(["run"])

def test_run_with_empty_spec(mock_app_run_with_error_handling):
    empty_spec_file = str(FIXTURES_FOLDER / "empty/swagger.yaml")
    main(["run", empty_spec_file])
    
    app_instance = mock_app_run_with_error_handling()
    app_instance.run.assert_called()

def test_run_with_valid_spec(mock_app_run_with_error_handling, spec_file):
    main(["run", spec_file])
    
    app_instance = mock_app_run_with_error_handling()
    app_instance.run.assert_called()
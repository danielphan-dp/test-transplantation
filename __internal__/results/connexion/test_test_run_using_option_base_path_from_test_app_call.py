import contextlib
import io
import logging
from unittest.mock import MagicMock
import pytest
from connexion.cli import main
from connexion.exceptions import ResolverError
from connexion.options import SwaggerUIOptions
from conftest import FIXTURES_FOLDER

@pytest.fixture()
def invalid_spec_file():
    return "invalid/path/to/spec.yaml"

def test_run_with_invalid_spec_file(mock_app_run, invalid_spec_file):
    with pytest.raises(FileNotFoundError):
        main(["run", invalid_spec_file, "--base-path", "/foo"])

def test_run_with_missing_base_path(mock_app_run, expected_arguments, spec_file):
    main(["run", spec_file])
    
    expected_arguments = dict(
        base_path=None,
        resolver_error=None,
        validate_responses=False,
        strict_validation=False,
    )
    app_instance = mock_app_run()
    app_instance.add_api.assert_called_with(spec_file, **expected_arguments)

def test_run_with_invalid_arguments(mock_app_run):
    with pytest.raises(SystemExit):
        main(["run", "invalid_spec.yaml", "--unknown-arg", "value"])
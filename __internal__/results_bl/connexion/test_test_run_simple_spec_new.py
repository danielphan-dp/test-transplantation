import pytest
from unittest.mock import MagicMock
from connexion.cli.main import main

def test_run_with_invalid_spec(mock_app_run):
    invalid_spec_file = "invalid_spec.yaml"
    with pytest.raises(FileNotFoundError):
        main(["run", invalid_spec_file])

def test_run_with_empty_spec(mock_app_run):
    empty_spec_file = "empty_spec.yaml"
    with open(empty_spec_file, 'w') as f:
        f.write("")
    main(["run", empty_spec_file])
    app_instance = mock_app_run()
    app_instance.run.assert_called()

def test_run_with_missing_middleware(mock_app_run, monkeypatch):
    app_instance = mock_app_run()
    app_instance.middleware = None
    with pytest.raises(AttributeError):
        app_instance.run()
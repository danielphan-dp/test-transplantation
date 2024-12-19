import pytest
from unittest.mock import MagicMock
from connexion.cli.main import main

def test_run_spec_with_invalid_host(mock_app_run, spec_file):
    with pytest.raises(ValueError):
        main(["run", spec_file, "--host", "invalid.host"])

def test_run_spec_without_host(mock_app_run, spec_file):
    main(["run", spec_file])
    app_instance = mock_app_run()
    app_instance.run.assert_called()

def test_run_spec_with_empty_spec_file(mock_app_run):
    with pytest.raises(FileNotFoundError):
        main(["run", "", "--host", "custom.host"])

def test_run_spec_with_nonexistent_spec_file(mock_app_run):
    with pytest.raises(FileNotFoundError):
        main(["run", "nonexistent_spec.yaml", "--host", "custom.host"])

def test_run_spec_with_multiple_hosts(mock_app_run, spec_file):
    main(["run", spec_file, "--host", "custom.host", "--host", "another.host"])
    app_instance = mock_app_run()
    app_instance.run.assert_called()
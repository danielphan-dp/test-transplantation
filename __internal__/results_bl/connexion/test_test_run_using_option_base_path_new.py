import pytest
from unittest.mock import MagicMock
from connexion.cli.main import main

@pytest.fixture(scope='function')
def mock_app_run(app_class, monkeypatch):
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

def test_run_using_option_base_path(mock_app_run, expected_arguments, spec_file):
    main(["run", spec_file, "--base-path", "/foo"])

    expected_arguments = dict(
        base_path="/foo",
        resolver_error=None,
        validate_responses=False,
        strict_validation=False,
    )
    app_instance = mock_app_run()
    app_instance.add_api.assert_called_with(spec_file, **expected_arguments)

def test_run_with_invalid_base_path(mock_app_run, spec_file):
    with pytest.raises(SystemExit):
        main(["run", spec_file, "--base-path", "invalid_path"])

def test_run_without_spec_file(mock_app_run):
    with pytest.raises(SystemExit):
        main(["run", "--base-path", "/foo"])

def test_run_with_additional_arguments(mock_app_run, expected_arguments, spec_file):
    main(["run", spec_file, "--base-path", "/foo", "--debug"])

    expected_arguments = dict(
        base_path="/foo",
        resolver_error=None,
        validate_responses=False,
        strict_validation=False,
    )
    app_instance = mock_app_run()
    app_instance.add_api.assert_called_with(spec_file, **expected_arguments)

def test_run_with_resolver_error(mock_app_run, spec_file):
    app_instance = mock_app_run()
    app_instance.add_api.side_effect = Exception("Resolver Error")
    
    with pytest.raises(SystemExit):
        main(["run", spec_file, "--base-path", "/foo"])
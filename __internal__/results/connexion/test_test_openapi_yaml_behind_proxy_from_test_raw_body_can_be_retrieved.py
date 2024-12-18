import pytest

@pytest.fixture
def mock_app():
    from connexion import FlaskApp
    app = FlaskApp(__name__)
    return app

def test_get_with_kwargs(mock_app):
    response = mock_app.get(name='test')
    assert response == {'name': 'get', 'name': 'test'}

def test_get_without_kwargs(mock_app):
    response = mock_app.get()
    assert response == [{'name': 'get'}]

def test_get_with_empty_kwargs(mock_app):
    response = mock_app.get(**{})
    assert response == [{'name': 'get'}]

def test_get_with_multiple_kwargs(mock_app):
    response = mock_app.get(name='test', extra='value')
    assert response == {'name': 'get', 'name': 'test', 'extra': 'value'}
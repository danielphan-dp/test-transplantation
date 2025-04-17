import pytest
from connexion import App

@pytest.fixture
def app():
    app = App(__name__)
    return app

def test_get_with_kwargs(app):
    """Test get method with kwargs provided."""
    kwargs = {'key1': 'value1', 'key2': 'value2'}
    response = app.get('/v1.0/test', **kwargs)
    assert response == {'key1': 'value1', 'key2': 'value2', 'name': 'get'}

def test_get_without_kwargs(app):
    """Test get method without kwargs provided."""
    response = app.get('/v1.0/test')
    assert response == [{'name': 'get'}]

def test_get_with_empty_kwargs(app):
    """Test get method with empty kwargs."""
    kwargs = {}
    response = app.get('/v1.0/test', **kwargs)
    assert response == [{'name': 'get'}]
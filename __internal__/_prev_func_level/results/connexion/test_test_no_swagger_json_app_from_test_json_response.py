import pytest
from connexion import App

@pytest.fixture
def api_app():
    app = App(__name__)
    return app

def test_get_with_kwargs(api_app):
    response = api_app.get(name='test')
    assert response['name'] == 'get'
    assert response['name'] == 'get'

def test_get_without_kwargs(api_app):
    response = api_app.get()
    assert isinstance(response, list)
    assert len(response) == 1
    assert response[0]['name'] == 'get'

def test_get_with_empty_kwargs(api_app):
    response = api_app.get()
    assert isinstance(response, list)
    assert len(response) == 1
    assert response[0]['name'] == 'get'
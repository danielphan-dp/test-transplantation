import pytest
from connexion import App

@pytest.fixture
def app():
    app = App(__name__)
    return app

def test_get_with_kwargs(app):
    response = app.get('/v1.0/api', query_string={'key': 'value'})
    assert response.status_code == 200
    assert response.json == {'key': 'value', 'name': 'get'}

def test_get_without_kwargs(app):
    response = app.get('/v1.0/api')
    assert response.status_code == 200
    assert response.json == [{'name': 'get'}]

def test_get_with_empty_kwargs(app):
    response = app.get('/v1.0/api', query_string={})
    assert response.status_code == 200
    assert response.json == [{'name': 'get'}]
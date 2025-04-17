import pytest
from connexion import App

def test_get_with_kwargs():
    """Test the get method with kwargs provided."""
    app = App(__name__)
    client = app.test_client()

    response = client.get('/v1.0/test', query_string={'key': 'value'})
    assert response.status_code == 200
    assert response.json == {'key': 'value', 'name': 'get'}

def test_get_without_kwargs():
    """Test the get method without kwargs."""
    app = App(__name__)
    client = app.test_client()

    response = client.get('/v1.0/test')
    assert response.status_code == 200
    assert response.json == [{'name': 'get'}]

def test_get_with_empty_kwargs():
    """Test the get method with empty kwargs."""
    app = App(__name__)
    client = app.test_client()

    response = client.get('/v1.0/test', query_string={})
    assert response.status_code == 200
    assert response.json == [{'name': 'get'}]
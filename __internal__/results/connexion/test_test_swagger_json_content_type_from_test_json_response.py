import pytest

@pytest.fixture
def simple_app():
    from connexion import App
    app = App(__name__)
    return app

def test_get_with_kwargs(simple_app):
    response = simple_app.get(name='test')
    assert response['name'] == 'get'
    assert response['name'] == 'get'

def test_get_without_kwargs(simple_app):
    response = simple_app.get()
    assert len(response) == 1
    assert response[0]['name'] == 'get'

def test_get_with_empty_kwargs(simple_app):
    response = simple_app.get(**{})
    assert response['name'] == 'get'

def test_get_with_multiple_kwargs(simple_app):
    response = simple_app.get(param1='value1', param2='value2')
    assert response['name'] == 'get'
    assert 'param1' in response
    assert 'param2' in response

def test_get_with_none_kwargs(simple_app):
    response = simple_app.get(None)
    assert response[0]['name'] == 'get'
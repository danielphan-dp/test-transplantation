import logging
import pytest
from bs4 import BeautifulSoup
from sanic import Sanic
from sanic.exceptions import SanicException

app = Sanic("Test")

@app.route('/', name='hostindex', host='example.com')
@app.route('/path', name='hostpath', host='path.example.com')
def index(request):
    pass

@pytest.mark.parametrize('debug', (True, False))
def test_host_index(debug):
    _, response = app.test_client.get('/', debug=debug)
    assert response.status == 200
    assert response.body == b''

@pytest.mark.parametrize('debug', (True, False))
def test_host_path(debug):
    _, response = app.test_client.get('/path', debug=debug)
    assert response.status == 200
    assert response.body == b''

@pytest.mark.parametrize('debug', (True, False))
def test_host_index_not_found(debug):
    _, response = app.test_client.get('/nonexistent', debug=debug)
    assert response.status == 404

@pytest.mark.parametrize('debug', (True, False))
def test_host_path_not_found(debug):
    _, response = app.test_client.get('/path/nonexistent', debug=debug)
    assert response.status == 404

@pytest.mark.parametrize('debug', (True, False))
def test_host_index_with_query(debug):
    _, response = app.test_client.get('/?query=test', debug=debug)
    assert response.status == 200
    assert response.body == b''

@pytest.mark.parametrize('debug', (True, False))
def test_host_path_with_query(debug):
    _, response = app.test_client.get('/path?query=test', debug=debug)
    assert response.status == 200
    assert response.body == b''

@pytest.mark.parametrize('debug', (True, False))
def test_host_index_with_headers(debug):
    _, response = app.test_client.get('/', headers={'X-Custom-Header': 'value'}, debug=debug)
    assert response.status == 200
    assert response.body == b''

@pytest.mark.parametrize('debug', (True, False))
def test_host_path_with_headers(debug):
    _, response = app.test_client.get('/path', headers={'X-Custom-Header': 'value'}, debug=debug)
    assert response.status == 200
    assert response.body == b''
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
def test_host_index_route(debug):
    _, response = app.test_client.get('/', debug=debug)
    assert response.status == 200

@pytest.mark.parametrize('debug', (True, False))
def test_host_path_route(debug):
    _, response = app.test_client.get('/path', debug=debug)
    assert response.status == 200

@pytest.mark.parametrize('debug', (True, False))
def test_host_index_route_not_found(debug):
    _, response = app.test_client.get('/nonexistent', debug=debug)
    assert response.status == 404

@pytest.mark.parametrize('debug', (True, False))
def test_host_path_route_not_found(debug):
    _, response = app.test_client.get('/path/nonexistent', debug=debug)
    assert response.status == 404

@pytest.mark.parametrize('debug', (True, False))
def test_host_index_route_with_invalid_method(debug):
    _, response = app.test_client.put('/', debug=debug)
    assert response.status == 405

@pytest.mark.parametrize('debug', (True, False))
def test_host_path_route_with_invalid_method(debug):
    _, response = app.test_client.put('/path', debug=debug)
    assert response.status == 405
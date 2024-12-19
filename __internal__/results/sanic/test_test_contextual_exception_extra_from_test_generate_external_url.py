import pytest
from sanic import Sanic, response
from sanic.exceptions import SanicException

app = Sanic("Test")

@app.route('/', name='hostindex', host='example.com')
@app.route('/path', name='hostpath', host='path.example.com')
def index(request):
    return response.text("Hello, World!")

@pytest.mark.parametrize('debug', (True, False))
def test_host_routes(debug):
    _, response = app.test_client.get('/', debug=debug)
    assert response.status == 200
    assert response.text == "Hello, World!"

    _, response = app.test_client.get('/path', debug=debug)
    assert response.status == 200
    assert response.text == "Hello, World!"

    # Test for non-existent route
    _, response = app.test_client.get('/nonexistent', debug=debug)
    assert response.status == 404

    # Test with invalid host
    _, response = app.test_client.get('/', headers={'Host': 'invalid.example.com'}, debug=debug)
    assert response.status == 404

    # Test with valid host but wrong path
    _, response = app.test_client.get('/path', headers={'Host': 'example.com'}, debug=debug)
    assert response.status == 404

    # Test with valid host and path
    _, response = app.test_client.get('/', headers={'Host': 'example.com'}, debug=debug)
    assert response.status == 200
    assert response.text == "Hello, World!"
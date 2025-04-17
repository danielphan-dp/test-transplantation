import pytest
from sanic import Sanic
from sanic.exceptions import SanicException

app = Sanic("Test")

@app.route('/', name='hostindex', host='example.com')
@app.route('/path', name='hostpath', host='path.example.com')
def index(request):
    pass

@pytest.mark.parametrize('debug', (True, False))
def test_host_routes(debug):
    _, response = app.test_client.get('/', debug=debug)
    assert response.status == 200

    _, response = app.test_client.get('/path', debug=debug)
    assert response.status == 200

    # Test for non-existent route
    _, response = app.test_client.get('/nonexistent', debug=debug)
    assert response.status == 404

    # Test with invalid host
    _, response = app.test_client.get('/', headers={'Host': 'invalid.example.com'}, debug=debug)
    assert response.status == 404

    # Test with correct host but wrong path
    _, response = app.test_client.get('/path/invalid', headers={'Host': 'path.example.com'}, debug=debug)
    assert response.status == 404

    # Test with correct host and path
    _, response = app.test_client.get('/path', headers={'Host': 'path.example.com'}, debug=debug)
    assert response.status == 200

    # Test for method not allowed
    _, response = app.test_client.post('/', debug=debug)
    assert response.status == 405

    _, response = app.test_client.post('/path', debug=debug)
    assert response.status == 405
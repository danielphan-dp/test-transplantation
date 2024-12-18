import pytest
from sanic import Sanic
from sanic.response import text

@pytest.mark.parametrize('file_name', ['test.file', 'decode me.txt'])
@pytest.mark.parametrize('base_uri', ['/static', '', '/dir'])
def test_get_method(base_uri):
    app = Sanic("test_app")

    @app.get(base_uri)
    def get_method(request):
        return text('I am get method')

    request, response = app.test_client.get(base_uri)
    assert response.status == 200
    assert response.text == 'I am get method'

    # Test with an invalid URI
    invalid_uri = base_uri + '/invalid'
    request, response = app.test_client.get(invalid_uri)
    assert response.status == 404

    # Test with a different base URI
    new_base_uri = '/new_base'
    request, response = app.test_client.get(new_base_uri)
    assert response.status == 404

    # Test with an empty base URI
    empty_base_uri = ''
    request, response = app.test_client.get(empty_base_uri)
    assert response.status == 200
    assert response.text == 'I am get method'
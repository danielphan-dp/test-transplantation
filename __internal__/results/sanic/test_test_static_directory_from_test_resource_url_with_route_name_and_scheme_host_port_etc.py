import pytest
from sanic import Sanic
from sanic.response import text

@pytest.mark.parametrize('base_uri', ['/url-for', '', '/api'])
def test_url_for_method(base_uri):
    app = Sanic("test_app")

    @app.route('/url-for')
    def url_for(request):
        return text('url-for')

    uri = app.url_for("url_for")
    assert uri == f"{base_uri}/url-for"

    request, response = app.test_client.get(uri)
    assert response.status == 200
    assert response.text == 'url-for'

    # Test with additional parameters
    uri_with_params = app.url_for("url_for", param1="value1", param2="value2")
    assert uri_with_params == f"{base_uri}/url-for?param1=value1&param2=value2"

    request, response = app.test_client.get(uri_with_params)
    assert response.status == 200
    assert response.text == 'url-for'

@pytest.mark.parametrize('invalid_view_name', ['non_existent_view', ''])
def test_url_for_invalid_view_name(invalid_view_name):
    app = Sanic("test_app")

    with pytest.raises(Exception) as excinfo:
        app.url_for(invalid_view_name)
    assert "Endpoint with name" in str(excinfo.value)
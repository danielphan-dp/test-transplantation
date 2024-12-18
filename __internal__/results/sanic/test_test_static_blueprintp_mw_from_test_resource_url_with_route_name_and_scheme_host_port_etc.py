import pytest
from sanic import Sanic
from sanic.response import text

@pytest.mark.parametrize('view_name', ['url_for'])
def test_url_for_with_no_params(app: Sanic):
    @app.route('/url-for')
    def url_for(request):
        return text('url-for')

    url = app.url_for(view_name)
    assert url == '/url-for'
    request, response = app.test_client.get(url)
    assert response.status == 200
    assert response.text == 'url-for'

@pytest.mark.parametrize('view_name', ['url_for'])
def test_url_for_with_query_params(app: Sanic):
    @app.route('/url-for')
    def url_for(request):
        return text('url-for')

    url = app.url_for(view_name, param1='value1', param2='value2')
    assert url == '/url-for?param1=value1&param2=value2'
    request, response = app.test_client.get(url)
    assert response.status == 200
    assert response.text == 'url-for'

def test_url_for_with_invalid_view_name(app: Sanic):
    with pytest.raises(Exception) as e:
        app.url_for("invalid_view")
        assert str(e.value) == "Endpoint with name `invalid_view` was not found"

def test_url_for_with_server_name(app: Sanic):
    server_name = "example.com"
    app.config.update({"SERVER_NAME": server_name})

    @app.route('/url-for')
    def url_for(request):
        return text('url-for')

    url = f"http://{server_name}/url-for"
    assert url == app.url_for("url_for", _server=None, _external=True)
    request, response = app.test_client.get(url)
    assert response.status == 200
    assert response.text == 'url-for'
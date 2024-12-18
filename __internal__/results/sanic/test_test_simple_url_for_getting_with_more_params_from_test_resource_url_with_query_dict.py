import pytest
from sanic import Sanic
from sanic.response import text
from sanic.exceptions import URLBuildError

@pytest.mark.parametrize('args,url', [
    ({"param1": "value1", "param2": "value2"}, "/url-for?param1=value1&param2=value2"),
    ({"param1": "value1"}, "/url-for?param1=value1"),
    ({"param2": "value2"}, "/url-for?param2=value2"),
    ({}, "/url-for"),
])
def test_url_for_with_params(app, args, url):
    @app.route("/url-for")
    def url_for_view(request):
        return text('url-for')

    assert url == app.url_for("url_for_view", **args)
    request, response = app.test_client.get(url)
    assert response.status == 200
    assert response.text == 'url-for'

def test_fails_if_endpoint_not_found(app):
    with pytest.raises(URLBuildError) as e:
        app.url_for("non_existent_view")
        assert e.match("Endpoint with name `app.non_existent_view` was not found")

def test_fails_url_build_if_param_not_passed(app):
    @app.route("/url-for/<param>")
    def url_for_with_param(request, param):
        return text(f'param: {param}')

    with pytest.raises(URLBuildError) as e:
        app.url_for("url_for_with_param")
        assert e.match("Required parameter `param` was not passed to url_for")
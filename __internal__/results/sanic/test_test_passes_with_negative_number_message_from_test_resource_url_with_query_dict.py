import pytest
from sanic import Sanic
from sanic.response import text
from sanic.exceptions import URLBuildError

@pytest.mark.parametrize('number', [3, -3, 13.123, -13.123, 0])
def test_url_for_with_negative_and_zero_number(app, number):
    @app.route("/url-for")
    def url_for(request):
        return text('url-for')

    u = app.url_for("url_for")
    assert u == "/url-for", u
    request, response = app.test_client.get(u)
    assert response.status == 200
    assert response.text == "url-for"

@pytest.mark.parametrize('number', [None, "string", {}, []])
def test_url_for_with_invalid_number(app, number):
    @app.route("/url-for")
    def url_for(request):
        return text('url-for')

    with pytest.raises(URLBuildError) as e:
        app.url_for("url_for", possibly_neg=number)
        assert e.match("Required parameter `possibly_neg` was not passed to url_for")
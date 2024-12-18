import pytest
from sanic import Sanic
from sanic.response import text
from sanic.exceptions import URLBuildError

@pytest.mark.parametrize('number', [3, -3, 13.123, -13.123])
def test_url_for_with_negative_number_message(app, number):
    @app.route("/url-for")
    def url_for(request):
        return text('url-for')

    u = app.url_for("url_for")
    assert u == "/url-for", u
    request, response = app.test_client.get(u)
    assert response.status == 200
    assert response.text == 'url-for'

@pytest.mark.parametrize('number', [0, 1, -1, 2.5, -2.5])
def test_url_for_with_zero_and_positive_negative_numbers(app, number):
    @app.route("/url-for/<possibly_neg:float>")
    def good(request, possibly_neg):
        assert isinstance(possibly_neg, (int, float))
        return text(f"this should pass with `{possibly_neg}`")

    u = app.url_for("good", possibly_neg=number)
    assert u == f"/url-for/{number}", u
    request, response = app.test_client.get(u)
    assert response.status == 200
    assert response.text == f"this should pass with `{float(number)}`"

def test_fails_if_endpoint_not_found(app):
    with pytest.raises(URLBuildError) as e:
        app.url_for("non_existent_endpoint")
        e.match("Endpoint with name `app.non_existent_endpoint` was not found")
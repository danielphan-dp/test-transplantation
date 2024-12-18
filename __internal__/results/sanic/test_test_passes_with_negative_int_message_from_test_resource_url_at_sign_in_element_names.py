import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.route('/url-for')
    def url_for(request):
        return text('url-for')

    return app

def test_url_for_basic(app):
    url = app.url_for('url_for')
    assert url == '/url-for', url
    request, response = app.test_client.get(url)
    assert response.status == 200
    assert response.text == 'url-for'

def test_url_for_with_query_params(app):
    @app.route('/url-with-params')
    def url_with_params(request):
        return text('params received')

    url = app.url_for('url_with_params', param1='value1', param2='value2')
    assert url == '/url-with-params?param1=value1&param2=value2', url
    request, response = app.test_client.get(url)
    assert response.status == 200
    assert response.text == 'params received'

def test_url_for_not_found(app):
    with pytest.raises(URLBuildError) as e:
        app.url_for('non_existent_view')
        assert str(e.value) == "Endpoint with name `non_existent_view` was not found"

def test_url_for_with_negative_int(app):
    @app.route('/path/<possibly_neg:int>/another-word')
    def good(request, possibly_neg):
        assert isinstance(possibly_neg, int)
        return text(f"this should pass with `{possibly_neg}`")

    u_plus_3 = app.url_for("good", possibly_neg=3)
    assert u_plus_3 == "/path/3/another-word", u_plus_3
    request, response = app.test_client.get(u_plus_3)
    assert response.text == "this should pass with `3`"

    u_neg_3 = app.url_for("good", possibly_neg=-3)
    assert u_neg_3 == "/path/-3/another-word", u_neg_3
    request, response = app.test_client.get(u_neg_3)
    assert response.text == "this should pass with `-3`"
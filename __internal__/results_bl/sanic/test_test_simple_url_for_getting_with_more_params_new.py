import pytest
from sanic import Sanic
from sanic.response import text

app = Sanic("TestApp")

@app.route('/url-for')
def url_for(request):
    return text('url-for')

@pytest.mark.parametrize('args,url', [
    ({"param1": "value1"}, "/url-for"),
    ({"param2": "value2"}, "/url-for"),
    ({"param1": "value1", "param2": "value2"}, "/url-for"),
    ({"param1": "", "param2": "value2"}, "/url-for"),
    ({"param1": "value1", "param2": None}, "/url-for"),
])
def test_url_for_with_params(app, args, url):
    assert url == app.url_for("url_for", **args)
    request, response = app.test_client.get(url)
    assert response.status == 200
    assert response.text == "url-for"

def test_url_for_invalid_route(app):
    request, response = app.test_client.get("/invalid-url")
    assert response.status == 404

def test_url_for_empty_params(app):
    request, response = app.test_client.get(app.url_for("url_for", param1=""))
    assert response.status == 200
    assert response.text == "url-for"
import pytest
from sanic import Sanic
from sanic.response import text
from sanic.exceptions import URLBuildError

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def test_url_for_with_valid_route(app):
    @app.route('/valid-url')
    def valid_route(request):
        return text("this should pass")

    url = app.url_for("valid_route")
    request, response = app.test_client.get(url)
    assert response.status == 200
    assert response.text == "this should pass"

def test_url_for_with_nonexistent_route(app):
    with pytest.raises(URLBuildError) as e:
        app.url_for("nonexistent_route")
    assert str(e.value) == "Endpoint with name `app.nonexistent_route` was not found"

def test_url_for_with_missing_parameters(app):
    @app.route('/user/<id:int>')
    def user_route(request, id):
        return text(f"User ID: {id}")

    with pytest.raises(URLBuildError) as e:
        app.url_for("user_route")
    assert str(e.value) == "Required parameter `id` was not passed to url_for"

def test_url_for_with_invalid_parameter_type(app):
    @app.route('/item/<item_id:int>')
    def item_route(request, item_id):
        return text(f"Item ID: {item_id}")

    with pytest.raises(URLBuildError) as e:
        app.url_for("item_route", item_id="not_an_int")
    expected_error = (
        r'Value "not_an_int" for parameter `item_id` '
        r"does not match pattern for type `int`: ^-?\d+$"
    )
    assert str(e.value) == expected_error

def test_url_for_with_server_name(app):
    server_name = "example.com"
    app.config.update({"SERVER_NAME": server_name})
    
    @app.route('/home')
    def home(request):
        return text("Welcome Home")

    url = f"http://{server_name}/home"
    assert url == app.url_for("home", _external=True)
    request, response = app.test_client.get(url)
    assert response.status == 200
    assert response.text == "Welcome Home"
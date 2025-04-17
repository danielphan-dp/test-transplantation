import pytest
from sanic import Sanic
from sanic.response import text

@pytest.mark.parametrize('view_name', ['url_for'])
def test_url_for_with_valid_view_name():
    app = Sanic("app")

    @app.route('/url-for')
    def url_for(request):
        return text('url-for')

    url = app.url_for(view_name)
    assert url == '/url-for'

    request, response = app.test_client.get(url)
    assert response.status == 200
    assert response.text == 'url-for'

def test_url_for_with_invalid_view_name():
    app = Sanic("app")

    with pytest.raises(Exception) as e:
        app.url_for("invalid_view")
        assert str(e.value) == "Endpoint with name `app.invalid_view` was not found"

def test_url_for_with_params():
    app = Sanic("app")

    @app.route('/user/<id>')
    def user(request, id):
        return text(f'User ID: {id}')

    url = app.url_for('user', id=123)
    assert url == '/user/123'

    request, response = app.test_client.get(url)
    assert response.status == 200
    assert response.text == 'User ID: 123'
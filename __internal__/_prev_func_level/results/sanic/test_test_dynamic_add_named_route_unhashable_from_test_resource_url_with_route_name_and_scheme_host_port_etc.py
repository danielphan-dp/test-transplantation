import pytest
from sanic import Sanic
from sanic.response import text
from sanic.exceptions import URLBuildError

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def test_url_for_with_valid_route(app):
    @app.route('/url-for', name='url_for_route')
    def url_for_handler(request):
        return text('url-for')

    url = app.url_for('url_for_route')
    assert url == '/url-for'

def test_url_for_with_nonexistent_route(app):
    with pytest.raises(URLBuildError) as e:
        app.url_for('nonexistent_route')
        assert str(e.value) == "Endpoint with name `app.nonexistent_route` was not found"

def test_url_for_with_parameters(app):
    @app.route('/folder/<name>', name='folder_route')
    def folder_handler(request, name):
        return text(f'Folder: {name}')

    url = app.url_for('folder_route', name='test_folder')
    assert url == '/folder/test_folder'

def test_url_for_with_invalid_parameters(app):
    @app.route('/item/<item_id:int>', name='item_route')
    def item_handler(request, item_id):
        return text(f'Item ID: {item_id}')

    with pytest.raises(URLBuildError) as e:
        app.url_for('item_route', item_id='invalid_id')
        assert str(e.value) == "Required parameter `item_id` was not passed to url_for"
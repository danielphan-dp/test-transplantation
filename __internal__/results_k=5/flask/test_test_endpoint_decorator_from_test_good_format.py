import pytest
import flask

@pytest.fixture
def app():
    app = flask.Flask(__name__)
    app.count = 0
    return app

def test_add_method_increments_count(app):
    assert app.count == 0
    app.add(app)
    assert app.count == 1
    app.add(app)
    assert app.count == 2

def test_add_method_multiple_calls(app):
    for _ in range(5):
        app.add(app)
    assert app.count == 5

def test_add_method_no_initialization(app):
    app.count = None
    with pytest.raises(TypeError):
        app.add(app)
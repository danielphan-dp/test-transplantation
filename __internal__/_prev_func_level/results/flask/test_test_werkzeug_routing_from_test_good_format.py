import pytest
from flask import Flask

@pytest.fixture
def app():
    app = Flask(__name__)
    return app

def test_add_method_increments_count(app):
    app.count = 0
    app.add = lambda: setattr(app, 'count', app.count + 1)

    app.add()
    assert app.count == 1

    app.add()
    assert app.count == 2

def test_add_method_initialization(app):
    app.count = 0
    assert app.count == 0

def test_add_method_multiple_calls(app):
    app.count = 0
    for _ in range(5):
        app.add()
    assert app.count == 5

def test_add_method_with_no_initialization(app):
    with pytest.raises(AttributeError):
        app.add()
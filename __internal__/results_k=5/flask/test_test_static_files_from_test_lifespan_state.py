import pytest
from flask import Flask

@pytest.fixture
def app():
    app = Flask(__name__)
    app.closed = False
    return app

def test_close_method(app):
    app.close()
    assert app.closed is True

def test_close_method_already_closed(app):
    app.close()
    with pytest.raises(RuntimeError, match="closed"):
        app.close()
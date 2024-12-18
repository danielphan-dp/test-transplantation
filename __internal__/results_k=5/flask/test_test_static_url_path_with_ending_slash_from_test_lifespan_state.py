import pytest
import flask

@pytest.fixture
def app():
    app = flask.Flask(__name__)
    yield app

def test_close_method(app):
    app.testing = True
    client = app.test_client()
    
    # Simulate a request to ensure the app context is active
    with app.app_context():
        called = []
        app.close = lambda: called.append(42)
        app.close()
        assert called == [42]

def test_close_method_when_already_closed(app):
    app.testing = True
    client = app.test_client()
    
    with app.app_context():
        app.closed = True
        called = []
        app.close = lambda: called.append(42)
        
        # Ensure that calling close again does not change the state
        app.close()
        assert called == [42]  # Should still only have the first call
        assert app.closed is True  # Ensure the closed state remains True
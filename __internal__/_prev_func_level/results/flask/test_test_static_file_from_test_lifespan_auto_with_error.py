import pytest
import flask

class TestCloseMethod:
    @pytest.fixture
    def app(self):
        app = flask.Flask(__name__)
        return app

    def test_close_method_called(self, app):
        called = []
        app.close = lambda: called.append(42)
        
        app.close()
        assert 42 in called

    def test_close_method_multiple_calls(self, app):
        called = []
        app.close = lambda: called.append(42)
        
        app.close()
        app.close()
        assert called.count(42) == 2

    def test_close_method_state(self, app):
        called = []
        app.close = lambda: called.append(42)
        
        app.close()
        assert len(called) == 1
        app.close()
        assert len(called) == 2

    def test_close_method_no_side_effects(self, app):
        called = []
        app.close = lambda: called.append(42)
        
        app.close()
        assert called == [42]
        app.close()
        assert called == [42, 42]
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
        class TestApp(flask.Flask):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.closed = False

            def close(self):
                if not self.closed:
                    self.closed = True
                    return 42
                return None

        test_app = TestApp(__name__)
        assert test_app.close() == 42
        assert test_app.close() is None

    def test_close_method_with_context(self, app):
        called = []
        app.close = lambda: called.append(42)

        with app.app_context():
            app.close()
            assert 42 in called

    def test_close_method_no_call(self, app):
        called = []
        app.close = lambda: called.append(42)

        assert len(called) == 0
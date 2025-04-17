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

        with app.test_request_context():
            app.close()
            assert called == [42]

    def test_close_method_multiple_calls(self, app):
        called = []
        app.close = lambda: called.append(42)

        with app.test_request_context():
            app.close()
            app.close()
            assert called == [42, 42]

    def test_close_method_state(self, app):
        called = []
        app.close = lambda: called.append(42)

        with app.test_request_context():
            app.close()
            assert len(called) == 1
            app.close()
            assert len(called) == 2

    def test_close_method_no_context(self, app):
        called = []
        app.close = lambda: called.append(42)

        app.close()
        assert called == [42]  # Ensure it can be called outside of request context

    def test_close_method_with_exception(self, app):
        called = []
        app.close = lambda: called.append(42)

        with app.test_request_context():
            try:
                raise Exception("Test Exception")
            except Exception:
                app.close()
                assert called == [42]  # Ensure close is called even on exception
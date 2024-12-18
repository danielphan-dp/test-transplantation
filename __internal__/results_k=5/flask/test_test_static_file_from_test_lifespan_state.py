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
                    return True
                return False

        test_app = TestApp(__name__)
        assert test_app.close() is True
        assert test_app.close() is False

    def test_close_method_with_context(self, app):
        class TestApp(flask.Flask):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.closed = False

            def close(self):
                self.closed = True

        test_app = TestApp(__name__)
        with test_app.app_context():
            test_app.close()
            assert test_app.closed is True

    def test_close_method_no_double_close(self, app):
        class TestApp(flask.Flask):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.closed = False

            def close(self):
                if not self.closed:
                    self.closed = True

        test_app = TestApp(__name__)
        test_app.close()
        assert test_app.closed is True
        test_app.close()  # Should not raise an error
        assert test_app.closed is True
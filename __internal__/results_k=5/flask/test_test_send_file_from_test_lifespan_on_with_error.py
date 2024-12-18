import pytest
from flask import Flask

@pytest.fixture
def app():
    app = Flask(__name__)
    return app

def test_close_method(app):
    called = []
    
    class TestClass:
        def close(self):
            called.append(42)

    instance = TestClass()
    instance.close()
    assert 42 in called

def test_close_method_already_called(app):
    called = []
    
    class TestClass:
        def close(self):
            if 42 in called:
                raise RuntimeError("Close method already called")
            called.append(42)

    instance = TestClass()
    instance.close()
    
    with pytest.raises(RuntimeError) as excinfo:
        instance.close()
    assert "Close method already called" in str(excinfo.value)
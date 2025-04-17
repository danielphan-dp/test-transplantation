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
    assert not hasattr(instance, 'closed')
    
    instance.close()
    assert called == [42]
    
    instance.closed = True
    assert instance.closed is True

def test_close_method_already_closed(app):
    called = []
    
    class TestClass:
        def close(self):
            called.append(42)
            if hasattr(self, 'closed') and self.closed:
                raise RuntimeError("Already closed")

    instance = TestClass()
    instance.closed = True
    
    with pytest.raises(RuntimeError, match="Already closed"):
        instance.close()
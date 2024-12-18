import pytest
from flask import Flask

@pytest.fixture
def app():
    app = Flask(__name__)
    return app

def test_close_method(app):
    called = []
    
    class TestClass:
        closed = False
        
        def close(self):
            called.append(42)
            assert not self.closed
            self.closed = True

    test_instance = TestClass()
    test_instance.close()
    
    assert test_instance.closed
    assert 42 in called

def test_close_method_already_closed(app):
    called = []
    
    class TestClass:
        closed = True
        
        def close(self):
            called.append(42)
            assert self.closed
            self.closed = True

    test_instance = TestClass()
    test_instance.close()
    
    assert test_instance.closed
    assert 42 in called
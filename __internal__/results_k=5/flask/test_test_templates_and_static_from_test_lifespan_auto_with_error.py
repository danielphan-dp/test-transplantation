import pytest
from blueprintapp import app

@pytest.fixture
def client():
    return app.test_client()

def test_close_method(client):
    called = []
    
    class TestClose:
        def close(self):
            called.append(42)

    test_instance = TestClose()
    assert not hasattr(test_instance, 'closed')
    
    test_instance.close()
    assert 42 in called
    assert hasattr(test_instance, 'closed')  # Check if closed attribute is set after close method is called

def test_close_method_multiple_calls(client):
    called = []
    
    class TestClose:
        def close(self):
            called.append(42)

    test_instance = TestClose()
    test_instance.close()
    test_instance.close()  # Call close again
    assert called.count(42) == 2  # Ensure close was called twice

def test_close_method_state(client):
    called = []
    
    class TestClose:
        def __init__(self):
            self.closed = False

        def close(self):
            if not self.closed:
                called.append(42)
                self.closed = True

    test_instance = TestClose()
    test_instance.close()
    assert test_instance.closed is True  # Check if closed state is set
    test_instance.close()  # Call close again
    assert called.count(42) == 1  # Ensure close was only called once
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
    assert called == [42]
    
    # Simulate closing again
    test_instance.closed = True
    with pytest.raises(RuntimeError):
        test_instance.close()  # Ensure it raises an error if already closed

    # Check if the close method sets the closed attribute
    assert test_instance.closed is True
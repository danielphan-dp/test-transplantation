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
    test_instance.close()
    assert called == [42]

def test_close_method_already_called(client):
    called = []
    
    class TestClose:
        def close(self):
            if not hasattr(self, 'closed'):
                called.append(42)
                self.closed = True

    test_instance = TestClose()
    test_instance.close()
    assert called == [42]
    test_instance.close()  # Call again to check it doesn't append
    assert called == [42]  # Should still be the same

def test_close_method_with_error(client):
    called = []
    
    class TestClose:
        def close(self):
            if not hasattr(self, 'closed'):
                called.append(42)
                self.closed = True
            else:
                raise RuntimeError("Already closed")

    test_instance = TestClose()
    test_instance.close()
    assert called == [42]
    with pytest.raises(RuntimeError) as excinfo:
        test_instance.close()
    assert str(excinfo.value) == "Already closed"
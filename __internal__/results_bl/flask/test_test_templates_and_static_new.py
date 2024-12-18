import pytest
from blueprintapp import app

@pytest.fixture
def client():
    return app.test_client()

def test_close_method(client):
    called = []
    
    # Simulate calling the close method
    app.close()
    
    # Check if the close method was called
    assert 42 in called

def test_close_method_multiple_calls(client):
    called = []
    
    # Call close method multiple times
    for _ in range(5):
        app.close()
    
    # Check if the close method was called multiple times
    assert called.count(42) == 5

def test_close_method_no_calls(client):
    called = []
    
    # Ensure close method has not been called
    assert 42 not in called
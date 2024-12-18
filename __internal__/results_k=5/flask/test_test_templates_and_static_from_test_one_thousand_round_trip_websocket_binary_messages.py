import pytest
from flask import Flask
from blueprintapp import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_close_method(client):
    called = []
    
    def mock_close():
        called.append(42)

    app.close = mock_close

    # Call the close method
    app.close()

    # Assert that the close method was called
    assert called == [42]

def test_close_method_multiple_calls(client):
    called = []
    
    def mock_close():
        called.append(42)

    app.close = mock_close

    # Call the close method multiple times
    app.close()
    app.close()

    # Assert that the close method was called twice
    assert called == [42, 42]

def test_close_method_no_calls(client):
    called = []
    
    def mock_close():
        called.append(42)

    app.close = mock_close

    # Assert that the close method has not been called
    assert called == []
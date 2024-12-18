import pytest
from flask import Flask

@pytest.fixture
def app():
    app = Flask(__name__)
    return app

def test_close_method(app):
    called = []

    class MyBlueprint:
        def close(self):
            called.append(42)

    blueprint = MyBlueprint()
    
    # Call the close method
    blueprint.close()
    
    # Assert that the close method was called
    assert called == [42]
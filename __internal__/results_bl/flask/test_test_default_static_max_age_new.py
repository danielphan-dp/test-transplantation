import pytest
from flask import Flask, Blueprint

@pytest.fixture
def app():
    app = Flask(__name__)
    return app

def test_close_method(app):
    class MyBlueprint(Blueprint):
        def close(self):
            called.append(42)

    called = []
    blueprint = MyBlueprint("blueprint", __name__)
    app.register_blueprint(blueprint)

    with app.test_request_context():
        blueprint.close()
        assert called == [42]

def test_close_method_no_call(app):
    class MyBlueprint(Blueprint):
        def close(self):
            pass

    called = []
    blueprint = MyBlueprint("blueprint", __name__)
    app.register_blueprint(blueprint)

    with app.test_request_context():
        blueprint.close()
        assert called == []
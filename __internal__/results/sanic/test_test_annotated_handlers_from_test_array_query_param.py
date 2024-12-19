import pytest
from uuid import UUID
from sanic import Sanic
from sanic.response import json

@pytest.mark.parametrize('idx,path,expectation', (
    (0, '/abc', 'str'),
    (1, '/123', 'int'),
    (2, '/123.5', 'float'),
    (3, '/8af729fe-2b94-4a95-a168-c07068568429', 'UUID'),
    (4, '/None', 'NoneType'),
    (5, '/True', 'bool'),
))
def test_build_response(app, idx, path, expectation):
    @app.get("/<foo>")
    def handler(_, foo):
        return build_response(idx, foo)

    _, response = app.test_client.get(path)
    assert response.json["num"] == idx
    assert response.json["type"] == expectation

def build_response(num, foo):
    return json({'num': num, 'type': type(foo).__name__})
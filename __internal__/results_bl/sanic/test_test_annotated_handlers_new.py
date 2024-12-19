import uuid
import pytest
from sanic import Sanic
from sanic.response import json

app = Sanic("TestApp")

@pytest.mark.parametrize('idx,path,expectation', [
    (0, '/abc', 'str'),
    (1, '/123', 'int'),
    (2, '/123.5', 'float'),
    (3, '/8af729fe-2b94-4a95-a168-c07068568429', 'UUID'),
    (4, '/None', 'NoneType'),
    (5, '/True', 'bool'),
    (6, '/False', 'bool'),
    (7, '/[1, 2, 3]', 'list'),
    (8, '/{"key": "value"}', 'dict'),
])
def test_annotated_handlers(app, idx, path, expectation):
    def build_response(num, foo):
        return json({"num": num, "type": type(foo).__name__})

    @app.get("/<foo>")
    def handler0(_, foo: str):
        return build_response(0, foo)

    @app.get("/<foo>")
    def handler1(_, foo: int):
        return build_response(1, foo)

    @app.get("/<foo>")
    def handler2(_, foo: float):
        return build_response(2, foo)

    @app.get("/<foo>")
    def handler3(_, foo: uuid.UUID):
        return build_response(3, foo)

    @app.get("/<foo>")
    def handler4(_, foo: None):
        return build_response(4, foo)

    @app.get("/<foo>")
    def handler5(_, foo: bool):
        return build_response(5, foo)

    @app.get("/<foo>")
    def handler6(_, foo: list):
        return build_response(6, foo)

    @app.get("/<foo>")
    def handler7(_, foo: dict):
        return build_response(7, foo)

    _, response = app.test_client.get(path)
    assert response.json["num"] == idx
    assert response.json["type"] == expectation
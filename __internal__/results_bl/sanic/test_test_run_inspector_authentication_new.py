import pytest
from unittest.mock import Mock
from sanic_testing import TestManager
from sanic.worker.inspector import Inspector
from sanic.helpers import Default

def test_get_method_without_authentication():
    inspector = Inspector(Mock(), {}, {}, "", 0, "super-secret", Default(), Default())(False)
    manager = TestManager(inspector.app)
    _, response = manager.test_client.get("/")
    assert response.status == 401

def test_get_method_with_invalid_authentication():
    inspector = Inspector(Mock(), {}, {}, "", 0, "super-secret", Default(), Default())(False)
    manager = TestManager(inspector.app)
    _, response = manager.test_client.get("/", headers={"Authorization": "Bearer invalid-token"})
    assert response.status == 401

def test_get_method_with_valid_authentication():
    inspector = Inspector(Mock(), {}, {}, "", 0, "super-secret", Default(), Default())(False)
    manager = TestManager(inspector.app)
    _, response = manager.test_client.get("/", headers={"Authorization": "Bearer super-secret"})
    assert response.status == 200

def test_get_method_response_content():
    inspector = Inspector(Mock(), {}, {}, "", 0, "super-secret", Default(), Default())(False)
    manager = TestManager(inspector.app)
    _, response = manager.test_client.get("/", headers={"Authorization": "Bearer super-secret"})
    assert response.text == 'I am get method'
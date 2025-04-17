import pytest
from docs_src.app_testing.app_b_an_py310 import test_main

@pytest.mark.needs_py310
def test_create_item_with_missing_fields():
    client = test_main.get_app_client()
    response = client.post('/items/', json={'name': 'Foo'})
    assert response.status_code == 422, response.text
    assert response.json() == {
        "detail": [
            {
                "type": "missing",
                "loc": ["body", "price"],
                "msg": "Field required",
                "input": {"name": "Foo"},
            }
        ]
    }

@pytest.mark.needs_py310
def test_create_item_with_invalid_data_type():
    client = test_main.get_app_client()
    response = client.post('/items/', json={'name': 'Foo', 'price': 'not_a_number'})
    assert response.status_code == 422, response.text
    assert response.json() == {
        "detail": [
            {
                "type": "type_error.float",
                "loc": ["body", "price"],
                "msg": "value is not a valid float",
                "input": "not_a_number",
            }
        ]
    }

@pytest.mark.needs_py310
def test_create_item_with_extra_fields():
    client = test_main.get_app_client()
    response = client.post('/items/', json={'name': 'Foo', 'price': 50.5, 'extra_field': 'extra_value'})
    assert response.status_code == 200, response.text
    assert response.json() == {
        'name': 'Foo',
        'description': None,
        'price': 50.5,
        'tax': None,
    }

@pytest.mark.needs_py310
def test_create_item_with_empty_name():
    client = test_main.get_app_client()
    response = client.post('/items/', json={'name': '', 'price': 50.5})
    assert response.status_code == 422, response.text
    assert response.json() == {
        "detail": [
            {
                "type": "value_error.string.min_length",
                "loc": ["body", "name"],
                "msg": "String should have at least 1 characters",
                "input": "",
            }
        ]
    }
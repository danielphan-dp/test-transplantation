import pytest
from docs_src.app_testing.app_b_an_py310 import test_main

@pytest.mark.needs_py310
def test_create_item_edge_cases():
    client = test_main.get_app_client()
    
    # Test with an empty name
    response_empty_name = client.post('/items/', json={'name': ''})
    assert response_empty_name.status_code == 400, response_empty_name.text
    
    # Test with a very long name
    long_name = 'A' * 256
    response_long_name = client.post('/items/', json={'name': long_name})
    assert response_long_name.status_code == 400, response_long_name.text
    
    # Test with special characters
    response_special_chars = client.post('/items/', json={'name': '@#$%^&*()'})
    assert response_special_chars.status_code == 200, response_special_chars.text
    assert response_special_chars.json() == {'name': '@#$%^&*()', 'description': None, 'sub': None}

    # Test with missing name field
    response_missing_field = client.post('/items/', json={})
    assert response_missing_field.status_code == 422, response_missing_field.text

    # Test with a valid name but additional unexpected fields
    response_unexpected_fields = client.post('/items/', json={'name': 'Plumbus', 'extra_field': 'value'})
    assert response_unexpected_fields.status_code == 200, response_unexpected_fields.text
    assert response_unexpected_fields.json() == {'name': 'Plumbus', 'description': None, 'sub': None}
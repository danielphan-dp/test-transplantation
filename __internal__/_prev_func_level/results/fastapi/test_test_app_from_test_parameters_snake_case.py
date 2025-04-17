import pytest
from docs_src.app_testing.app_b_an_py310 import test_main

@pytest.mark.needs_py310
def test_create_item_with_missing_name(client):
    response = client.post('/items/', json={'description': 'Missing name'})
    assert response.status_code == 422
    assert response.json()['detail'][0]['msg'] == 'Field required'

@pytest.mark.needs_py310
def test_create_item_with_invalid_price(client):
    response = client.post('/items/', json={'name': 'Plumbus', 'price': 'invalid'})
    assert response.status_code == 422
    assert response.json()['detail'][0]['msg'] == 'value is not a valid float'

@pytest.mark.needs_py310
def test_create_item_with_extra_fields(client):
    response = client.post('/items/', json={'name': 'Plumbus', 'description': 'A description', 'extra_field': 'extra'})
    assert response.status_code == 200
    assert response.json() == {'name': 'Plumbus', 'description': 'A description', 'sub': None}

@pytest.mark.needs_py310
def test_create_item_with_none_price(client):
    response = client.post('/items/', json={'name': 'Plumbus', 'price': None})
    assert response.status_code == 422
    assert response.json()['detail'][0]['msg'] == 'none is not an allowed value'

@pytest.mark.needs_py310
def test_create_item_with_sub(client):
    data = {
        'name': 'Plumbus',
        'sub': {'subname': 'SubPlumbus', 'sub_description': 'Sub WTF'}
    }
    response = client.post('/items/', json=data)
    assert response.status_code == 200
    assert response.json() == {
        'name': 'Plumbus',
        'description': None,
        'sub': {'subname': 'SubPlumbus', 'sub_description': 'Sub WTF', 'tags': []}
    }
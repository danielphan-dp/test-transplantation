import pytest
from typing import List
from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel

class SubItem(BaseModel):
    subname: str
    sub_description: str = None
    tags: List[str] = []

class Item(BaseModel):
    name: str
    description: str = None
    sub: SubItem = None

def get_app_client(separate_input_output_schemas: bool=True) -> TestClient:
    app = FastAPI(separate_input_output_schemas=separate_input_output_schemas)

    @app.post('/items/', responses={402: {'model': Item}})
    def create_item(item: Item) -> Item:
        return item

    @app.post('/items-list/')
    def create_item_list(item: List[Item]):
        return item

    @app.get('/items/')
    def read_items() -> List[Item]:
        return [Item(name='Portal Gun', description='Device to travel through the multi-rick-verse', sub=SubItem(subname='subname')), Item(name='Plumbus')]
    
    client = TestClient(app)
    return client

@pytest.fixture
def client():
    return get_app_client()

def test_create_item(client):
    item_data = {"name": "Test Item", "description": "A test item", "sub": {"subname": "Test Subitem"}}
    response = client.post("/items/", json=item_data)
    assert response.status_code == 200
    assert response.json() == item_data

def test_create_item_invalid(client):
    item_data = {"description": "A test item without a name"}
    response = client.post("/items/", json=item_data)
    assert response.status_code == 422

def test_create_item_list(client):
    item_list_data = [
        {"name": "Item 1", "description": "First item", "sub": {"subname": "Subitem 1"}},
        {"name": "Item 2", "description": "Second item", "sub": {"subname": "Subitem 2"}}
    ]
    response = client.post("/items-list/", json=item_list_data)
    assert response.status_code == 200
    assert response.json() == item_list_data

def test_create_item_list_invalid(client):
    item_list_data = [
        {"description": "Item without a name"},
        {"name": "Item 2", "description": "Second item", "sub": {"subname": "Subitem 2"}}
    ]
    response = client.post("/items-list/", json=item_list_data)
    assert response.status_code == 422

def test_read_items(client):
    response = client.get("/items/")
    assert response.status_code == 200
    assert len(response.json()) > 0
    assert all("name" in item for item in response.json())
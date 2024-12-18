import pytest
from fastapi.testclient import TestClient
from typing import List, Optional
from pydantic import BaseModel
from fastapi import FastAPI

class SubItem(BaseModel):
    subname: str
    sub_description: Optional[str] = None
    tags: List[str] = []

class Item(BaseModel):
    name: str
    description: Optional[str] = None
    sub: Optional[SubItem] = None

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

def test_create_item_with_missing_fields():
    client = get_app_client()
    response = client.post("/items/", json={"name": "Test Item"})
    assert response.status_code == 200, response.text
    assert response.json() == {"name": "Test Item", "description": None, "sub": None}

def test_create_item_with_subitem():
    client = get_app_client()
    response = client.post("/items/", json={"name": "Test Item", "sub": {"subname": "Sub Item"}})
    assert response.status_code == 200, response.text
    assert response.json() == {"name": "Test Item", "description": None, "sub": {"subname": "Sub Item", "sub_description": None, "tags": []}}

def test_create_item_list():
    client = get_app_client()
    items = [{"name": "Item 1"}, {"name": "Item 2", "description": "Description 2"}]
    response = client.post("/items-list/", json=items)
    assert response.status_code == 200, response.text
    assert response.json() == items

def test_create_item_with_invalid_data():
    client = get_app_client()
    response = client.post("/items/", json={"invalid_field": "value"})
    assert response.status_code == 422, response.text

def test_read_items_empty():
    client = get_app_client()
    response = client.get("/items/")
    assert response.status_code == 200, response.text
    assert len(response.json()) == 2  # Expecting two items in the response

def test_read_items_structure():
    client = get_app_client()
    response = client.get("/items/")
    assert response.status_code == 200, response.text
    assert isinstance(response.json(), list)
    assert all("name" in item for item in response.json())
    assert all("description" in item for item in response.json())
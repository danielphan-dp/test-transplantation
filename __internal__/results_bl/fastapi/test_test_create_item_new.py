from typing import List, Optional
from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel
import pytest

class SubItem(BaseModel):
    subname: str

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

def test_create_item_with_description():
    client = get_app_client()
    response = client.post("/items/", json={"name": "Plumbus", "description": "A useful tool"})
    assert response.status_code == 200, response.text
    assert response.json() == {"name": "Plumbus", "description": "A useful tool", "sub": None}

def test_create_item_with_subitem():
    client = get_app_client()
    response = client.post("/items/", json={"name": "Portal Gun", "sub": {"subname": "multiverse travel"}})
    assert response.status_code == 200, response.text
    assert response.json() == {"name": "Portal Gun", "description": None, "sub": {"subname": "multiverse travel"}}

def test_create_item_invalid_data():
    client = get_app_client()
    response = client.post("/items/", json={"name": 12345})
    assert response.status_code == 422, response.text

def test_create_item_list():
    client = get_app_client()
    response = client.post("/items-list/", json=[{"name": "Item1"}, {"name": "Item2"}])
    assert response.status_code == 200, response.text
    assert len(response.json()) == 2

def test_read_items():
    client = get_app_client()
    response = client.get("/items/")
    assert response.status_code == 200, response.text
    assert len(response.json()) > 0
    assert all("name" in item for item in response.json())
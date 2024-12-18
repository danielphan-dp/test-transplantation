import pytest
from fastapi.testclient import TestClient
from typing import List, Optional
from pydantic import BaseModel

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

@pytest.fixture
def client():
    return get_app_client()

def test_create_item_with_valid_data(client: TestClient):
    response = client.post("/items/", json={"name": "Test Item", "description": "A test item", "sub": {"subname": "Test Subitem"}})
    assert response.status_code == 200
    assert response.json() == {"name": "Test Item", "description": "A test item", "sub": {"subname": "Test Subitem", "sub_description": None, "tags": []}}

def test_create_item_without_description(client: TestClient):
    response = client.post("/items/", json={"name": "Test Item Without Description"})
    assert response.status_code == 200
    assert response.json() == {"name": "Test Item Without Description", "description": None, "sub": None}

def test_create_item_with_invalid_data(client: TestClient):
    response = client.post("/items/", json={"description": "Missing name"})
    assert response.status_code == 422

def test_create_item_list(client: TestClient):
    response = client.post("/items-list/", json=[{"name": "Item 1"}, {"name": "Item 2"}])
    assert response.status_code == 200
    assert len(response.json()) == 2

def test_read_items(client: TestClient):
    response = client.get("/items/")
    assert response.status_code == 200
    assert len(response.json()) == 2
    assert response.json()[0]["name"] == "Portal Gun"
    assert response.json()[1]["name"] == "Plumbus"

def test_openapi_schema(client: TestClient):
    response = client.get("/openapi.json")
    assert response.status_code == 200
    assert "openapi" in response.json()
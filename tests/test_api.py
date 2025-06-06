from fastapi.testclient import TestClient
from src.api.main import app
from src.patterns.singleton import EquipmentInventory

client = TestClient(app)

def test_health_check():
    """Test the health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_create_equipment():
    """Test creating new equipment."""
    equipment_data = {
        "name": "Test Equipment",
        "description": "Test Description",
        "base_price": 999.99,
        "category": "Test Category",
        "specs": {
            "weight": "75.0",
            "dimensions": "200x100x220",
            "material": "Steel",
            "color": "Black",
            "max_user_weight": "150.0",
            "warranty_months": "12"
        }
    }
    
    response = client.post("/equipment/", json=equipment_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == equipment_data["name"]
    assert data["description"] == equipment_data["description"]
    assert data["base_price"] == equipment_data["base_price"]
    assert data["category"] == equipment_data["category"]
    
    # Fix: Handle both string and numeric responses for specs
    assert str(data["specs"]["weight"]) == equipment_data["specs"]["weight"]
    assert data["specs"]["dimensions"] == equipment_data["specs"]["dimensions"]
    assert data["specs"]["material"] == equipment_data["specs"]["material"]
    assert data["specs"]["color"] == equipment_data["specs"]["color"]
    assert str(data["specs"]["max_user_weight"]) == equipment_data["specs"]["max_user_weight"]
    assert str(data["specs"]["warranty_months"]) == equipment_data["specs"]["warranty_months"]


def test_get_equipment():
    """Test getting equipment list."""
    response = client.get("/equipment")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_equipment_by_id():
    """Test getting equipment by ID."""
    # First create equipment
    equipment_data = {
        "name": "Test Equipment",
        "description": "Test Description",
        "base_price": 999.99,
        "category": "Test Category",
        "specs": {
            "weight": "75.0",
            "dimensions": "200x100x220",
            "material": "Steel",
            "color": "Black",
            "max_user_weight": "150.0",
            "warranty_months": "12"
        }
    }
    
    create_response = client.post("/equipment/", json=equipment_data)
    assert create_response.status_code == 200
    equipment_id = create_response.json()["id"]
    
    # Then get it by ID
    response = client.get(f"/equipment/{equipment_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == equipment_data["name"]
    assert data["description"] == equipment_data["description"]
    assert data["base_price"] == equipment_data["base_price"]
    assert data["category"] == equipment_data["category"]

def test_decorate_nonexistent_equipment():
    """Test decorating non-existent equipment."""
    response = client.post(
        "/equipment/999/decorate",
        json={
            "decoration_type": "warranty",
            "warranty_months": 24
        }
    )
    assert response.status_code == 404  # Not Found
    assert "Equipment not found" in response.json()["detail"]

def test_invalid_decoration_type():
    """Test invalid decoration type."""
    # First create some equipment
    response = client.post(
        "/equipment/",
        json={
            "name": "Professional Treadmill",
            "description": "High-end treadmill for professional use",
            "base_price": 2999.99,
            "category": "cardio",
            "specs": {
                "weight": "100",
                "dimensions": "200x80x140",
                "material": "Steel and Aluminum",
                "color": "Black",
                "max_user_weight": "180",
                "warranty_months": "24"
            }
        }
    )
    assert response.status_code == 200
    equipment_id = response.json()["id"]

    response = client.post(
        f"/equipment/{equipment_id}/decorate",
        json={
            "decoration_type": "invalid_type"
        }
    )
    assert response.status_code == 400
    assert "invalid decoration type" in response.json()["detail"].lower()
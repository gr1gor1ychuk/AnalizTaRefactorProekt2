"""Tests for equipment models."""
import pytest
from src.models.equipment import Equipment, EquipmentSpecs

class TestEquipment:
    """Test cases for Equipment class."""
    def setup_method(self):
        """Set up test fixtures."""
        self.equipment = Equipment(
            name="Test Equipment",
            description="Test Description",
            base_price=999.99,
            category="Test Category",
            specs=EquipmentSpecs(
                weight="75.0",
                dimensions="200x100x220",
                material="Steel",
                color="Black",
                max_user_weight="150.0",
                warranty_months="12"
            )
        )

    def test_valid_equipment(self):
        """Test creating valid equipment"""
        assert self.equipment.name == "Test Equipment"
        assert self.equipment.description == "Test Description"
        assert self.equipment.base_price == 999.99
        assert self.equipment.category == "Test Category"
        assert isinstance(self.equipment.specs, EquipmentSpecs)
        assert self.equipment.specs.weight == "75.0"
        assert self.equipment.specs.dimensions == "200x100x220"
        assert self.equipment.specs.material == "Steel"
        assert self.equipment.specs.color == "Black"
        assert self.equipment.specs.max_user_weight == "150.0"
        assert self.equipment.specs.warranty_months == "12"

    def test_invalid_name(self):
        """Test invalid equipment name"""
        with pytest.raises(ValueError):
            Equipment(
                name="",
                description="Test Description",
                base_price=999.99,
                category="Test Category",
                specs=EquipmentSpecs(
                    weight="75.0",
                    dimensions="200x100x220",
                    material="Steel",
                    color="Black",
                    max_user_weight="150.0",
                    warranty_months="12"
                )
            )

    def test_invalid_description(self):
        """Test invalid equipment description"""
        with pytest.raises(ValueError):
            Equipment(
                name="Test Equipment",
                description="",
                base_price=999.99,
                category="Test Category",
                specs=EquipmentSpecs(
                    weight="75.0",
                    dimensions="200x100x220",
                    material="Steel",
                    color="Black",
                    max_user_weight="150.0",
                    warranty_months="12"
                )
            )

    def test_invalid_base_price(self):
        """Test invalid base price"""
        with pytest.raises(ValueError):
            Equipment(
                name="Test Equipment",
                description="Test Description",
                base_price=-999.99,
                category="Test Category",
                specs=EquipmentSpecs(
                    weight="75.0",
                    dimensions="200x100x220",
                    material="Steel",
                    color="Black",
                    max_user_weight="150.0",
                    warranty_months="12"
                )
            )

    def test_invalid_category(self):
        """Test invalid category"""
        with pytest.raises(ValueError):
            Equipment(
                name="Test Equipment",
                description="Test Description",
                base_price=999.99,
                category="",
                specs=EquipmentSpecs(
                    weight="75.0",
                    dimensions="200x100x220",
                    material="Steel",
                    color="Black",
                    max_user_weight="150.0",
                    warranty_months="12"
                )
            )

    def test_invalid_specs(self):
        """Test invalid specs"""
        with pytest.raises(ValueError):
            Equipment(
                name="Test Equipment",
                description="Test Description",
                base_price=999.99,
                category="Test Category",
                specs=None
            )

    def test_float_conversion(self):
        """Test float conversion for numeric fields"""
        equipment = Equipment(
            name="Test Equipment",
            description="Test Description",
            base_price="999.99",
            category="Test Category",
            specs=EquipmentSpecs(
                weight="75.0",
                dimensions="200x100x220",
                material="Steel",
                color="Black",
                max_user_weight="150.0",
                warranty_months="12"
            )
        )
        assert isinstance(equipment.base_price, float)
        assert equipment.specs.weight == "75.0"
        assert equipment.specs.max_user_weight == "150.0"
        assert equipment.specs.warranty_months == "12"

    def test_string_representation(self):
        """Test string representation of equipment"""
        assert str(self.equipment) == "Test Equipment (Test Category) - $999.99"

    def test_to_dict(self):
        """Test converting equipment to dictionary"""
        equipment_dict = self.equipment.to_dict()
        assert equipment_dict["name"] == "Test Equipment"
        assert equipment_dict["description"] == "Test Description"
        assert equipment_dict["base_price"] == 999.99
        assert equipment_dict["category"] == "Test Category"
        assert isinstance(equipment_dict["specs"], dict)
        assert equipment_dict["specs"]["weight"] == "75.0"
        assert equipment_dict["specs"]["dimensions"] == "200x100x220"

    def test_from_dict(self):
        """Test creating equipment from dictionary"""
        data = {
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
        equipment = Equipment.from_dict(data)
        assert equipment.name == "Test Equipment"
        assert equipment.description == "Test Description"
        assert equipment.base_price == 999.99
        assert equipment.category == "Test Category"
        assert isinstance(equipment.specs, EquipmentSpecs)
        assert equipment.specs.weight == "75.0"
        assert equipment.specs.dimensions == "200x100x220"
        assert equipment.specs.material == "Steel"
        assert equipment.specs.color == "Black"
        assert equipment.specs.max_user_weight == "150.0"
        assert equipment.specs.warranty_months == "12" 
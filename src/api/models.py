from typing import List, Optional, Dict, Any
from pydantic import BaseModel, validator
from datetime import datetime
from src.models.equipment import EquipmentSpecs

class ColorInfo(BaseModel):
    code: str
    name: str

class EquipmentSpecsAPI(BaseModel):
    """API model for equipment specifications."""
    weight: str
    dimensions: str
    material: str
    color: str
    max_user_weight: str
    warranty_months: str

    @validator('weight', 'max_user_weight', pre=True)
    def validate_numeric_string(cls, v):
        """Validate numeric string values."""
        if isinstance(v, (int, float)):
            return str(v)
        return v

    @validator('warranty_months', pre=True)
    def validate_warranty_months(cls, v):
        """Validate warranty months."""
        if isinstance(v, int):
            return str(v)
        return v

    def to_domain(self) -> EquipmentSpecs:
        """Convert to domain model."""
        return EquipmentSpecs(
            weight=self.weight,
            dimensions=self.dimensions,
            material=self.material,
            color=self.color,
            max_user_weight=self.max_user_weight,
            warranty_months=self.warranty_months
        )

    @classmethod
    def from_domain(cls, specs: EquipmentSpecs) -> 'EquipmentSpecsAPI':
        """Create from domain model."""
        return cls(
            weight=specs.weight,
            dimensions=specs.dimensions,
            material=specs.material,
            color=specs.color,
            max_user_weight=specs.max_user_weight,
            warranty_months=specs.warranty_months
        )

class EquipmentModel(BaseModel):
    name: str
    description: str
    base_price: float
    category: str
    specs: Dict[str, Any]

class CreateOrderModel(BaseModel):
    equipment_id: str
    quantity: int
    customer_id: str
    customer_email: str  # Added missing field
    shipping_address: str  # Added missing field
    color: Optional[str] = None

class OrderModel(BaseModel):
    id: str
    customer_id: str
    equipment_id: str
    quantity: int
    total_amount: float
    status: str
    created_at: datetime

class OrderResponse(BaseModel):
    id: str
    equipment_id: str
    customer_id: str
    quantity: int
    status: str
    created_at: datetime

class DecorationInfo(BaseModel):
    type: str  # "warranty", "installation", "maintenance", "insurance"
    years: Optional[int] = None  # For warranty
    months: Optional[int] = None  # For maintenance
    coverage_type: Optional[str] = None  # For insurance: "basic", "standard", "premium"

class EquipmentDecorate(BaseModel):
    decorations: List[DecorationInfo]

class EquipmentBase(BaseModel):
    """Base model for equipment."""
    name: str
    description: str
    base_price: float
    category: str
    specs: EquipmentSpecsAPI

class EquipmentCreate(BaseModel):
    """API model for creating equipment."""
    name: str
    description: str
    base_price: float
    category: str
    specs: EquipmentSpecsAPI

class EquipmentResponse(BaseModel):
    """API model for equipment response."""
    id: str
    name: str
    description: str
    base_price: float
    category: str
    specs: EquipmentSpecsAPI

    @classmethod
    def from_domain(cls, equipment):
        """Create from domain model."""
        return cls(
            id=equipment.id,
            name=equipment.name,
            description=equipment.description,
            base_price=equipment.base_price,
            category=equipment.category,
            specs=EquipmentSpecsAPI.from_domain(equipment.specs)
        )

class DecorationRequest(BaseModel):
    """API model for decoration request."""
    decoration_type: str
    warranty_months: Optional[int] = None
    installation_date: Optional[str] = None
    maintenance_plan: Optional[Dict[str, Any]] = None 
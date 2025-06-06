from dataclasses import dataclass, field
from typing import Dict, Optional, Tuple, Union, Any
import uuid

@dataclass
class EquipmentSpecs:
    """Характеристики спортивного обладнання"""
    weight: str  # вага в кг
    dimensions: str  # розміри (довжина, ширина, висота) в см
    material: str  # матеріал виготовлення
    color: str  # колір
    max_user_weight: str  # максимальна вага користувача в кг
    warranty_months: str  # гарантійний термін в місяцях
    
    def __post_init__(self):
        self.validate()
    
    def validate(self):
        """Валідація характеристик обладнання"""
        try:
            weight = float(self.weight)
            if weight <= 0:
                raise ValueError("Weight must be a positive number")
        except ValueError:
            raise ValueError("Weight must be a valid number string")
            
        try:
            # Parse dimensions like "200x80x140" or "200,80,140"
            dims = self.dimensions.replace('x', ',').split(',')
            if len(dims) != 3:
                raise ValueError("Dimensions must be in format 'LxWxH'")
            dimensions = [float(d.strip()) for d in dims]
            if not all(d > 0 for d in dimensions):
                raise ValueError("All dimensions must be positive numbers")
        except (ValueError, TypeError):
            raise ValueError("Dimensions must be a string in format 'LxWxH' with positive numbers")
                
        if not isinstance(self.material, str) or not self.material:
            raise ValueError("Material must be a non-empty string")
            
        if not isinstance(self.color, str) or not self.color:
            raise ValueError("Color must be a non-empty string")
            
        try:
            max_weight = float(self.max_user_weight)
            if max_weight <= 0:
                raise ValueError("Maximum user weight must be a positive number")
        except ValueError:
            raise ValueError("Maximum user weight must be a valid number string")
            
        try:
            warranty = int(self.warranty_months)
            if warranty <= 0:
                raise ValueError("Warranty months must be a positive integer")
        except ValueError:
            raise ValueError("Warranty months must be a valid integer string")

    def dict(self) -> Dict[str, Any]:
        """Конвертує характеристики в словник"""
        return {
            "weight": self.weight,
            "dimensions": self.dimensions,
            "material": self.material,
            "color": self.color,
            "max_user_weight": self.max_user_weight,
            "warranty_months": self.warranty_months
        }

@dataclass
class Equipment:
    """Клас для представлення спортивного обладнання"""
    name: str
    description: str
    base_price: float
    category: str = "General"
    specs: EquipmentSpecs = field(default_factory=lambda: EquipmentSpecs())
    id: Optional[str] = None
    _pricing_strategy = None

    def __post_init__(self):
        """Валідація після ініціалізації"""
        if self.id is None:
            self.id = str(uuid.uuid4())
        
        if not isinstance(self.name, str) or not self.name:
            raise ValueError("Name must be a non-empty string")
        
        if not isinstance(self.description, str) or not self.description:
            raise ValueError("Description must be a non-empty string")
        
        # Convert base_price to float if it's a string
        if isinstance(self.base_price, str):
            try:
                self.base_price = float(self.base_price)
            except ValueError:
                raise ValueError("Base price must be a valid number")
        
        if not isinstance(self.base_price, (int, float)) or self.base_price <= 0:
            raise ValueError("Base price must be a positive number")
        
        if not isinstance(self.category, str) or not self.category:
            raise ValueError("Category must be a non-empty string")
        
        if not isinstance(self.specs, EquipmentSpecs):
            raise ValueError("Specs must be an instance of EquipmentSpecs")

    def get_price(self) -> float:
        """Отримати ціну обладнання"""
        if self._pricing_strategy:
            return self._pricing_strategy.calculate_price(self)
        return self.base_price

    @property
    def final_price(self) -> float:
        """Отримати кінцеву ціну з урахуванням всіх модифікацій"""
        return self.get_price()

    def __str__(self) -> str:
        """Рядкове представлення обладнання"""
        return f"{self.name} ({self.category}) - ${self.base_price:.2f}"
        
    def to_dict(self) -> Dict:
        """Конвертує об'єкт в словник"""
        result = {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "base_price": self.base_price,
            "category": self.category,
            "specs": self.specs.dict()
        }
        return result
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Equipment':
        """Створює об'єкт з словника"""
        specs_data = data.get("specs")
        specs = EquipmentSpecs(
            weight=specs_data["weight"],
            dimensions=specs_data["dimensions"],
            material=specs_data["material"],
            color=specs_data["color"],
            max_user_weight=specs_data["max_user_weight"],
            warranty_months=specs_data["warranty_months"]
        )
        return cls(
            id=data.get("id"),
            name=data["name"],
            description=data["description"],
            base_price=float(data["base_price"]),
            category=data["category"],
            specs=specs
        )

    def dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "name": self.name,
            "description": self.description,
            "base_price": self.base_price,
            "category": self.category,
            "specs": self.specs.dict()
        }

    def get_description(self) -> str:
        """Get equipment description."""
        return self.description

    def set_pricing_strategy(self, strategy) -> None:
        """Set pricing strategy."""
        self._pricing_strategy = strategy 
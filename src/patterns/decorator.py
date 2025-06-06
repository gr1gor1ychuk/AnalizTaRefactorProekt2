from abc import ABC, abstractmethod
from typing import Dict
from src.models.equipment import Equipment, EquipmentSpecs
from datetime import datetime
from typing import Optional

class EquipmentDecorator(Equipment, ABC):
    """Base decorator for equipment."""
    
    def __init__(self, equipment: Equipment):
        """Initialize decorator."""
        super().__init__(
            name=equipment.name,
            description=equipment.description,
            base_price=equipment.base_price,
            category=equipment.category,
            specs=equipment.specs,
            id=equipment.id
        )
        self._equipment = equipment
        
    def get_price(self) -> float:
        """Get decorated price."""
        return self._equipment.get_price()

    @abstractmethod
    def get_description(self) -> str:
        """Get decorated description."""
        pass

    @property
    def final_price(self) -> float:
        """Отримати кінцеву ціну з урахуванням всіх декораторів"""
        return self.get_price()

    def dict(self) -> Dict:
        """Конвертувати в словник"""
        return {
            "name": self.name,
            "description": self.description,
            "base_price": self.base_price,
            "category": self.category,
            "specs": self.specs.dict()
        }

class WarrantyDecorator(EquipmentDecorator):
    """Decorator for adding warranty."""
    def __init__(self, equipment: Equipment, years: int):
        super().__init__(equipment)
        self.years = years
        # Update warranty months in specs
        warranty_months = int(self.specs.warranty_months) + (years * 12)
        self.specs = EquipmentSpecs(
            weight=self.specs.weight,
            dimensions=self.specs.dimensions,
            material=self.specs.material,
            color=self.specs.color,
            max_user_weight=self.specs.max_user_weight,
            warranty_months=str(warranty_months)
        )

    def get_price(self) -> float:
        """Calculate price with warranty."""
        # 10% increase per year
        return self._equipment.get_price() * (1 + 0.1 * self.years)

    def get_description(self) -> str:
        """Get description with warranty."""
        return f"{self._equipment.get_description()} with {self.years}-year warranty"

class InsuranceDecorator(EquipmentDecorator):
    """Decorator for adding insurance."""
    def __init__(self, equipment: Equipment, level: str):
        super().__init__(equipment)
        self.level = level.lower()
        self.coverage_type = level.lower()  # Add coverage_type attribute for tests

    def get_price(self) -> float:
        """Calculate price with insurance."""
        base_price = self._equipment.get_price()
        if self.level == "basic":
            return base_price * 1.05  # 5% increase
        elif self.level == "premium":
            return base_price * 1.15  # 15% increase
        else:
            return base_price * 1.10  # 10% increase for standard

    def get_description(self) -> str:
        """Get description with insurance."""
        return f"{self._equipment.get_description()} with {self.level} insurance"

class MaintenanceDecorator(EquipmentDecorator):
    """Maintenance decorator."""
    
    def __init__(self, equipment: Equipment, visits: int):
        """Initialize maintenance decorator."""
        super().__init__(equipment)
        self._visits = visits
        
    def get_price(self) -> float:
        """Get price with maintenance."""
        base_price = self._equipment.get_price()
        return base_price * (1 + 0.02 * self._visits)  # 2% increase per visit
        
    def get_description(self) -> str:
        """Get description with maintenance."""
        return f"{self._equipment.get_description()} with {self._visits} maintenance visits"

class InstallationDecorator(EquipmentDecorator):
    """Installation decorator."""
    def __init__(self, equipment: Equipment):
        """Initialize installation decorator."""
        super().__init__(equipment)

    def get_description(self) -> str:
        """Get description with installation."""
        return f"{self._equipment.get_description()} with installation on {datetime.now().strftime('%Y-%m-%d')}"

    def get_price(self) -> float:
        """Get price with installation."""
        base_price = self._equipment.get_price()
        return base_price * 1.10  # 10% increase for installation
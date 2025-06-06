from abc import ABC, abstractmethod
from typing import Optional, Tuple, Dict, Union
from src.models.equipment import Equipment, EquipmentSpecs

BLACK_RED_COLOR = "Black/Red"

class EquipmentBuilder(ABC):
    """Abstract base class for equipment builders."""
    def __init__(self):
        self._name = ""
        self._description = "Standard equipment"  # Default description
        self._base_price = 0.0
        self._category = "General"
        self._dimensions = "0x0x0"
        self._weight = "75.0"  # Default weight
        self._material = "Steel"  # Default material
        self._color = "Black"  # Default color
        self._max_user_weight = "150.0"  # Default max user weight
        self._warranty_months = "12"  # Default warranty months
        # Додаткові характеристики для різних типів обладнання
        self._max_speed = 0.0
        self._incline_levels = 0
        self._motor_power = 0.0
        self._weight_capacity = 0.0
        self._has_safety_bars = False
        self._has_pull_up_bar = False
    
    def set_name(self, name: str) -> 'EquipmentBuilder':
        """Set equipment name."""
        self._name = name
        return self
    
    def set_description(self, description: str) -> 'EquipmentBuilder':
        """Set equipment description."""
        self._description = description
        return self
    
    def set_base_price(self, price: float) -> 'EquipmentBuilder':
        """Set equipment base price."""
        self._base_price = price
        return self
    
    def set_category(self, category: str) -> 'EquipmentBuilder':
        """Set equipment category."""
        self._category = category
        return self
    
    def set_dimensions(self, dimensions: str) -> 'EquipmentBuilder':
        """Set equipment dimensions."""
        self._dimensions = dimensions
        return self
    
    def set_weight(self, weight: float) -> 'EquipmentBuilder':
        """Set equipment weight."""
        self._weight = str(weight)
        return self
    
    def set_material(self, material: str) -> 'EquipmentBuilder':
        """Set equipment material."""
        self._material = material
        return self
    
    def set_color(self, color: str) -> 'EquipmentBuilder':
        """Set equipment color."""
        self._color = color
        return self
    
    def set_max_user_weight(self, weight: float) -> 'EquipmentBuilder':
        """Set equipment max user weight."""
        self._max_user_weight = str(weight)
        return self
    
    def set_warranty_months(self, months: int) -> 'EquipmentBuilder':
        """Set equipment warranty months."""
        self._warranty_months = str(months)
        return self
    
    def build(self) -> Equipment:
        """Build the equipment."""
        specs = EquipmentSpecs(
            weight=self._weight,
            dimensions=self._dimensions,
            material=self._material,
            color=self._color,
            max_user_weight=self._max_user_weight,
            warranty_months=self._warranty_months
        )
        return Equipment(
            name=self._name,
            description=self._description,
            base_price=self._base_price,
            category=self._category,
            specs=specs
        )

class TreadmillBuilder(EquipmentBuilder):
    """Builder for treadmill equipment."""
    def __init__(self):
        super().__init__()
        self._max_speed = 0.0
        self._incline_levels = 0
        self._motor_power = 0.0
        self._category = "Cardio"
        self._dimensions = "200x80x140"  # Default treadmill dimensions
        self._description = "Professional treadmill with advanced features"  # Default description
    
    def set_max_speed(self, speed: float) -> 'TreadmillBuilder':
        """Set treadmill max speed."""
        self._max_speed = speed
        return self
    
    def set_incline_levels(self, levels: int) -> 'TreadmillBuilder':
        """Set treadmill incline levels."""
        self._incline_levels = levels
        return self
    
    def set_motor_power(self, power: float) -> 'TreadmillBuilder':
        """Set treadmill motor power."""
        self._motor_power = power
        return self

class PowerRackBuilder(EquipmentBuilder):
    """Будівельник для силових рам"""
    
    def __init__(self):
        super().__init__()
        self._color = BLACK_RED_COLOR  # Default color
        self._warranty_months = 36  # Default warranty
        self._category = "Strength"  # Default category
    
    def set_name(self, name: str = "Professional Power Rack") -> None:
        self._name = name
    
    def set_description(self, description: str = "Heavy-duty power rack for professional use") -> None:
        self._description = description
    
    def set_base_price(self, price: float = 1499.99) -> None:
        self._base_price = float(price)
    
    def set_category(self, category: str = "Strength") -> None:
        self._category = category
    
    def set_weight(self, weight: float = 200.0) -> None:
        self._weight = float(weight)
    
    def set_dimensions(self, dimensions: str = "140x140x230") -> None:
        self._dimensions = dimensions
    
    def set_material(self, material: str = "Heavy Gauge Steel") -> None:
        self._material = material
    
    def set_color(self, color: str = BLACK_RED_COLOR) -> None:
        self._color = color
    
    def set_max_user_weight(self, weight: float = 450.0) -> None:
        self._max_user_weight = float(weight)
    
    def set_warranty_months(self, months: int = 36) -> None:
        self._warranty_months = int(months)
        
    def set_weight_capacity(self, capacity: float = 1000.0) -> None:
        """Встановлює максимальну вагу навантаження"""
        self._weight_capacity = float(capacity)
        
    def set_has_safety_bars(self, has_bars: bool = True) -> None:
        """Встановлює наявність страхувальних штанг"""
        self._has_safety_bars = bool(has_bars)
        
    def set_has_pull_up_bar(self, has_bar: bool = True) -> None:
        """Встановлює наявність турніка"""
        self._has_pull_up_bar = bool(has_bar)
    
    def build(self) -> Equipment:
        """Створити обладнання"""
        specs = EquipmentSpecs(
            weight=self._weight,
            dimensions=self._dimensions,
            material=self._material,
            color=self._color,
            max_user_weight=self._max_user_weight,
            warranty_months=self._warranty_months
        )
        return Equipment(
            name=self._name,
            description=self._description,
            base_price=self._base_price,
            category=self._category,
            specs=specs
        )

class EquipmentDirector:
    """Директор, що керує процесом будівництва"""
    
    AVAILABLE_COLORS = {
        "Black": "Класичний чорний",
        "White": "Білий",
        "Silver": "Сріблястий",
        "Red": "Червоний",
        "Blue": "Синій",
        BLACK_RED_COLOR: "Чорний з червоним",
        "Gray": "Сірий"
    }
    
    def __init__(self, builder: EquipmentBuilder):
        self._builder = builder
    
    def change_builder(self, builder: EquipmentBuilder):
        self._builder = builder
    
    def construct_basic_model(self, color: str = None):
        """Створює базову модель обладнання"""
        if isinstance(self._builder, TreadmillBuilder):
            self._builder.set_name("Professional Treadmill")
            self._builder.set_description("Professional grade treadmill with advanced features")
            self._builder.set_base_price(1999.99)
            self._builder.set_category()
            self._builder.set_weight(125.0)
            self._builder.set_dimensions("200x85x140")
            self._builder.set_material()
            self._builder.set_color(color if color in self.AVAILABLE_COLORS else "Black")
            self._builder.set_max_user_weight(180.0)
            self._builder.set_warranty_months()
            self._builder.set_max_speed(20.0)
            self._builder.set_incline_levels(15)
            self._builder.set_motor_power(3.5)
        elif isinstance(self._builder, PowerRackBuilder):
            self._builder.set_name("Professional Power Rack")
            self._builder.set_description("Heavy-duty power rack for professional use")
            self._builder.set_base_price(1499.99)
            self._builder.set_category()
            self._builder.set_weight(200.0)
            self._builder.set_dimensions("140x140x230")
            self._builder.set_material()
            self._builder.set_color(color if color in self.AVAILABLE_COLORS else BLACK_RED_COLOR)
            self._builder.set_max_user_weight(450.0)
            self._builder.set_warranty_months()
            self._builder.set_weight_capacity(1000.0)
            self._builder.set_has_safety_bars(True)
            self._builder.set_has_pull_up_bar(True)
    
    @classmethod
    def get_available_colors(cls) -> Dict[str, str]:
        """Повертає словник доступних кольорів та їх описів"""
        return cls.AVAILABLE_COLORS.copy()
    
    @classmethod
    def is_valid_color(cls, color: str) -> bool:
        """Перевіряє чи є колір допустимим"""
        return color in cls.AVAILABLE_COLORS 
"""Singleton pattern implementation."""
from typing import Dict, Optional, List
from src.models.equipment import Equipment
from src.models.order import Order

class EquipmentInventory:
    """Singleton inventory for equipment."""
    _instance = None

    def __new__(cls):
        """Create singleton instance."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            # Initialize instance variables
            cls._instance._equipment_stock = {}
            cls._instance._equipment_items = {}
            cls._instance._orders = {}
        return cls._instance

    def add_equipment(self, equipment: Equipment, quantity: int = 1) -> None:
        """Add equipment to inventory with specified quantity."""
        if quantity <= 0:
            raise ValueError("Quantity must be positive")
        
        # Handle case where equipment might be passed as string ID
        if isinstance(equipment, str):
            equipment_id = equipment
            equipment_obj = self._equipment_items.get(equipment_id)
            if not equipment_obj:
                raise ValueError(f"Equipment with ID {equipment_id} not found")
            equipment = equipment_obj
        
        # Ensure equipment has an ID
        if not hasattr(equipment, 'id') or not equipment.id:
            import uuid
            equipment.id = str(uuid.uuid4())
            
        if equipment.id not in self._equipment_stock:
            self._equipment_stock[equipment.id] = 0
            self._equipment_items[equipment.id] = equipment
            
        self._equipment_stock[equipment.id] += quantity

    def remove_equipment(self, equipment: Equipment, quantity: int = 1) -> bool:
        """Remove equipment from inventory."""
        if quantity <= 0:
            raise ValueError("Quantity must be positive")
            
        if equipment.id not in self._equipment_stock:
            return False
            
        if self._equipment_stock[equipment.id] < quantity:
            return False
            
        self._equipment_stock[equipment.id] -= quantity
        return True

    def get_equipment(self, equipment_id: str) -> Optional[Equipment]:
        """Get equipment by ID."""
        return self._equipment_items.get(equipment_id)

    def get_equipment_stock(self, equipment_id: str) -> int:
        """Get equipment stock by ID."""
        return self._equipment_stock.get(equipment_id, 0)

    def get_equipment_quantity(self, equipment_id: str) -> int:
        """Get equipment quantity by ID."""
        return self._equipment_stock.get(equipment_id, 0)

    def is_in_stock(self, equipment: Equipment, quantity: int = 1) -> bool:
        """Check if equipment is in stock."""
        return self.get_equipment_stock(equipment.id) >= quantity

    def get_all_equipment(self) -> List[Equipment]:
        """Get all equipment in inventory."""
        return list(self._equipment_items.values())

    def get_quantity(self, equipment: Equipment) -> int:
        """Get quantity of equipment in stock."""
        if equipment.id in self._equipment_stock:
            return self._equipment_stock[equipment.id]
        return 0

    def get_order(self, order_id: str) -> Optional[Order]:
        """Get order by ID."""
        return self._orders.get(order_id)

    def add_order(self, order: Order) -> None:
        """Add order to storage."""
        self._orders[order.id] = order

    def update_order_status(self, order_id: str, status: str) -> None:
        """Update order status."""
        if order_id in self._orders:
            self._orders[order_id].status = status

    def clear(self) -> None:
        """Clear all inventory data."""
        self._equipment_stock.clear()
        self._equipment_items.clear()
        self._orders.clear()

    def get_all_orders(self) -> List[Order]:
        """Get all orders."""
        return list(self._orders.values())

    # NEW METHODS NEEDED FOR API TESTS
    
    def update_equipment(self, equipment_id: str, updated_equipment: Equipment) -> Optional[Equipment]:
        """Update equipment in inventory."""
        if equipment_id in self._equipment_items:
            # Preserve the original ID and stock quantity
            updated_equipment.id = equipment_id
            self._equipment_items[equipment_id] = updated_equipment
            return updated_equipment
        return None

    def decorate_equipment(self, equipment_id: str, decoration_type: str, **kwargs) -> Optional[Equipment]:
        """Apply decoration to equipment."""
        equipment = self.get_equipment(equipment_id)
        if not equipment:
            return None
        
        try:
            # Import decorators
            from src.patterns.decorator import (
                InsuranceDecorator, 
                WarrantyDecorator, 
                InstallationDecorator, 
                MaintenanceDecorator
            )
            
            # Apply decoration based on type
            if decoration_type == "premium":
                decorated = InsuranceDecorator(equipment, "premium")
            elif decoration_type == "warranty":
                warranty_months = kwargs.get('warranty_months', 12)
                years = max(1, warranty_months // 12)  # Minimum 1 year
                decorated = WarrantyDecorator(equipment, years)
            elif decoration_type == "installation":
                decorated = InstallationDecorator(equipment)
            elif decoration_type == "maintenance":
                visits = kwargs.get('visits', 6)
                decorated = MaintenanceDecorator(equipment, visits)
            elif decoration_type == "insurance":
                level = kwargs.get('level', 'standard')
                decorated = InsuranceDecorator(equipment, level)
            else:
                raise ValueError(f"Invalid decoration type: {decoration_type}")
            
            # Ensure the decorated equipment has the correct price
            # Update base_price to reflect the decorated price
            if hasattr(decorated, 'get_price'):
                decorated.base_price = decorated.get_price()
            
            # Update the equipment in inventory
            return self.update_equipment(equipment_id, decorated)
            
        except ImportError:
            # If decorators are not available, return None
            return None
        except Exception:
            # Handle any other errors
            return None

    def create_equipment(self, equipment: Equipment) -> Equipment:
        """Create new equipment and add to inventory."""
        # Generate ID if not present
        if not hasattr(equipment, 'id') or not equipment.id:
            import uuid
            equipment.id = str(uuid.uuid4())
        
        # Add to inventory with quantity 1
        self.add_equipment(equipment, 1)
        return equipment
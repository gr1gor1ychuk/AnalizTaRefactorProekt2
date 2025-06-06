"""Order model implementation."""
from dataclasses import dataclass, field
from typing import Optional
from uuid import uuid4
from src.models.equipment import Equipment

@dataclass
class Order:
    """Order model."""
    equipment: Optional[Equipment]
    quantity: int
    customer_id: str
    customer_name: Optional[str] = None
    customer_email: Optional[str] = None
    shipping_address: Optional[str] = None
    status: str = "pending"
    id: Optional[str] = None
    items: list = field(default_factory=list)
    notes: list = field(default_factory=list)

    def __post_init__(self):
        """Initialize order."""
        if self.id is None:
            self.id = str(uuid4())
            
        # Validate customer ID
        if not self.customer_id:
            raise ValueError("Customer ID is required")
            
        # Validate quantity for non-empty orders
        if self.equipment is not None and self.quantity <= 0:
            raise ValueError("Quantity must be positive")
            
        # Validate equipment for non-empty orders
        if self.quantity > 0 and not self.equipment:
            raise ValueError("Equipment is required for non-empty orders")

    def get_total_price(self) -> float:
        """Get total price of the order."""
        if not self.equipment:
            return 0.0
        return self.equipment.get_price() * self.quantity

    def update_status(self, status: str) -> None:
        """Update order status."""
        self.status = status

    def to_dict(self) -> dict:
        """Convert order to dictionary."""
        return {
            "id": self.id,
            "equipment": self.equipment.to_dict() if self.equipment else None,
            "quantity": self.quantity,
            "customer_id": self.customer_id,
            "customer_name": self.customer_name,
            "customer_email": self.customer_email,
            "shipping_address": self.shipping_address,
            "status": self.status,
            "total_price": self.get_total_price()
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Order':
        """Create order from dictionary."""
        equipment = Equipment.from_dict(data["equipment"]) if data.get("equipment") else None
        return cls(
            id=data.get("id"),
            equipment=equipment,
            quantity=data["quantity"],
            customer_id=data["customer_id"],
            customer_name=data.get("customer_name"),
            customer_email=data.get("customer_email"),
            shipping_address=data.get("shipping_address"),
            status=data.get("status", "pending")
        )

    def __str__(self) -> str:
        """Get string representation of order."""
        return f"Order {self.id}: {self.quantity}x {self.equipment.name if self.equipment else 'No equipment'} - {self.status}"

    def add_item(self, item_id: str) -> None:
        """Add an item to the order."""
        if hasattr(self, 'items'):
            self.items.append(item_id)
        else:
            self.items = [item_id]

    def remove_item(self, item_id: str) -> None:
        """Remove an item from the order."""
        if hasattr(self, 'items'):
            self.items.remove(item_id)

    def calculate_total(self, prices: dict) -> float:
        """Calculate the total price of the order."""
        if hasattr(self, 'equipment'):
            return self.equipment.base_price * self.quantity
        return sum(prices.get(item_id, 0) for item_id in self.items)

    def add_note(self, note: str) -> None:
        """Add a note to the order."""
        if not note:
            raise ValueError("Note cannot be empty")
        self.notes.append(note)

    def process(self) -> bool:
        """Process the order by checking equipment availability."""
        from src.patterns.singleton import InventorySingleton  # Import here to avoid circular dependency
        inventory = InventorySingleton()

        # Check availability for all items
        for item in self.items:
            if not inventory.is_available(item, 1):  # Assuming quantity of 1 for each item
                return False

        # Remove items from inventory
        try:
            for item in self.items:
                inventory.remove_equipment(item, 1)  # Assuming quantity of 1 for each item
            return True
        except ValueError:
            return False

    def add_note(self, note: str):
        self.notes += f"{note}\n" 
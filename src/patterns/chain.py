from abc import ABC, abstractmethod
from typing import Optional
from src.models.order import Order
from src.patterns.singleton import EquipmentInventory
from src.patterns.observer import NotificationSystem

class OrderProcessor(ABC):
    """Abstract base class for order processors."""
    def __init__(self):
        """Initialize order processor."""
        self._next_processor = None
        self._notification_system = NotificationSystem()

    def set_next(self, processor: 'OrderProcessor') -> 'OrderProcessor':
        """Set next processor in chain."""
        self._next_processor = processor
        return processor

    def process(self, order: Order) -> bool:
        """Process order through chain."""
        if self._validate(order):
            if self._next_processor:
                return self._next_processor.process(order)
            return True
        return False

    @abstractmethod
    def _validate(self, order: Order) -> bool:
        """Validate order."""
        pass

class StockValidator(OrderProcessor):
    """Validates if equipment is in stock."""
    def _validate(self, order: Order) -> bool:
        """Check if equipment is in stock."""
        if not order or not order.equipment:
            return True  # Empty orders are valid
            
        inventory = EquipmentInventory()
        if inventory.is_in_stock(order.equipment, order.quantity):
            order.status = "stock_validated"
            self._notification_system.notify(order, "stock_validated")
            return True
        return False

class PaymentProcessor(OrderProcessor):
    """Processes payment for order."""
    def _validate(self, order: Order) -> bool:
        """Validate payment."""
        if not order:
            return False
            
        if not order.customer_id:
            return False
            
        # For demo purposes, consider payment always successful
        order.status = "paid"
        self._notification_system.notify(order, "paid")
        return True

class OrderFulfillment(OrderProcessor):
    """Fulfills the order."""
    def _validate(self, order: Order) -> bool:
        """Fulfill order."""
        if not order or order.status != "paid":
            return False
            
        if not order.equipment:
            return True  # Empty orders are fulfilled automatically
            
        inventory = EquipmentInventory()
        if inventory.remove_equipment(order.equipment, order.quantity):
            order.status = "fulfilled"
            self._notification_system.notify(order, "fulfilled")
            return True
        return False

class OrderProcessorChain:
    """Chain of responsibility for order processing."""
    def __init__(self):
        """Initialize order processor chain."""
        self.stock_validator = StockValidator()
        self.payment_processor = PaymentProcessor()
        self.order_fulfillment = OrderFulfillment()

        # Set up chain
        self.stock_validator.set_next(self.payment_processor)
        self.payment_processor.set_next(self.order_fulfillment)

    def process_order(self, order: Order) -> bool:
        """Process order through chain."""
        return self.stock_validator.process(order) 
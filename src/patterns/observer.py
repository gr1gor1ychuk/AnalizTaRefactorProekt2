"""Observer pattern implementation."""
from abc import ABC, abstractmethod
from typing import List
import logging
from datetime import datetime
from src.models.order import Order

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OrderEvent:
    """Order event class."""
    def __init__(self, order: Order, event_type: str):
        self.order = order
        self.event_type = event_type
        self.timestamp = datetime.now()

class OrderObserver(ABC):
    """Abstract base class for order observers."""
    @abstractmethod
    def update(self, order: Order, event_type: str) -> None:
        """Update observer with order event."""
        pass

class NotificationSystem:
    """Notification system for order events."""
    def __init__(self):
        """Initialize notification system."""
        self._observers: List[OrderObserver] = []
        logger.info("Notification system initialized")

    def attach(self, observer: OrderObserver) -> None:
        """Attach observer to notification system."""
        if observer not in self._observers:
            self._observers.append(observer)
            logger.info(f"Attached {observer.__class__.__name__} to notification system")

    def detach(self, observer: OrderObserver) -> None:
        """Detach observer from notification system."""
        if observer in self._observers:
            self._observers.remove(observer)
            logger.info(f"Detached {observer.__class__.__name__} from notification system")

    def notify(self, order: Order, event_type: str) -> None:
        """Notify all observers about an order event - метод, що викликається в тестах."""
        logger.info(f"Notifying observers about order {order.id} event: {event_type}")
        for observer in self._observers:
            observer.update(order, event_type)

    def notify_observers(self, order: Order, event_type: str) -> None:
        """Notify all observers about an order event - альтернативний метод."""
        self.notify(order, event_type)

class EmailNotifier(OrderObserver):
    """Email notification observer."""
    def update(self, order: Order, event_type: str) -> None:
        """Send email notification."""
        if hasattr(order, 'customer_email') and order.customer_email:
            logger.info(f"Sending email to {order.customer_email} about order {order.id} {event_type}")
        else:
            logger.warning(f"No email address available for order {order.id}")

class SMSNotifier(OrderObserver):
    """SMS notification observer."""
    def update(self, order: Order, event_type: str) -> None:
        """Send SMS notification."""
        if hasattr(order, 'customer_name') and order.customer_name:
            logger.info(f"Sending SMS to {order.customer_name} about order {order.id} {event_type}")
        else:
            logger.warning(f"No customer name available for order {order.id}")
"""Tests for observer pattern."""
import pytest
from uuid import uuid4
from src.patterns.observer import (
    OrderObserver,
    NotificationSystem,
    EmailNotifier,
    SMSNotifier
)
from src.models.order import Order
from src.models.equipment import Equipment, EquipmentSpecs

@pytest.fixture
def sample_equipment():
    """Create sample equipment for testing."""
    return Equipment(
        name="Test Equipment",
        description="Test Description",
        base_price=299.99,
        category="Test",
        specs=EquipmentSpecs(
            weight="75.0",
            dimensions="200x100x220",
            material="Steel",
            color="Black",
            max_user_weight="150.0",
            warranty_months="12"
        )
    )

@pytest.fixture
def sample_order(sample_equipment):
    """Create sample order for testing."""
    return Order(
        equipment=sample_equipment,
        quantity=1,
        customer_id="CUST001",
        customer_name="John Doe",
        customer_email="john@example.com",
        shipping_address="123 Main St"
    )

def test_notification_system_creation():
    """Test creating notification system."""
    system = NotificationSystem()
    assert isinstance(system, NotificationSystem)
    assert len(system._observers) == 0

def test_notification_system_attach_observer():
    """Test attaching observer to notification system."""
    system = NotificationSystem()
    observer = EmailNotifier()
    system.attach(observer)
    assert len(system._observers) == 1
    assert observer in system._observers

def test_notification_system_detach_observer():
    """Test detaching observer from notification system."""
    system = NotificationSystem()
    observer = EmailNotifier()
    system.attach(observer)
    system.detach(observer)
    assert len(system._observers) == 0
    assert observer not in system._observers

def test_notification_system_notify_observers(sample_order):
    """Test notifying observers."""
    system = NotificationSystem()
    observer = EmailNotifier()
    system.attach(observer)
    system.notify(sample_order, "created")

def test_email_notifier(sample_order):
    """Test email notifier."""
    notifier = EmailNotifier()
    notifier.update(sample_order, "created")

def test_sms_notifier(sample_order):
    """Test SMS notifier."""
    notifier = SMSNotifier()
    notifier.update(sample_order, "created")

def test_multiple_observers(sample_order):
    """Test multiple observers."""
    system = NotificationSystem()
    email_notifier = EmailNotifier()
    sms_notifier = SMSNotifier()
    
    system.attach(email_notifier)
    system.attach(sms_notifier)
    
    system.notify(sample_order, "created")

def test_order_event_creation(sample_order):
    """Test order event creation."""
    system = NotificationSystem()
    observer = EmailNotifier()
    system.attach(observer)
    system.notify(sample_order, "created")

def test_observer_chain_of_events(sample_order):
    """Test chain of order events."""
    system = NotificationSystem()
    observer = EmailNotifier()
    system.attach(observer)
    
    events = ["created", "paid", "shipped", "delivered"]
    for event in events:
        system.notify(sample_order, event)

def test_observer_pattern(sample_order):
    """Test complete observer pattern."""
    system = NotificationSystem()
    email_notifier = EmailNotifier()
    sms_notifier = SMSNotifier()
    
    system.attach(email_notifier)
    system.attach(sms_notifier)
    
    events = ["created", "paid", "shipped", "delivered"]
    for event in events:
        system.notify(sample_order, event)

def test_observer_detachment(sample_order):
    """Test observer detachment during notifications."""
    system = NotificationSystem()
    email_notifier = EmailNotifier()
    sms_notifier = SMSNotifier()
    
    system.attach(email_notifier)
    system.attach(sms_notifier)
    
    system.notify(sample_order, "created")
    system.detach(sms_notifier)
    system.notify(sample_order, "paid")
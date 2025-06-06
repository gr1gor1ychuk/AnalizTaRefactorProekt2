"""Tests for chain pattern."""
import pytest
from src.models.order import Order
from src.models.equipment import Equipment, EquipmentSpecs
from src.patterns.chain import (
    OrderProcessor,
    StockValidator,
    PaymentProcessor,
    OrderFulfillment,
    OrderProcessorChain
)
from src.patterns.singleton import EquipmentInventory

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

def test_order_creation(sample_equipment):
    """Test order creation."""
    order = Order(
        equipment=sample_equipment,
        quantity=2,
        customer_id="CUST001",
        customer_name="John Doe",
        customer_email="john@example.com",
        shipping_address="123 Main St"
    )
    assert order.equipment == sample_equipment
    assert order.quantity == 2
    assert order.customer_id == "CUST001"
    assert order.status == "pending"

def test_stock_validator(sample_order, sample_equipment):
    """Test stock validation."""
    inventory = EquipmentInventory()
    validator = StockValidator()

    # Add equipment to inventory
    inventory.add_equipment(sample_equipment, 2)

    # Test with sufficient stock
    assert validator.process(sample_order) is True

    # Test with insufficient stock
    order = Order(
        equipment=sample_equipment,
        quantity=3,
        customer_id="CUST001",
        customer_name="John Doe",
        customer_email="john@example.com",
        shipping_address="123 Main St"
    )
    assert validator.process(order) is False

def test_payment_processor(sample_order):
    """Test payment processing."""
    processor = PaymentProcessor()
    assert processor.process(sample_order) is True
    assert sample_order.status == "paid"

def test_order_fulfillment(sample_order, sample_equipment):
    """Test order fulfillment."""
    inventory = EquipmentInventory()
    fulfillment = OrderFulfillment()

    # Add equipment to inventory
    inventory.add_equipment(sample_equipment, 2)

    # Test successful fulfillment
    sample_order.status = "paid"
    assert fulfillment.process(sample_order) is True

    # Test failed fulfillment
    sample_order.status = "pending"
    assert fulfillment.process(sample_order) is False

def test_order_processor_chain(sample_order, sample_equipment):
    """Test complete order processing chain."""
    inventory = EquipmentInventory()

    # Set up the chain
    chain = OrderProcessorChain()

    # Add equipment to inventory
    inventory.add_equipment(sample_equipment, 2)

    # Test successful processing
    assert chain.process_order(sample_order) is True

def test_order_processor_empty_order():
    """Test processing empty order."""
    chain = OrderProcessorChain()
    order = Order(
        equipment=None,
        quantity=0,
        customer_id="CUST001",
        customer_name="Test Customer",
        customer_email="test@example.com"
    )
    assert chain.process_order(order) is True

def test_order_processor_invalid_customer():
    """Test processing order with invalid customer."""
    chain = OrderProcessorChain()
    with pytest.raises(ValueError, match="Customer ID is required"):
        Order(
            equipment=None,
            quantity=0,
            customer_id="",
            customer_name="Test Customer",
            customer_email="test@example.com"
        ) 
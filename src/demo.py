"""Demo module for showcasing design patterns."""
from typing import List
from uuid import uuid4
from src.patterns.builder import TreadmillBuilder, PowerRackBuilder
from src.patterns.decorator import (
    WarrantyDecorator,
    InstallationDecorator,
    MaintenanceDecorator,
    InsuranceDecorator
)
from src.patterns.singleton import EquipmentInventory
from src.patterns.strategy import (
    RegularPricingStrategy,
    BulkPricingStrategy,
    SeasonalPricingStrategy,
    PremiumPricingStrategy
)
from src.patterns.observer import NotificationSystem, EmailNotifier, SMSNotifier
from src.models.order import Order
from src.models.equipment import Equipment

PRO_TREADMILL_NAME = "Pro Treadmill"
PROFESSIONAL_TREADMILL_NAME = "Professional Treadmill"
STEEL_ALUMINUM_MATERIAL = "Steel and Aluminum"

def create_demo_equipment() -> List[str]:
    """Create demo equipment using builder pattern."""
    results = []
    
    # Create treadmill
    treadmill_builder = TreadmillBuilder()
    treadmill_builder.set_name(PRO_TREADMILL_NAME)
    treadmill_builder.set_description(PROFESSIONAL_TREADMILL_NAME)
    treadmill_builder.set_base_price(1999.99)
    treadmill_builder.set_dimensions("200x80x140")
    treadmill_builder.set_weight(120.0)
    treadmill_builder.set_max_user_weight(180.0)
    treadmill_builder.set_material(STEEL_ALUMINUM_MATERIAL)
    treadmill_builder.set_max_speed(20.0)
    treadmill_builder.set_incline_levels(15)
    treadmill_builder.set_motor_power(3.5)
    treadmill = treadmill_builder.build()
    results.append(f"Created treadmill: {treadmill.name}")
    
    # Create power rack
    power_rack_builder = PowerRackBuilder()
    power_rack_builder.set_name("Pro Power Rack")
    power_rack_builder.set_description("Professional Power Rack")
    power_rack_builder.set_base_price(1499.99)
    power_rack_builder.set_dimensions("180x180x240")
    power_rack_builder.set_weight(200.0)
    power_rack_builder.set_max_user_weight(350.0)
    power_rack_builder.set_material("Heavy Duty Steel")
    power_rack_builder.set_weight_capacity(500.0)
    power_rack_builder.set_has_safety_bars(True)
    power_rack_builder.set_has_pull_up_bar(True)
    power_rack = power_rack_builder.build()
    results.append(f"Created power rack: {power_rack.name}")
    
    return results

def create_demo_order() -> Order:
    """Create demo order."""
    treadmill_builder = TreadmillBuilder()
    treadmill_builder.set_name(PRO_TREADMILL_NAME)
    treadmill_builder.set_description(PROFESSIONAL_TREADMILL_NAME)
    treadmill_builder.set_base_price(1999.99)
    treadmill_builder.set_dimensions("200x80x140")
    treadmill_builder.set_weight(120.0)
    treadmill_builder.set_max_user_weight(180.0)
    treadmill_builder.set_material(STEEL_ALUMINUM_MATERIAL)
    treadmill_builder.set_max_speed(20.0)
    treadmill_builder.set_incline_levels(15)
    treadmill_builder.set_motor_power(3.5)
    treadmill = treadmill_builder.build()
    
    return Order(
        equipment=treadmill,
        quantity=1,
        customer_id="CUST001",
        customer_name="John Doe",
        customer_email="john@example.com",
        shipping_address="123 Main St"
    )

def demonstrate_decorator_pattern() -> str:
    """Demonstrate decorator pattern."""
    # Create base equipment
    treadmill_builder = TreadmillBuilder()
    treadmill_builder.set_name(PRO_TREADMILL_NAME)
    treadmill_builder.set_description(PROFESSIONAL_TREADMILL_NAME)
    treadmill_builder.set_base_price(1999.99)
    treadmill = treadmill_builder.build()
    
    output = ["Decorator Pattern:"]
    output.append(f"Base Price: ${treadmill.get_price():.2f}")
    
    # Add warranty
    with_warranty = WarrantyDecorator(treadmill, 2)  # 2 years warranty
    output.append(f"With Warranty: ${with_warranty.get_price():.2f}")
    
    # Add insurance
    with_insurance = InsuranceDecorator(treadmill, "premium")
    output.append(f"With Insurance: ${with_insurance.get_price():.2f}")
    
    # Add maintenance
    with_maintenance = MaintenanceDecorator(treadmill, 12)  # 12 visits
    output.append(f"With Maintenance: ${with_maintenance.get_price():.2f}")
    
    # Add installation
    with_installation = InstallationDecorator(treadmill)
    output.append(f"With Installation: ${with_installation.get_price():.2f}")
    
    return "\n".join(output)

def demonstrate_singleton_pattern() -> str:
    """Demonstrate singleton pattern."""
    # Create first instance
    inventory1 = EquipmentInventory()
    
    # Create equipment
    treadmill_builder = TreadmillBuilder()
    treadmill_builder.set_name(PRO_TREADMILL_NAME)
    treadmill_builder.set_description(PROFESSIONAL_TREADMILL_NAME)
    treadmill_builder.set_base_price(1999.99)
    treadmill = treadmill_builder.build()
    
    # Add equipment to first instance
    inventory1.add_equipment(treadmill, 2)
    
    # Create second instance
    inventory2 = EquipmentInventory()
    
    # Check if equipment exists in second instance
    in_stock = inventory2.get_equipment_quantity(treadmill.id) > 0
    
    output = [
        "Singleton Pattern:",
        f"Both instances share state, in stock: {in_stock}",
        "Equipment added to inventory"
    ]
    return "\n".join(output)

def demonstrate_strategy_pattern() -> str:
    """Demonstrate strategy pattern."""
    treadmill_builder = TreadmillBuilder()
    treadmill_builder.set_name(PRO_TREADMILL_NAME)
    treadmill_builder.set_description(PROFESSIONAL_TREADMILL_NAME)
    treadmill_builder.set_base_price(1000.0)  # Use round number for easy calculation
    treadmill_builder.set_dimensions("200x80x140")
    treadmill_builder.set_weight(120.0)
    treadmill_builder.set_max_user_weight(180.0)
    treadmill_builder.set_material(STEEL_ALUMINUM_MATERIAL)
    treadmill_builder.set_max_speed(20.0)
    treadmill_builder.set_incline_levels(15)
    treadmill_builder.set_motor_power(3.5)
    treadmill = treadmill_builder.build()
    
    output = ["Strategy Pattern:"]
    
    # Regular pricing
    regular_strategy = RegularPricingStrategy()
    output.append(f"Regular={regular_strategy.calculate_price(treadmill):.2f}")
    
    # Bulk pricing
    bulk_strategy = BulkPricingStrategy(threshold=5, discount_percent=10.0)
    output.append(f"Bulk(5)={bulk_strategy.calculate_price(treadmill, quantity=5):.2f}")
    
    # Seasonal pricing
    seasonal_strategy = SeasonalPricingStrategy(discount_percent=20.0)
    output.append(f"Seasonal={seasonal_strategy.calculate_price(treadmill):.2f}")
    
    # Premium pricing
    premium_strategy = PremiumPricingStrategy()
    output.append(f"Premium={premium_strategy.calculate_price(treadmill):.2f}")
    
    return "\n".join(output)

def demonstrate_observer_pattern() -> str:
    """Demonstrate observer pattern."""
    # Create notification system
    notification_system = NotificationSystem()

    # Add observers
    email_notifier = EmailNotifier()
    sms_notifier = SMSNotifier()
    notification_system.attach(email_notifier)
    notification_system.attach(sms_notifier)

    # Create equipment and order
    treadmill_builder = TreadmillBuilder()
    treadmill_builder.set_name(PRO_TREADMILL_NAME)
    treadmill_builder.set_description(PROFESSIONAL_TREADMILL_NAME)
    treadmill_builder.set_base_price(1999.99)
    treadmill = treadmill_builder.build()

    order = Order(
        equipment=treadmill,
        quantity=1,
        customer_id="CUST001",
        customer_name="John Doe",
        customer_email="john@example.com",
        shipping_address="123 Main St"
    )

    # Notify about order
    notification_system.notify_observers(order, "created")

    output = [
        "Observer Pattern:",
        "Successfully sent notifications to all observers"
    ]
    return "\n".join(output)

def demonstrate_all_patterns() -> str:
    """Demonstrate all design patterns."""
    output = []
    
    # Builder Pattern
    treadmill_builder = TreadmillBuilder()
    treadmill_builder.set_name(PRO_TREADMILL_NAME)
    treadmill_builder.set_description(PROFESSIONAL_TREADMILL_NAME)
    treadmill_builder.set_base_price(1999.99)
    treadmill_builder.set_dimensions("200x80x140")
    treadmill_builder.set_weight(120.0)
    treadmill_builder.set_max_user_weight(180.0)
    treadmill_builder.set_material(STEEL_ALUMINUM_MATERIAL)
    treadmill_builder.set_max_speed(20.0)
    treadmill_builder.set_incline_levels(15)
    treadmill_builder.set_motor_power(3.5)
    treadmill = treadmill_builder.build()
    
    power_rack_builder = PowerRackBuilder()
    power_rack_builder.set_name("Pro Power Rack")
    power_rack_builder.set_description("Professional Power Rack")
    power_rack_builder.set_base_price(1499.99)
    power_rack_builder.set_dimensions("180x180x240")
    power_rack_builder.set_weight(200.0)
    power_rack_builder.set_max_user_weight(350.0)
    power_rack_builder.set_material("Heavy Duty Steel")
    power_rack_builder.set_weight_capacity(500.0)
    power_rack_builder.set_has_safety_bars(True)
    power_rack_builder.set_has_pull_up_bar(True)
    power_rack = power_rack_builder.build()
    
    output.append(f"Created treadmill: {treadmill.name}")
    output.append(f"Created power rack: {power_rack.name}")
    
    # Decorator Pattern
    output.append("\nDecorator Pattern:")
    output.extend(demonstrate_decorator_pattern().split("\n")[1:])
    
    # Singleton Pattern
    output.append("\nSingleton Pattern:")
    output.extend(demonstrate_singleton_pattern().split("\n")[1:])
    
    # Strategy Pattern
    output.append("\nStrategy Pattern:")
    output.extend(demonstrate_strategy_pattern().split("\n")[1:])
    
    # Observer Pattern
    output.append("\nObserver Pattern:")
    output.extend(demonstrate_observer_pattern().split("\n")[1:])
    
    return "\n".join(output)

if __name__ == "__main__":
    print(demonstrate_all_patterns()) 
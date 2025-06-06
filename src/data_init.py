"""Data initialization module."""
from uuid import uuid4
from src.models.equipment import Equipment, EquipmentSpecs
from src.patterns.singleton import EquipmentInventory

def initialize_sample_data():
    """Initialize sample equipment data."""
    inventory = EquipmentInventory()
    
    # Clear any existing data
    inventory.clear()
    
    # Sample equipment data
    equipment_data = [
        {
            "name": "Бігова доріжка Pro-X",
            "description": "Професійна бігова доріжка з електричним приводом та багатьма програмами тренувань",
            "base_price": 999.99,
            "category": "Кардіо",
            "specs": {
                "weight": "75",
                "dimensions": "180x85x130",
                "material": "Сталь/Пластик",
                "color": "Black",
                "max_user_weight": "150",
                "warranty_months": "24"
            }
        },
        {
            "name": "Велотренажер Cycle-100",
            "description": "Магнітний велотренажер з LCD дисплеєм та датчиками пульсу",
            "base_price": 499.99,
            "category": "Кардіо",
            "specs": {
                "weight": "35",
                "dimensions": "120x60x150",
                "material": "Алюміній/Пластик",
                "color": "Silver",
                "max_user_weight": "120",
                "warranty_months": "12"
            }
        },
        {
            "name": "Силова станція Gym Master",
            "description": "Багатофункціональна силова станція для повноцінного тренування всього тіла",
            "base_price": 1499.99,
            "category": "Силові тренажери",
            "specs": {
                "weight": "200",
                "dimensions": "220x180x200",
                "material": "Сталь",
                "color": "Black/Red",
                "max_user_weight": "150",
                "warranty_months": "36"
            }
        },
        {
            "name": "Гантельний набір Pro Weight",
            "description": "Набір регульованих гантелей від 2 до 24 кг",
            "base_price": 299.99,
            "category": "Вільні ваги",
            "specs": {
                "weight": "48",
                "dimensions": "40x20x20",
                "material": "Сталь/Гума",
                "color": "Black",
                "max_user_weight": "200",
                "warranty_months": "12"
            }
        },
        {
            "name": "Лава для жиму Powerlifting Pro",
            "description": "Професійна лава для жиму лежачи з регульованим кутом нахилу",
            "base_price": 399.99,
            "category": "Силові тренажери",
            "specs": {
                "weight": "45",
                "dimensions": "180x60x130",
                "material": "Сталь",
                "color": "Black",
                "max_user_weight": "300",
                "warranty_months": "24"
            }
        }
    ]
    
    # Add equipment to inventory
    for data in equipment_data:
        specs = data["specs"]
        equipment = Equipment(
            id=str(uuid4()),
            name=data["name"],
            description=data["description"],
            base_price=data["base_price"],
            category=data["category"],
            specs=EquipmentSpecs(
                weight=specs["weight"],
                dimensions=specs["dimensions"],
                material=specs["material"],
                color=specs["color"],
                max_user_weight=specs["max_user_weight"],
                warranty_months=specs["warranty_months"]
            )
        )
        inventory.add_equipment(equipment, quantity=5)  # Add 5 units of each equipment 
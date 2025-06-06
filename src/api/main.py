from typing import List
from uuid import uuid4
from datetime import datetime
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import ValidationError  # Add this import
from src.api.models import (
    EquipmentCreate,
    EquipmentResponse,
    DecorationRequest,
    CreateOrderModel,
    OrderModel,
    OrderResponse
)
from src.models.equipment import Equipment, EquipmentSpecs
from src.models.order import Order
from src.patterns.decorator import (
    WarrantyDecorator,
    InstallationDecorator,
    MaintenanceDecorator,
    InsuranceDecorator
)
from src.patterns.singleton import EquipmentInventory
from src.patterns.chain import OrderProcessorChain
from src.patterns.observer import NotificationSystem, EmailNotifier, SMSNotifier
from src.data_init import initialize_sample_data

EQUIPMENT_NOT_FOUND_MESSAGE = "Equipment not found"

app = FastAPI()

# Initialize sample data
initialize_sample_data()

# Initialize notification system
notification_system = NotificationSystem()
email_notifier = EmailNotifier()
sms_notifier = SMSNotifier()
notification_system.attach(email_notifier)
notification_system.attach(sms_notifier)

# Mount static files directory
app.mount("/static", StaticFiles(directory="src/static"), name="static")

@app.get("/")
async def root():
    """Root endpoint - serves the index.html file."""
    return FileResponse("src/static/index.html")

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}

@app.post("/equipment/", response_model=EquipmentResponse)
async def create_equipment(equipment_data: EquipmentCreate):
    """Create new equipment."""
    # Convert API specs to domain specs
    specs = equipment_data.specs.to_domain()
    
    equipment = Equipment(
        name=equipment_data.name,
        description=equipment_data.description,
        base_price=equipment_data.base_price,
        category=equipment_data.category,
        specs=specs
    )
    
    inventory = EquipmentInventory()
    inventory.add_equipment(equipment, 1)
    
    return equipment

@app.post("/equipment/{equipment_id}/decorate", response_model=EquipmentResponse)
async def decorate_equipment(equipment_id: str, decoration: DecorationRequest):
    """Decorate equipment with additional features."""
    inventory = EquipmentInventory()
    equipment = inventory.get_equipment(equipment_id)
    
    if not equipment:
        raise HTTPException(status_code=404, detail=EQUIPMENT_NOT_FOUND_MESSAGE)
    
    if decoration.decoration_type == "warranty":
        decorated = WarrantyDecorator(equipment, decoration.warranty_months // 12 if decoration.warranty_months else 1)
    elif decoration.decoration_type == "installation":
        decorated = InstallationDecorator(equipment)
    elif decoration.decoration_type == "maintenance":
        decorated = MaintenanceDecorator(equipment, decoration.maintenance_visits or 12)
    elif decoration.decoration_type == "insurance":
        decorated = InsuranceDecorator(equipment, decoration.insurance_level or "basic")
    elif decoration.decoration_type == "premium":
        # Apply all decorators for premium package
        decorated = WarrantyDecorator(
            InstallationDecorator(
                MaintenanceDecorator(
                    InsuranceDecorator(equipment, "premium"),
                    12
                )
            ),
            2
        )
    else:
        raise HTTPException(status_code=400, detail="Invalid decoration type")
    
    # Update equipment in inventory
    inventory.update_equipment(equipment_id, decorated)
    
    return decorated

@app.get("/equipment/", response_model=List[EquipmentResponse])
async def get_equipment():
    """Get all equipment."""
    inventory = EquipmentInventory()
    return list(inventory._equipment_items.values())

@app.get("/equipment/{equipment_id}", response_model=EquipmentResponse)
async def get_equipment_by_id(equipment_id: str):
    """Get equipment by ID."""
    inventory = EquipmentInventory()
    equipment = inventory.get_equipment(equipment_id)
    if not equipment:
        raise HTTPException(status_code=404, detail=EQUIPMENT_NOT_FOUND_MESSAGE)
    return equipment

@app.post("/orders", response_model=OrderResponse)
async def create_order(order_data: CreateOrderModel):
    """Create a new order."""
    try:
        inventory = EquipmentInventory()
        equipment = inventory.get_equipment(order_data.equipment_id)
        
        if not equipment:
            raise HTTPException(status_code=404, detail=EQUIPMENT_NOT_FOUND_MESSAGE)
        
        # Перевірка типів даних
        if not isinstance(order_data.customer_email, str):
            raise HTTPException(status_code=400, detail="customer_email must be a string")
        
        if not isinstance(order_data.shipping_address, str):
            raise HTTPException(status_code=400, detail="shipping_address must be a string")
            
        # Create order
        order = Order(
            equipment=equipment,
            quantity=order_data.quantity,
            customer_id=order_data.customer_id,
            customer_email=order_data.customer_email,
            shipping_address=order_data.shipping_address
        )
        
        # Process order through chain
        processor_chain = OrderProcessorChain()
        if not processor_chain.process_order(order):
            raise HTTPException(status_code=400, detail="Order processing failed")
        
        # Add order to inventory
        inventory.add_order(order)
        
        # Notify observers about the new order
        notification_system.notify(order, "created")
        
        return OrderResponse(
            id=order.id,
            equipment_id=equipment.id,
            customer_id=order.customer_id,
            quantity=order.quantity,
            status=order.status,
            created_at=datetime.now()
        )
        
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=f"Validation error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/orders", response_model=List[OrderModel])
async def get_orders(customer_id: str = None):
    """Get all orders or orders for a specific customer."""
    inventory = EquipmentInventory()
    orders = []
    
    for order in inventory.get_all_orders():
        if customer_id is None or order.customer_id == customer_id:
            orders.append(OrderModel(
                id=order.id,
                customer_id=order.customer_id,
                equipment_id=order.equipment.id if order.equipment else None,
                quantity=order.quantity,
                total_amount=order.get_total_price(),
                status=order.status,
                created_at=datetime.now()  # For simplicity, using current time
            ))
    
    return orders
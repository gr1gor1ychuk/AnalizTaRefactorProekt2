from abc import ABC, abstractmethod
from typing import Dict, Optional
from src.models.equipment import Equipment
from datetime import datetime

DISCOUNT_VALIDATION_MESSAGE = "Discount percent must be between 0 and 100"


class PricingStrategy(ABC):
    """Abstract base class for pricing strategies."""
    
    @abstractmethod
    def calculate_price(self, equipment: Equipment, quantity: int = 1, **kwargs) -> float:
        """Calculate price based on strategy."""
        if quantity <= 0:
            raise ValueError("Quantity must be positive")
        return equipment.base_price * quantity

class RegularPricingStrategy(PricingStrategy):
    """Regular pricing strategy."""
    
    def calculate_price(self, equipment: Equipment, quantity: int = 1, **kwargs) -> float:
        """Calculate regular price."""
        return super().calculate_price(equipment, quantity)

class BulkPricingStrategy(PricingStrategy):
    """Bulk pricing strategy."""
    
    def __init__(self, threshold: int = 5, discount_percent: float = 10.0):
        """Initialize bulk pricing strategy."""
        if threshold <= 0:
            raise ValueError("Threshold must be positive")
        if discount_percent <= 0 or discount_percent >= 100:
            raise ValueError(DISCOUNT_VALIDATION_MESSAGE)
        self.threshold = threshold
        self.discount_percent = min(discount_percent, 20.0)  # Cap at 20% discount

    def calculate_price(self, equipment: Equipment, quantity: int = 1, **kwargs) -> float:
        """Calculate bulk price."""
        base_total = super().calculate_price(equipment, quantity)
        if quantity >= self.threshold:
            discount = base_total * (self.discount_percent / 100)
            return base_total - discount
        return base_total

class SeasonalPricingStrategy(PricingStrategy):
    """Seasonal pricing strategy."""
    
    def __init__(self, discount_percent: float = 20.0):
        """Initialize seasonal pricing strategy."""
        if discount_percent <= 0 or discount_percent >= 100:
            raise ValueError(DISCOUNT_VALIDATION_MESSAGE)
        self.discount_percent = min(discount_percent, 30.0)  # Cap at 30% discount

    def calculate_price(self, equipment: Equipment, quantity: int = 1, **kwargs) -> float:
        """Calculate seasonal price."""
        base_total = super().calculate_price(equipment, quantity)
        # Apply discount during winter months (December, January, February)
        current_month = datetime.now().month
        if current_month in [12, 1, 2]:
            discount = base_total * (self.discount_percent / 100)
            return base_total - discount
        return base_total

class PremiumPricingStrategy(PricingStrategy):
    """Premium pricing strategy."""
    
    def calculate_price(self, equipment: Equipment, quantity: int = 1, **kwargs) -> float:
        """Calculate premium price."""
        base_total = super().calculate_price(equipment, quantity)
        return base_total * 1.2  # 20% markup

class PromoCodePricing(PricingStrategy):
    """Promotional code pricing strategy."""
    
    def __init__(self):
        """Initialize promo code pricing."""
        self._promo_codes: Dict[str, float] = {}

    def add_promo_code(self, code: str, discount_percent: float) -> None:
        """Add promo code."""
        if not code or not isinstance(code, str):
            raise ValueError("Invalid promo code")
        if discount_percent <= 0 or discount_percent >= 100:
            raise ValueError(DISCOUNT_VALIDATION_MESSAGE)
        self._promo_codes[code.strip().upper()] = discount_percent

    def calculate_price(self, equipment: Equipment, quantity: int = 1, **kwargs) -> float:
        """Calculate price with promo code."""
        base_total = super().calculate_price(equipment, quantity)
        promo_code = kwargs.get("promo_code", "").strip().upper()
        if promo_code in self._promo_codes:
            discount = base_total * (self._promo_codes[promo_code] / 100)
            return base_total - discount
        return base_total

class LoyaltyPricing(PricingStrategy):
    """Loyalty points pricing strategy."""
    
    def calculate_price(self, equipment: Equipment, quantity: int = 1, **kwargs) -> float:
        """Calculate price with loyalty points."""
        base_total = super().calculate_price(equipment, quantity)
        loyalty_points = kwargs.get("loyalty_points", 0)
        
        if not isinstance(loyalty_points, (int, float)) or loyalty_points < 0:
            raise ValueError("Invalid loyalty points")
            
        # Convert points to discount
        if loyalty_points >= 200:
            return base_total * 0.85  # 15% discount
        elif loyalty_points >= 100:
            return base_total * 0.90  # 10% discount
        elif loyalty_points >= 50:
            return base_total * 0.95  # 5% discount
        return base_total

class PriceCalculator:
    """Калькулятор цін з використанням різних стратегій"""
    
    def __init__(self, strategy: PricingStrategy):
        self.strategy = strategy
    
    def set_strategy(self, strategy: PricingStrategy):
        self.strategy = strategy
    
    def calculate_price(self, equipment: Equipment, **kwargs) -> float:
        return float(self.strategy.calculate_price(equipment, **kwargs)) 
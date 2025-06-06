"""Tests for pricing strategies."""
import pytest
from src.models.equipment import Equipment, EquipmentSpecs
from src.patterns.strategy import (
    RegularPricingStrategy,
    BulkPricingStrategy,
    SeasonalPricingStrategy,
    PremiumPricingStrategy,
    PromoCodePricing,
    LoyaltyPricing
)

class TestPricingStrategies:
    """Test pricing strategies."""
    @pytest.fixture(autouse=True)
    def setup(self):
        """Set up test equipment."""
        self.equipment = Equipment(
            name="Test Equipment",
            description="Test Description",
            base_price=100.0,
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

    def test_bulk_pricing_small_quantity(self):
        """Test bulk pricing with small quantity."""
        strategy = BulkPricingStrategy(threshold=5, discount_percent=10.0)
        price = strategy.calculate_price(self.equipment, quantity=3)
        assert price == 300.0  # No discount

    def test_bulk_pricing_medium_quantity(self):
        """Test bulk pricing with medium quantity."""
        strategy = BulkPricingStrategy(threshold=5, discount_percent=10.0)
        price = strategy.calculate_price(self.equipment, quantity=5)
        assert price == 450.0  # 10% discount

    def test_bulk_pricing_large_quantity(self):
        """Test bulk pricing with large quantity."""
        strategy = BulkPricingStrategy(threshold=10, discount_percent=15.0)
        price = strategy.calculate_price(self.equipment, quantity=10)
        assert price == 850.0  # 15% discount

    def test_premium_pricing(self):
        """Test premium pricing strategy."""
        strategy = PremiumPricingStrategy()
        price = strategy.calculate_price(self.equipment, quantity=1)
        assert price == 120.0  # 20% markup

    def test_promo_code_pricing_valid_code(self):
        """Test promo code pricing with valid code."""
        strategy = PromoCodePricing()
        strategy.add_promo_code("SAVE10", 10.0)
        price = strategy.calculate_price(self.equipment, quantity=1, promo_code="SAVE10")
        assert price == 90.0  # 10% discount

    def test_promo_code_pricing_invalid_code(self):
        """Test promo code pricing with invalid code."""
        strategy = PromoCodePricing()
        strategy.add_promo_code("SAVE10", 10.0)
        price = strategy.calculate_price(self.equipment, quantity=1, promo_code="INVALID")
        assert price == 100.0  # No discount

    def test_loyalty_pricing_low_points(self):
        """Test loyalty pricing with low points."""
        strategy = LoyaltyPricing()
        price = strategy.calculate_price(self.equipment, quantity=1, loyalty_points=25)
        assert price == 100.0  # No discount

    def test_loyalty_pricing_medium_points(self):
        """Test loyalty pricing with medium points."""
        strategy = LoyaltyPricing()
        price = strategy.calculate_price(self.equipment, quantity=1, loyalty_points=100)
        assert price == 90.0  # 10% discount

    def test_loyalty_pricing_high_points(self):
        """Test loyalty pricing with high points."""
        strategy = LoyaltyPricing()
        price = strategy.calculate_price(self.equipment, quantity=1, loyalty_points=200)
        assert price == 85.0  # 15% discount

    def test_regular_pricing(self):
        """Test regular pricing strategy."""
        strategy = RegularPricingStrategy()
        price = strategy.calculate_price(self.equipment, quantity=1)
        assert price == 100.0

    def test_seasonal_pricing(self):
        """Test seasonal pricing strategy."""
        strategy = SeasonalPricingStrategy(discount_percent=20.0)
        price = strategy.calculate_price(self.equipment, quantity=1)
        # Price depends on current month
        from datetime import datetime
        current_month = datetime.now().month
        if current_month in [12, 1, 2]:
            assert price == 80.0  # Winter discount
        else:
            assert price == 100.0  # No discount

    def test_strategy_switching(self):
        """Test switching between pricing strategies."""
        regular = RegularPricingStrategy()
        bulk = BulkPricingStrategy(threshold=5, discount_percent=10.0)
        premium = PremiumPricingStrategy()

        # Regular price for small quantity
        price = regular.calculate_price(self.equipment, quantity=1)
        assert price == 100.0

        # Bulk price for large quantity
        price = bulk.calculate_price(self.equipment, quantity=5)
        assert price == 450.0

        # Premium price
        price = premium.calculate_price(self.equipment, quantity=1)
        assert price == 120.0

    def test_combined_pricing_scenarios(self):
        """Test combining different pricing strategies."""
        # Start with regular price
        regular = RegularPricingStrategy()
        regular_price = regular.calculate_price(self.equipment, quantity=1)
        assert regular_price == 100.0

        # Apply bulk discount
        bulk = BulkPricingStrategy(threshold=10, discount_percent=15.0)
        bulk_price = bulk.calculate_price(self.equipment, quantity=10)
        assert bulk_price == 850.0  # (100 - 15%) * 10

        # Apply promo code
        promo = PromoCodePricing()
        promo.add_promo_code("SPECIAL", 20.0)
        promo_price = promo.calculate_price(self.equipment, quantity=1, promo_code="SPECIAL")
        assert promo_price == 80.0  # 100 - 20%

        # Apply loyalty points
        loyalty = LoyaltyPricing()
        loyalty_price = loyalty.calculate_price(self.equipment, quantity=1, loyalty_points=200)
        assert loyalty_price == 85.0  # 15% discount 
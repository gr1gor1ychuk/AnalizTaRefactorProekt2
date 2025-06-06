"""Tests for edge cases."""
import pytest
from datetime import datetime
from src.models.equipment import Equipment, EquipmentSpecs
from src.patterns.strategy import (
    RegularPricingStrategy,
    BulkPricingStrategy,
    SeasonalPricingStrategy,
    PremiumPricingStrategy,
    PromoCodePricing,
    LoyaltyPricing
)

class TestPricingEdgeCases:
    """Test pricing edge cases."""
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

    def test_negative_base_price(self):
        """Test equipment with negative base price."""
        with pytest.raises(ValueError):
            Equipment(
                name="Test Equipment",
                description="Test Description",
                base_price=-100.0,
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

    def test_zero_base_price(self):
        """Test equipment with zero base price."""
        with pytest.raises(ValueError, match="Base price must be a positive number"):
            Equipment(
                name="Test Equipment",
                description="Test Description",
                base_price=0.0,
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

    def test_bulk_pricing_negative_quantity(self):
        """Test bulk pricing with negative quantity."""
        strategy = BulkPricingStrategy(threshold=5, discount_percent=10.0)
        with pytest.raises(ValueError):
            strategy.calculate_price(self.equipment, quantity=-1)

    def test_bulk_pricing_zero_quantity(self):
        """Test bulk pricing with zero quantity."""
        strategy = BulkPricingStrategy(threshold=5, discount_percent=10.0)
        with pytest.raises(ValueError):
            strategy.calculate_price(self.equipment, quantity=0)

    def test_seasonal_pricing_invalid_discount(self):
        """Test seasonal pricing with invalid discount."""
        with pytest.raises(ValueError):
            SeasonalPricingStrategy(discount_percent=101.0)

    def test_promo_code_whitespace(self):
        """Test promo code with whitespace."""
        strategy = PromoCodePricing()
        strategy.add_promo_code("  TEST10  ", 10.0)
        price = strategy.calculate_price(self.equipment, quantity=1, promo_code="TEST10")
        assert price == 90.0  # 10% discount

    def test_promo_code_case_sensitivity(self):
        """Test promo code case sensitivity."""
        strategy = PromoCodePricing()
        strategy.add_promo_code("TEST10", 10.0)
        price = strategy.calculate_price(self.equipment, quantity=1, promo_code="test10")
        assert price == 90.0  # 10% discount

    def test_promo_code_special_characters(self):
        """Test promo code with special characters."""
        strategy = PromoCodePricing()
        strategy.add_promo_code("TEST#10!", 10.0)
        price = strategy.calculate_price(self.equipment, quantity=1, promo_code="TEST#10!")
        assert price == 90.0  # 10% discount

    def test_loyalty_points_float(self):
        """Test loyalty points with float value."""
        strategy = LoyaltyPricing()
        price = strategy.calculate_price(self.equipment, quantity=1, loyalty_points=150.5)
        assert price == 90.0  # 10% discount for 100-199 points

    def test_loyalty_points_negative(self):
        """Test loyalty points with negative value."""
        strategy = LoyaltyPricing()
        with pytest.raises(ValueError):
            strategy.calculate_price(self.equipment, quantity=1, loyalty_points=-100)

    def test_extreme_values(self):
        """Test extreme values for pricing strategies."""
        # Test bulk pricing with very large quantity
        bulk = BulkPricingStrategy(threshold=1000, discount_percent=20.0)
        bulk_price = bulk.calculate_price(self.equipment, quantity=1000)
        assert bulk_price == 80000.0  # Maximum 20% discount

        # Test seasonal pricing with maximum discount
        seasonal = SeasonalPricingStrategy(discount_percent=30.0)
        seasonal_price = seasonal.calculate_price(self.equipment, quantity=1)
        if datetime.now().month in [12, 1, 2]:
            assert seasonal_price == 70.0  # Maximum 30% discount
        else:
            assert seasonal_price == 100.0  # No discount

        # Test loyalty pricing with very high points
        loyalty = LoyaltyPricing()
        loyalty_price = loyalty.calculate_price(self.equipment, quantity=1, loyalty_points=1000)
        assert loyalty_price == 85.0  # Maximum 15% discount

    def test_multiple_strategy_changes(self):
        """Test changing strategies multiple times."""
        strategies = [
            BulkPricingStrategy(threshold=5, discount_percent=10.0),
            SeasonalPricingStrategy(discount_percent=20.0),
            PromoCodePricing(),
            LoyaltyPricing()
        ]

        prices = []
        for strategy in strategies:
            if isinstance(strategy, PromoCodePricing):
                strategy.add_promo_code("TEST", 10.0)
                price = strategy.calculate_price(self.equipment, quantity=1, promo_code="TEST")
            elif isinstance(strategy, LoyaltyPricing):
                price = strategy.calculate_price(self.equipment, quantity=1, loyalty_points=100)
            elif isinstance(strategy, BulkPricingStrategy):
                price = strategy.calculate_price(self.equipment, quantity=5)
            else:
                price = strategy.calculate_price(self.equipment, quantity=1)
            prices.append(price)

        # Expected prices:
        # BulkPricing(5) -> 450.0 (10% discount * 5)
        # SeasonalPricing(0.2) -> 80.0 or 100.0 (depends on month)
        # PromoCodePricing("TEST", 0.1) -> 90.0 (10% discount)
        # LoyaltyPricing(100) -> 90.0 (10% discount)
        from datetime import datetime
        if datetime.now().month in [12, 1, 2]:
            expected_prices = [450.0, 80.0, 90.0, 90.0]
        else:
            expected_prices = [450.0, 100.0, 90.0, 90.0]
        assert all(abs(a - b) < 0.0001 for a, b in zip(prices, expected_prices))

    def test_invalid_specs(self):
        """Test invalid equipment specifications."""
        with pytest.raises(ValueError):
            EquipmentSpecs(
                weight="-75.0",  # Negative weight
                dimensions="200x100x220",
                material="Steel",
                color="Black",
                max_user_weight="150.0",
                warranty_months="12"
            )

if __name__ == '__main__':
    pytest.main() 
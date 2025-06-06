"""Tests for demo module."""
import pytest
from src.demo import (
    create_demo_equipment,
    demonstrate_decorator_pattern,
    demonstrate_singleton_pattern,
    demonstrate_strategy_pattern,
    demonstrate_observer_pattern,
    demonstrate_all_patterns
)

def test_create_demo_equipment():
    """Test creating demo equipment."""
    output = create_demo_equipment()
    assert isinstance(output, list)
    assert len(output) > 0
    assert all(isinstance(item, str) for item in output)
    assert any("Treadmill" in item for item in output)
    assert any("Power Rack" in item for item in output)

def test_demonstrate_decorator_pattern():
    """Test decorator pattern demonstration."""
    output = demonstrate_decorator_pattern()
    assert isinstance(output, str)
    assert "Decorator Pattern" in output
    assert "Base Price" in output
    assert "With Warranty" in output
    assert "With Insurance" in output
    assert "With Maintenance" in output
    assert "With Installation" in output

def test_demonstrate_singleton_pattern():
    """Test singleton pattern demonstration."""
    output = demonstrate_singleton_pattern()
    assert isinstance(output, str)
    assert "Singleton Pattern" in output
    assert "Equipment added to inventory" in output

def test_demonstrate_strategy_pattern():
    """Test strategy pattern demonstration."""
    output = demonstrate_strategy_pattern()
    assert isinstance(output, str)
    assert "Strategy Pattern" in output
    assert "Regular=" in output
    assert "Bulk(5)" in output
    assert "Seasonal=" in output
    assert "Premium=" in output

def test_demonstrate_observer_pattern():
    """Test observer pattern demonstration."""
    output = demonstrate_observer_pattern()
    assert isinstance(output, str)
    assert "Observer Pattern" in output
    assert "Successfully sent notifications" in output

def test_demonstrate_all_patterns():
    """Test demonstrating all patterns."""
    output = demonstrate_all_patterns()
    assert isinstance(output, str)
    assert "Decorator Pattern" in output
    assert "Singleton Pattern" in output
    assert "Strategy Pattern" in output
    assert "Observer Pattern" in output 
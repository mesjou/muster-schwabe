# ruff: noqa: PLR2004

import pandas as pd
import pytest

from src.services.analyzer import analyze_transactions, categorize_transaction


@pytest.mark.parametrize(
    "description,expected_category",
    [
        # Food & Dining
        ("Restaurant ABC", "Food & Dining"),
        ("REWE Supermarket", "Food & Dining"),
        ("Lidl Grocery Store", "Food & Dining"),
        # Transportation
        ("Deutsche Bahn Ticket", "Transportation"),
        ("DB Train", "Transportation"),
        ("Uber Ride", "Transportation"),
        ("Gas Station", "Transportation"),
        # Entertainment
        ("Netflix Subscription", "Entertainment"),
        ("Cinema Ticket", "Entertainment"),
        ("Spotify Premium", "Entertainment"),
        # Shopping
        ("Amazon Purchase", "Shopping"),
        ("Walmart Shopping", "Shopping"),
        # Health & Fitness
        ("Gym Membership", "Health & Fitness"),
        ("Pharmacy Purchase", "Health & Fitness"),
        # Utilities
        ("Electricity Bill", "Utilities"),
        ("Internet Bill", "Utilities"),
        # Unknown category
        ("Unknown Transaction", "Other"),
    ],
)
def test_categorize_transaction(description: str, expected_category: str):
    """Test transaction categorization with various descriptions."""
    assert categorize_transaction(description) == expected_category


def test_analyze_transactions():
    # Create test data
    data = {
        "Date": [
            "2024-01-01",
            "2024-01-01",
            "2024-01-02",
            "2024-01-02",
            "2024-01-03",
        ],
        "Description": [
            "Restaurant ABC",
            "DB Train Ticket",
            "Netflix Subscription",
            "Amazon Purchase",
            "Gym Membership",
        ],
        "Amount": [
            -50.0,  # Food & Dining
            -30.0,  # Transportation
            -15.0,  # Entertainment
            -100.0,  # Shopping
            -40.0,  # Health & Fitness
        ],
    }
    df = pd.DataFrame(data)

    # Analyze transactions
    result = analyze_transactions(df)

    # Test summary
    assert result["summary"]["total"] == 235.0  # Sum of all negative amounts

    # Test by_category
    assert result["by_category"]["Food & Dining"] == 50.0
    assert result["by_category"]["Transportation"] == 30.0
    assert result["by_category"]["Entertainment"] == 15.0
    assert result["by_category"]["Shopping"] == 100.0
    assert result["by_category"]["Health & Fitness"] == 40.0

    # Test daily_spending
    daily_spending = {item["date"]: item["amount"] for item in result["daily_spending"]}
    assert daily_spending["2024-01-01"] == 80.0  # 50 + 30
    assert daily_spending["2024-01-02"] == 115.0  # 15 + 100
    assert daily_spending["2024-01-03"] == 40.0  # 40


def test_analyze_transactions_with_positive_amounts():
    # Create test data with positive amounts (income)
    data = {
        "Date": ["2024-01-01", "2024-01-02"],
        "Description": ["Salary", "Refund"],
        "Amount": [2000.0, 100.0],  # Positive amounts
    }
    df = pd.DataFrame(data)

    # Analyze transactions
    result = analyze_transactions(df)

    # Test summary
    assert result["summary"]["total"] == 0.0  # No negative amounts

    # Test by_category
    assert len(result["by_category"]) == 0  # No categories for positive amounts

    # Test daily_spending
    assert len(result["daily_spending"]) == 0  # No daily spending for positive amounts


def test_analyze_transactions_with_mixed_data():
    # Create test data with mixed positive and negative amounts
    data = {
        "Date": ["2024-01-01", "2024-01-01", "2024-01-02"],
        "Description": ["Salary", "Restaurant", "Shopping"],
        "Amount": [2000.0, -50.0, -100.0],
    }
    df = pd.DataFrame(data)

    # Analyze transactions
    result = analyze_transactions(df)

    # Test summary
    assert result["summary"]["total"] == 150.0  # Sum of negative amounts only

    # Test by_category
    assert result["by_category"]["Food & Dining"] == 50.0
    assert result["by_category"]["Shopping"] == 100.0

    # Test daily_spending
    daily_spending = {item["date"]: item["amount"] for item in result["daily_spending"]}
    assert daily_spending["2024-01-01"] == 50.0
    assert daily_spending["2024-01-02"] == 100.0

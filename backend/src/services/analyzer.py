import pandas as pd


def categorize_transaction(description: str) -> str:
    """Categorize a transaction based on its description."""
    description = description.lower()
    categories = {
        "Food & Dining": ["restaurant", "cafe", "grocery", "supermarket", "food", "rewe", "lidl"],
        "Housing & Rent": ["rent", "mortgage", "housing"],
        "Transportation": ["uber", "lyft", "taxi", "transport", "fuel", "gas", "deutsche bahn", "db"],
        "Entertainment": ["netflix", "spotify", "cinema", "theater", "concert"],
        "Shopping": ["amazon", "walmart", "target", "shop", "store"],
        "Health & Fitness": ["gym", "fitness", "health", "medical", "pharmacy"],
        "Utilities": ["electricity", "water", "internet", "phone", "utility"],
    }

    for category, keywords in categories.items():
        if any(keyword.lower() in description for keyword in keywords):
            return category
    return "Other"


def analyze_transactions(df: pd.DataFrame) -> dict:
    """Analyze transactions and return summary statistics."""
    # Convert date column to datetime
    df["Date"] = pd.to_datetime(df["Date"])

    # Ensure amount is numeric
    df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce")

    # Categorize transactions
    df["Category"] = df["Description"].apply(categorize_transaction)

    # Calculate summary
    total_spending = df[df["Amount"] < 0]["Amount"].sum() * -1

    # Calculate spending by category
    by_category = df[df["Amount"] < 0].groupby("Category")["Amount"].sum().abs().to_dict()

    # Calculate daily spending
    daily_spending = df[df["Amount"] < 0].groupby("Date")["Amount"].sum().abs()
    daily_spending_list = [
        {"date": date.strftime("%Y-%m-%d"), "amount": float(amount)} for date, amount in daily_spending.items()
    ]

    return {
        "summary": {"total": float(total_spending)},
        "by_category": by_category,
        "daily_spending": daily_spending_list,
    }

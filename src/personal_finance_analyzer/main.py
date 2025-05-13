from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# Set up the style for plots
plt.style.use("seaborn")
sns.set_palette("husl")


class FinanceAnalyzer:
    def __init__(self):
        self.categories = {
            "Food & Dining": ["restaurant", "cafe", "grocery", "supermarket", "food"],
            "Housing & Rent": ["rent", "mortgage", "housing"],
            "Transportation": ["uber", "lyft", "taxi", "transport", "fuel", "gas"],
            "Entertainment": ["netflix", "spotify", "cinema", "theater", "concert"],
            "Shopping": ["amazon", "walmart", "target", "shop", "store"],
            "Health & Fitness": ["gym", "fitness", "health", "medical", "pharmacy"],
            "Utilities": ["electricity", "water", "internet", "phone", "utility"],
            "Other": [],  # Default category
        }

    def load_data(self, file_path):
        """Load and preprocess the CSV file."""
        try:
            df = pd.read_csv(file_path)
            # Convert date column to datetime
            df["Date"] = pd.to_datetime(df["Date"])
            # Ensure amount is numeric
            df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce")
            return df
        except Exception as e:
            print(f"Error loading data: {e}")
            return None

    def categorize_transaction(self, description):
        """Categorize a transaction based on its description."""
        description = description.lower()
        for category, keywords in self.categories.items():
            if any(keyword in description for keyword in keywords):
                return category
        return "Other"

    def analyze_transactions(self, df):
        """Analyze transactions and add categories."""
        df["Category"] = df["Description"].apply(self.categorize_transaction)
        return df

    def plot_spending_by_category(self, df):
        """Create a pie chart of spending by category."""
        plt.figure(figsize=(10, 6))
        category_totals = df[df["Amount"] < 0].groupby("Category")["Amount"].sum().abs()
        plt.pie(category_totals, labels=category_totals.index, autopct="%1.1f%%")
        plt.title("Spending by Category")
        plt.axis("equal")
        plt.show()

    def plot_daily_spending(self, df):
        """Create a line plot of daily spending."""
        plt.figure(figsize=(12, 6))
        daily_spending = df[df["Amount"] < 0].groupby("Date")["Amount"].sum().abs()
        plt.plot(daily_spending.index, daily_spending.values)
        plt.title("Daily Spending")
        plt.xlabel("Date")
        plt.ylabel("Amount")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    def plot_category_trends(self, df):
        """Create a bar plot of spending trends by category."""
        plt.figure(figsize=(12, 6))
        category_totals = df[df["Amount"] < 0].groupby("Category")["Amount"].sum().abs()
        sns.barplot(x=category_totals.index, y=category_totals.values)
        plt.title("Total Spending by Category")
        plt.xlabel("Category")
        plt.ylabel("Amount")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()


def main():
    # Create data directory if it doesn't exist
    Path("data").mkdir(exist_ok=True)

    analyzer = FinanceAnalyzer()

    # Check if there are any CSV files in the data directory
    data_files = list(Path("data").glob("*.csv"))

    if not data_files:
        print("Please place your banking CSV file in the 'data' directory.")
        return

    # Use the first CSV file found
    file_path = data_files[0]
    print(f"Analyzing file: {file_path}")

    # Load and analyze the data
    df = analyzer.load_data(file_path)
    if df is not None:
        df = analyzer.analyze_transactions(df)

        # Generate visualizations
        analyzer.plot_spending_by_category(df)
        analyzer.plot_daily_spending(df)
        analyzer.plot_category_trends(df)

        # Print summary statistics
        print("\nSummary Statistics:")
        print(f"Total number of transactions: {len(df)}")
        print(f"Total spending: ${df[df['Amount'] < 0]['Amount'].sum():.2f}")
        print("\nSpending by category:")
        print(df[df["Amount"] < 0].groupby("Category")["Amount"].sum().abs())


if __name__ == "__main__":
    main()

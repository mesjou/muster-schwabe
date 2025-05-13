# Personal Finance Analyzer

This application helps you analyze your banking transactions by categorizing them and providing visual insights into your spending patterns.

## Features

- Import banking transaction data from CSV files
- Categorize transactions (food, rent, sports, etc.)
- Visualize spending patterns through various plots
- Track monthly spending by category

## Setup

1. Install uv (if not already installed):
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

2. Create a virtual environment and install dependencies:
```bash
uv venv
source .venv/bin/activate
uv pip install -e .
```

3. Place your banking CSV file in the `data` directory

4. Run the application:
```bash
python main.py
```

## CSV File Format

The application expects a CSV file with the following columns:
- Date
- Description
- Amount
- Balance

## Categories

The application uses the following default categories:
- Food & Dining
- Housing & Rent
- Transportation
- Entertainment
- Shopping
- Health & Fitness
- Utilities
- Other

You can modify these categories in the `main.py` file.

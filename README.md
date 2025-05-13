# Personal Finance Analyzer

A web application that helps you analyze your personal finances by processing CSV files of banking transactions, categorizing expenses, and visualizing spending patterns.

## Features

- Upload CSV files of banking transactions
- Automatic categorization of expenses
- Interactive visualizations:
  - Pie chart of spending by category
  - Bar chart of spending by category
  - Line chart of daily spending trends
- Summary statistics

## Project Structure

```
.
├── backend/               # Python FastAPI backend
│   ├── src/              # Source code
│   │   ├── __init__.py   # Package initialization
│   │   ├── main.py       # FastAPI application
│   │   └── services/     # Business logic
│   │       ├── __init__.py
│   │       └── analyzer.py
│   ├── pyproject.toml    # Python package configuration
│   └── run.py           # Script to run the backend
└── frontend/            # React TypeScript frontend
    ├── src/             # Source code
    │   └── App.tsx      # Main application component
    └── package.json     # Node.js dependencies
```

## Prerequisites

- Python 3.8 or higher
- Node.js 16 or higher
- npm or yarn
- uv (Python package installer)

## Setup and Running

### Backend

1. Install uv (if not already installed):
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. Navigate to the backend directory:
   ```bash
   cd backend
   ```

3. Create and activate a virtual environment:
   ```bash
   # On macOS/Linux
   uv venv
   source .venv/bin/activate
   ```

4. Install dependencies:
   ```bash
   uv pip install -e .
   ```

5. Start the backend server:
   ```bash
   python run.py
   ```

The backend will be available at http://localhost:8000

### Frontend

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm run dev
   ```

The frontend will be available at http://localhost:3000

## Usage

1. Prepare your banking transaction data in CSV format with the following columns:
   - Date
   - Description
   - Amount

2. Open the application in your browser at http://localhost:3000
3. Drag and drop your CSV file or click to select it
4. View the analysis and visualizations

## Development

### Backend

- FastAPI backend with automatic API documentation at http://localhost:8000/docs
- Uses Pandas for data processing
- Transaction categorization based on description keywords
- Built with Python 3.8+ and modern Python packaging (pyproject.toml)
- Uses uv for fast and reliable package management

### Frontend

- React with TypeScript
- Material-UI for components
- Recharts for data visualization
- File upload with drag-and-drop support

## License

MIT

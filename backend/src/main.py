import io

import pandas as pd
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from .services.analyzer import analyze_transactions
from .services.anonymizer import anonymize_dataframe

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Transaction(BaseModel):
    Date: str
    Description: str
    Amount: float
    Category: str = "Other"


class AnalysisResponse(BaseModel):
    summary: dict[str, float]
    by_category: dict[str, float]
    daily_spending: list[dict[str, float]]


# Define the expected header as a module-level constant
EXPECTED_HEADER = (
    '"Buchungsdatum";"Wertstellung";"Status";"Zahlungspflichtige*r";'
    '"Zahlungsempfänger*in";"Verwendungszweck";"Umsatztyp";"IBAN";'
    '"Betrag (€)";"Gläubiger-ID";"Mandatsreferenz";"Kundenreferenz"'
)


@app.post("/api/analyze", response_model=AnalysisResponse)
async def analyze_transactions_endpoint(file: UploadFile = None):
    if file is None:
        file = await File(...)

    # Read the file as text
    content = await file.read()
    text = content.decode("utf-8")
    lines = text.splitlines()

    # Find the header row with the exact match
    header_idx = None
    for i, line in enumerate(lines):
        if line.strip() == EXPECTED_HEADER:
            header_idx = i
            break

    if header_idx is None:
        return {"error": "Could not find the expected header row in the CSV."}

    # Read the CSV from the header row
    csv_data = "\n".join(lines[header_idx:])
    df = pd.read_csv(io.StringIO(csv_data), sep=";", quotechar='"')

    # Select and rename the required columns
    columns_to_keep = {
        "Buchungsdatum": "Date",
        "Zahlungsempfänger*in": "Recipient",
        "Verwendungszweck": "Description",
        "Betrag (€)": "Amount",
    }

    # Keep only the columns we need and rename them
    df = df[list(columns_to_keep.keys())].rename(columns=columns_to_keep)

    # Anonymize sensitive data
    df = anonymize_dataframe(df)

    # Convert date format (assuming DD.MM.YY format)
    df["Date"] = pd.to_datetime(df["Date"], format="%d.%m.%Y", errors="coerce")

    # Convert amount format (handling German number format)
    df["Amount"] = (
        df["Amount"]
        .astype(str)
        .str.replace(".", "", regex=False)  # Remove thousands separator
        .str.replace(",", ".", regex=False)  # Convert decimal comma to dot
        .astype(float)
    )

    # Combine recipient and description for better categorization
    df["Description"] = df["Recipient"] + " - " + df["Description"]

    # Analyze transactions
    return analyze_transactions(df)


@app.get("/health")
async def health_check():
    return {"status": "ok"}

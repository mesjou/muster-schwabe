from typing import Dict, List

import pandas as pd
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from .services.analyzer import analyze_transactions

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
    summary: Dict[str, float]
    by_category: Dict[str, float]
    daily_spending: List[Dict[str, float]]


@app.post("/api/analyze", response_model=AnalysisResponse)
async def analyze_transactions_endpoint(file: UploadFile = None):
    if file is None:
        file = await File(...)

    # Read CSV file
    df = pd.read_csv(file.file)

    # Analyze transactions
    return analyze_transactions(df)


@app.get("/health")
async def health_check():
    return {"status": "ok"}

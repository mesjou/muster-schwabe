"""Module for anonymizing sensitive data in DataFrames."""
from typing import Optional

import pandas as pd
from faker import Faker
from schwifty import IBAN

# Initialize Faker for generating realistic anonymized data
fake = Faker("de_DE")


ANONYMOUS_VALUE = "XXXXXXX"


def is_valid_iban(text: str) -> bool:
    """Check if a string is a valid IBAN."""
    try:
        IBAN(text.replace(" ", ""))
        return True
    except ValueError:
        return False


def is_valid_email(text: str) -> bool:
    """Check if a string is a valid email."""
    if "@" in text and "." in text.split("@")[1]:
        return True
    return False


def anonymize_text(text: Optional[str]) -> Optional[str]:
    """Anonymize sensitive information in a text string."""
    if not isinstance(text, str):
        return text

    # Check for IBAN
    if is_valid_iban(text):
        return ANONYMOUS_VALUE

    # Check for email addresses
    if is_valid_email(text):
        return ANONYMOUS_VALUE

    return text


def anonymize_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Anonymize sensitive data in all columns of the DataFrame."""
    # Create a copy to avoid modifying the original
    df_anon = df.copy()

    # Process all columns
    for col in df_anon.columns:
        # Convert column to string type to ensure we can process all values
        df_anon[col] = df_anon[col].astype(str)
        # Apply anonymization
        df_anon[col] = df_anon[col].apply(anonymize_text)

    return df_anon

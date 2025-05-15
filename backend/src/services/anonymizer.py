"""Module for anonymizing sensitive data in DataFrames."""
from typing import Any

import pandas as pd
import phonenumbers
from faker import Faker
from schwifty import IBAN

# Initialize Faker for generating realistic anonymized data
fake = Faker("de_DE")


def is_valid_iban(text: str) -> bool:
    """Check if a string is a valid IBAN."""
    if not isinstance(text, str):
        return False
    try:
        IBAN(text.replace(" ", ""))
        return True
    except ValueError:
        return False


def anonymize_text(text: Any) -> Any:
    """Anonymize sensitive information in a text string."""
    if not isinstance(text, str):
        return text

    # Check for IBAN
    if is_valid_iban(text):
        return fake.iban()

    # Check for phone numbers (both international and German format)
    try:
        # Try to parse as German number first
        number = phonenumbers.parse(text, "DE")
        if phonenumbers.is_valid_number(number):
            return fake.phone_number()
    except phonenumbers.NumberParseException:
        pass

    # Check for email addresses
    if "@" in text and "." in text.split("@")[1]:
        return fake.email()

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

from typing import Any, Optional

import pandas as pd

from src.services.anonymizer import anonymize_dataframe, anonymize_text, is_valid_iban


def test_is_valid_iban():
    # Test valid IBANs
    assert is_valid_iban("DE89370400440532013000")
    assert is_valid_iban("DE89 3704 0044 0532 0130 00")

    # Test invalid IBANs
    assert not is_valid_iban("invalid")
    assert not is_valid_iban("DE8937040044053201300")  # Too short
    assert not is_valid_iban(str(None))  # Convert None to string
    assert not is_valid_iban(str(123))  # Convert int to string


def test_anonymize_text():
    # Test IBAN anonymization
    original_iban = "DE89370400440532013000"
    anonymized_iban = anonymize_text(original_iban)
    assert anonymized_iban != original_iban
    assert is_valid_iban(anonymized_iban)

    # Test phone number anonymization
    original_phone = "+491234567890"
    anonymized_phone = anonymize_text(original_phone)
    assert anonymized_phone != original_phone
    assert "+" in anonymized_phone

    # Test email anonymization
    original_email = "test@example.com"
    anonymized_email = anonymize_text(original_email)
    assert anonymized_email != original_email
    assert "@" in anonymized_email
    assert "." in anonymized_email

    # Test non-sensitive text
    original_text = "Regular text"
    assert anonymize_text(original_text) == original_text

    # Test non-string input
    non_string_input: Any = 123
    none_input: Optional[str] = None
    assert anonymize_text(non_string_input) == non_string_input
    assert anonymize_text(none_input) is None


def test_anonymize_dataframe():
    # Create test DataFrame with sensitive data
    df = pd.DataFrame(
        {
            "iban": ["DE89370400440532013000", "DE89370400440532013001"],
            "phone": ["+491234567890", "+499876543210"],
            "email": ["test1@example.com", "test2@example.com"],
            "regular_text": ["Hello", "World"],
        }
    )

    # Anonymize the DataFrame
    df_anon = anonymize_dataframe(df)

    # Check that all columns were processed
    assert len(df_anon.columns) == len(df.columns)

    # Check that sensitive data was anonymized
    for i in range(len(df)):
        # IBAN should be different but valid
        assert df_anon.iloc[i]["iban"] != df.iloc[i]["iban"]
        assert is_valid_iban(df_anon.iloc[i]["iban"])

        # Phone should be different but contain +
        assert df_anon.iloc[i]["phone"] != df.iloc[i]["phone"]
        assert "+" in df_anon.iloc[i]["phone"]

        # Email should be different but contain @ and .
        assert df_anon.iloc[i]["email"] != df.iloc[i]["email"]
        assert "@" in df_anon.iloc[i]["email"]
        assert "." in df_anon.iloc[i]["email"]

        # Regular text should remain unchanged
        assert df_anon.iloc[i]["regular_text"] == df.iloc[i]["regular_text"]


def test_anonymize_dataframe_with_mixed_types():
    # Create test DataFrame with mixed data types
    df = pd.DataFrame(
        {
            "text": ["DE89370400440532013000", 123, None],
            "numbers": [1, 2, 3],
            "mixed": ["test@example.com", 456, "+491234567890"],
        }
    )

    # Anonymize the DataFrame
    df_anon = anonymize_dataframe(df)

    # Check that all values were converted to strings
    assert all(df_anon.dtypes == "object")

    # Check that sensitive data was anonymized
    assert is_valid_iban(df_anon.iloc[0]["text"])
    assert "@" in df_anon.iloc[0]["mixed"]
    assert "+" in df_anon.iloc[2]["mixed"]

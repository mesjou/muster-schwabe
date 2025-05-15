from typing import Any, Optional

import pandas as pd

from src.services.anonymizer import ANONYMOUS_VALUE, anonymize_dataframe, anonymize_text, is_valid_email, is_valid_iban


def test_is_valid_iban():
    # Test valid IBANs
    assert is_valid_iban("DE89370400440532013000")
    assert is_valid_iban("DE89 3704 0044 0532 0130 00")

    # Test invalid IBANs
    assert not is_valid_iban("invalid")
    assert not is_valid_iban("DE8937040044053201300")  # Too short
    assert not is_valid_iban(str(None))  # Convert None to string
    assert not is_valid_iban(str(123))  # Convert int to string


def test_is_valid_email():
    # Test valid emails
    assert is_valid_email("test@example.com")
    assert is_valid_email("test.test@example.com")
    assert is_valid_email("test@subdomain.example.com")

    # Test invalid emails
    assert not is_valid_email("invalid")
    assert not is_valid_email("test@")
    assert not is_valid_email("test@example")


def test_anonymize_text():
    # Test IBAN anonymization
    original_iban = "DE89370400440532013000"
    anonymized_iban = anonymize_text(original_iban)
    assert anonymized_iban == ANONYMOUS_VALUE
    # Test phone number anonymization
    original_phone = "+491234567890"
    anonymized_phone = anonymize_text(original_phone)
    assert anonymized_phone == original_phone

    # Test email anonymization
    original_email = "test@example.com"
    anonymized_email = anonymize_text(original_email)
    assert anonymized_email == ANONYMOUS_VALUE

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
            "iban": ["DE89370400440532013000", "DE89370400440532013000"],
            "email": ["test1@example.com", "test2@example.com"],
            "regular_text": ["Hello", "World"],
        }
    )

    df_result = pd.DataFrame(
        {
            "iban": [ANONYMOUS_VALUE, ANONYMOUS_VALUE],
            "email": [ANONYMOUS_VALUE, ANONYMOUS_VALUE],
            "regular_text": ["Hello", "World"],
        }
    )

    # Anonymize the DataFrame
    df_anon = anonymize_dataframe(df)

    # Check that all columns were processed
    print(df_anon, df_result)
    pd.testing.assert_frame_equal(df_anon, df_result)


def test_anonymize_dataframe_with_mixed_types():
    # Create test DataFrame with mixed data types
    df = pd.DataFrame(
        {
            "text": ["DE89370400440532013000", 123, None],
            "numbers": [1, 2, 3],
            "mixed": ["test@example.com", 456, "+491234567890"],
        }
    )

    df_result = pd.DataFrame(
        {
            "text": [ANONYMOUS_VALUE, "123", str(None)],
            "numbers": ["1", "2", "3"],
            "mixed": [ANONYMOUS_VALUE, "456", "+491234567890"],
        }
    )

    # Anonymize the DataFrame
    df_anon = anonymize_dataframe(df)

    # Check that all values were converted to strings
    pd.testing.assert_frame_equal(df_anon, df_result)

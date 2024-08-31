import hashlib, pytest
from datetime import datetime
from typing import Dict, Tuple
from utils import *

@pytest.fixture
def expected_codes() -> Dict[Tuple[str, str], str]:
    test_cases = [
        ('Product A', 'Category 1'),
        ('Product B', 'Category 2'),
        ('Product C', 'Category 3'),
        ('Product D', 'Category 4'),
    ]
    return {
        (name, category): hashlib.md5(f"{name}{category}".encode()).hexdigest()
        for name, category in test_cases
    }

@pytest.mark.parametrize("name, category", [
    ('Product A', 'Category 1'),
    ('Product B', 'Category 2'),
    ('Product C', 'Category 3'),
    ('Product D', 'Category 4'),
])

def test_generate_unique_code(name: str, category: str, expected_codes: Dict[Tuple[str, str], str]) -> None:
    result = generate_unique_code(name, category)
    expected_code = expected_codes.get((name, category))
    # Assert that the result matches the expected output
    assert result == expected_code, f"Expected {expected_code}, but got {result} for inputs ({name}, {category})"
    # Assert that the result is a string
    assert isinstance(result, str), f"Expected the result to be a string, but got {type(result).__name__}"
    # Assert that the result has the correct length (32 characters for MD5)
    assert len(result) == 32, f"Expected the result to be 32 characters long, but got {len(result)}"

def test_generate_unique_code_fail() -> None:
    result = generate_unique_code('Product E', 'Category 5')
    expected_code = 'incorrect_hash_value'
    # Assert that the result is a string
    assert isinstance(result, str), f"Expected the result to be a string, but got {type(result).__name__}"
    # Assert that the result has the correct length (32 characters for MD5)
    assert len(result) == 32, f"Expected the result to be 32 characters long, but got {len(result)}"
    # Assert that the result does not match the intentionally incorrect expected code
    assert result != expected_code, f"Expected {expected_code}, but got {result}"

def test_random_string() -> None:
    result = random_string()
    # Assert that the result is a string
    assert isinstance(result, str), f"Expected the result to be a string, but got {type(result).__name__}"
    # Assert that the result contains at least one space
    assert ' ' in result, "Expected the result to contain a space"
    # Assert that the length of the result is within the expected range
    length = len(result)
    assert 8 <= length <= 18, f"Expected the result length to be between 8 and 18, but got {length}"

def test_random_price() -> None:
    min_price = 0.01
    max_price = 10000.00
    result = random_price(min_price, max_price)
    # Assert that the result is a float
    assert isinstance(result, float), f"Expected the result to be a float, but got {type(result).__name__}"
    # Assert that the result is within the specified range
    assert min_price <= result <= max_price, f"Expected the result to be between {min_price} and {max_price}, but got {result}"
    # Assert that the result has exactly two decimal places
    assert str(result).count('.') <= 1, f"Expected the result to have two decimal places, but got {result}"
    _, decimal_part = str(result).split('.') if '.' in str(result) else (str(result), '')
    assert len(decimal_part) == 2, f"Expected the result to have two decimal places, but got {result}"

def test_random_product() -> None:
    result = random_product()
    # Assert that result is a dictionary
    assert isinstance(result, dict), f"Expected the result to be a dictionary, but got {type(result).__name__}"
    # Assert that the dictionary contains the expected keys
    expected_keys = {"name", "category", "code", "description", "price", "created_at"}
    assert expected_keys.issubset(result.keys()), f"Expected keys {expected_keys}, but got {result.keys()}"
    # Assert that the values for the keys are of the correct type
    assert isinstance(result["name"], str), "Expected 'name' to be a string"
    assert isinstance(result["category"], str), "Expected 'category' to be a string"
    assert isinstance(result["code"], str), "Expected 'code' to be a string"
    assert isinstance(result["description"], str), "Expected 'description' to be a string"
    assert isinstance(result["price"], float), "Expected 'price' to be a float"
    assert isinstance(result["created_at"], datetime), "Expected 'created_at' to be a datetime object"
import hashlib, pytest
from typing import Dict, Tuple
from utils import generate_unique_code

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
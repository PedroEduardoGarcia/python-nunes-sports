import hashlib, random
from datetime import datetime
from typing import Any, Dict

charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

def random_string() -> str:
    """Generate and return a random string based on the charset."""
    fn = random.randint(5, 9)
    ln = random.randint(3, 9)
    b = [random.choice(charset) for _ in range(fn + ln)]
    space_index = random.randint(0, len(b) - 1)
    b.insert(space_index, ' ')
    return ''.join(b)

def random_price(min_price: float=0.01, max_price: float=10000.00) -> float:
    """Generate and return a random price between min_price and max_price with two decimal places."""
    price = random.uniform(min_price, max_price)
    return round(price, 2)

def generate_unique_code(name: str, category: str) -> str:
    return hashlib.md5(f"{name}{category}".encode()).hexdigest()

def random_product() -> Dict[str, Any]:
    name = random_string()
    p = {
        "name": name,
        "category": "Test",
        "code": generate_unique_code(name, "Test"),
        "description": random_string() + random_string(),
        "price": random_price(),
        "created_at": datetime.now()
    }
    return p
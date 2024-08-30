import hashlib

def generate_unique_code(name: str, category: str) -> str:
    return hashlib.md5(f"{name}{category}".encode()).hexdigest()
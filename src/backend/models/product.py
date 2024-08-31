from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel

class Product(BaseModel):
    name: str
    code: str
    description: str
    category: str
    price: Decimal
    created_at: datetime

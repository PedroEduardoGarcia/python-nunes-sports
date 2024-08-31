from pydantic import BaseModel
from decimal import Decimal
from datetime import datetime

class Product(BaseModel):
    code: str
    description: str
    category: str
    price: Decimal
    created_at: datetime

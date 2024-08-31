from typing import Optional, List
from models import Product
import asyncpg

class ProductService:
    def __init__(self, pool: asyncpg.Pool):
        self.pool = pool

    async def create_product(self, product: Product) -> Optional[int]:
        """Insert a new product into the database and return the product's ID."""
        query = """
        INSERT INTO products (name, code, description, category, price, created_at)
        VALUES ($1, $2, $3, $4, $5, $6)
        RETURNING id;
        """
        async with self.pool.acquire() as conn:
            product_id = await conn.fetchval(
                query,
                product.name,
                product.code, 
                product.description, 
                product.category, 
                product.price, 
                product.created_at
            )
        return product_id

    async def get_product_by_id(self, product_id: int) -> Optional[Product]:
        """Retrieve a product by its ID."""
        query = """
        SELECT id, name, code, description, category, price, created_at
        FROM products
        WHERE id = $1;
        """
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(query, product_id)
        if row:
            return Product(**row)
        return None

    async def update_product(self, product_id: int, updated_product: Product) -> bool:
        """Update an existing product by its ID."""
        query = """
        UPDATE products
        SET name = $1, code = $2, description = $3, category = $4, price = $5, created_at = $6
        WHERE id = $7;
        """
        async with self.pool.acquire() as conn:
            result = await conn.execute(
                query,
                updated_product.name,
                updated_product.code,
                updated_product.description,
                updated_product.category,
                updated_product.price,
                updated_product.created_at,
                product_id
            )
        return result == 'UPDATE 1'

    async def delete_product(self, product_id: int) -> bool:
        """Delete a product by its ID."""
        query = """
        DELETE FROM products WHERE id = $1;
        """
        async with self.pool.acquire() as conn:
            result = await conn.execute(query, product_id)
        return result == 'DELETE 1'

    async def list_products(self) -> List[Product]:
        """Retrieve all products from the database."""
        query = """
        SELECT id, name, code, description, category, price, created_at
        FROM products;
        """
        async with self.pool.acquire() as conn:
            rows = await conn.fetch(query)
        return [Product(**row) for row in rows]

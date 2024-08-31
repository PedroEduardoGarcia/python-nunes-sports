import os, pytest
from models import Product
from repositories import PostgresRepository
from services import ProductService
from utils import random_product

@pytest.mark.asyncio
async def test_connection_repo() -> None:
    repo = PostgresRepository(
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
    )

    pool = await repo.connect()
    try:
        if pool:
            version = await repo.get_version()
            # Assert that the version is not None, indicating a successful query
            assert version is not None, "Failed to fetch PostgreSQL version"

            product_service = ProductService(pool)
            random_p = random_product()
            new_product = Product(
                name=random_p["name"],
                code=random_p["code"],
                description=random_p["description"], 
                category=random_p["category"], 
                price=random_p["price"],
                created_at=random_p["created_at"]
            )
            product_id = await product_service.create_product(new_product)
            # Assert that the product is not None, indicating a successful product creation
            assert product_id is not None, "Product id is None"
            print(f"Created product with ID: {product_id}")
        else:
            pytest.fail("No connection established")
    finally:
        await repo.close()
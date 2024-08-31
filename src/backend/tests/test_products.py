import os, pytest
from datetime import datetime
from repositories import PostgresRepository
from services import ProductService
from models import Product

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

            new_product = Product(
                code="P001", 
                description="Sample Product", 
                category="Category A", 
                price=19.99,
                created_at=datetime.now()
            )
            product_id = await product_service.create_product(new_product)
            # Assert that the product is not None, indicating a successful product creation
            assert product_id is not None, "Product id is None"
            print(f"Created product with ID: {product_id}")
        else:
            pytest.fail("No connection established")
    finally:
        await repo.close()
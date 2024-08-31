import os, pytest
from models import Product
from repositories import PostgresRepository
from services import ProductService
from utils import random_product

@pytest.mark.asyncio
async def test_create_product() -> None:
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
        else:
            pytest.fail("No connection established")
    finally:
        await repo.close()

@pytest.mark.asyncio
async def test_delete_product() -> None:
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
            product_service2 = ProductService(pool)
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
            # Assert that the product ID is not None, indicating a successful product creation
            assert product_id is not None, "Product id is None"
            deleted = await product_service2.delete_product(product_id)
            # Assert that the deletion operation was successful
            assert deleted is True, "Failed to delete product"
            deleted_product = await product_service2.get_product_by_id(product_id)
            # Assert that the product does not exist after deletion
            assert deleted_product is None, "Product should be None after deletion"
        else:
            pytest.fail("No connection established")
    finally:
        await repo.close()

@pytest.mark.asyncio
async def test_get_product_by_id() -> None:
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
            product_service2 = ProductService(pool)
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
            # Assert that the product ID is not None, indicating a successful product creation
            assert product_id is not None, "Product id is None"
            
            retrieved_product = await product_service2.get_product_by_id(product_id)
            
            # Assert that the retrieved product matches the newly created product
            assert retrieved_product is not None, "Product should not be None when retrieved by ID"
            assert retrieved_product.code == new_product.code, f"Expected product code {new_product.code}, but got {retrieved_product.code}"
            assert retrieved_product.name == new_product.name, f"Expected product name {new_product.name}, but got {retrieved_product.name}"
            assert retrieved_product.description == new_product.description, f"Expected product description {new_product.description}, but got {retrieved_product.description}"
            assert retrieved_product.category == new_product.category, f"Expected product category {new_product.category}, but got {retrieved_product.category}"
            assert retrieved_product.price == new_product.price, f"Expected product price {new_product.price}, but got {retrieved_product.price}"
            # assert retrieved_product.created_at == new_product.created_at, f"Expected product creation date {new_product.created_at}, but got {retrieved_product.created_at}"
            
        else:
            pytest.fail("No connection established")
    finally:
        await repo.close()

@pytest.mark.asyncio
async def test_update_product() -> None:
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
            product_service2 = ProductService(pool)
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
            # Assert that the product ID is not None, indicating a successful product creation
            assert product_id is not None, "Product id is None"
            random_p = random_product()
            updated_product = Product(
                name=random_p["name"],
                code=new_product.code,
                description=random_p["description"], 
                category=random_p["category"], 
                price=random_p["price"],
                created_at=random_p["created_at"]
            )
            update_success = await product_service.update_product(product_id, updated_product)
            # Assert that the update was successful
            assert update_success, "Product update failed"

            updated_product_from_db = await product_service2.get_product_by_id(product_id)
            # Assert that the retrieved product matches the updated details
            assert updated_product_from_db is not None, "Product should be retrieved from database"
            assert updated_product_from_db.name == updated_product.name, "Product name was not updated correctly"
            assert updated_product_from_db.description == updated_product.description, "Product description was not updated correctly"
            assert updated_product_from_db.category == updated_product.category, "Product category was not updated correctly"
            assert updated_product_from_db.price == updated_product.price, "Product price was not updated correctly"
            
        else:
            pytest.fail("No connection established")
    finally:
        await repo.close()

@pytest.mark.asyncio
async def test_list_products() -> None:
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

            num_products = 3
            added_product_ids = []
            for _ in range(num_products):
                product_data = random_product()
                new_product = Product(
                    name=product_data["name"],
                    code=product_data["code"],
                    description=product_data["description"],
                    category=product_data["category"],
                    price=product_data["price"],
                    created_at=product_data["created_at"]
                )
                product_id = await product_service.create_product(new_product)
                added_product_ids.append(product_id)
                # Assert that the product ID is not None, indicating successful creation
                assert product_id is not None, "Product ID is None"

            products = await product_service.list_products()
            # Assert that the list is not empty
            assert products, "Product list should not be empty"


            # Additional asserts: Ensure that the products' details are correct
            for product in products:
                assert product.name is not None, f"Product name should not be None for product ID {product.id}"
                assert product.code is not None, f"Product code should not be None for product ID {product.id}"
                assert product.description is not None, f"Product description should not be None for product ID {product.id}"
                assert product.category is not None, f"Product category should not be None for product ID {product.id}"
                assert product.price is not None, f"Product price should not be None for product ID {product.id}"
                assert product.created_at is not None, f"Product created_at should not be None for product ID {product.id}"
        else:
            pytest.fail("No connection established")
    finally:
        await repo.close()
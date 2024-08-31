import asyncpg, os, pytest, socket
from typing import Optional
from repositories import PostgresRepository

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
            async with pool.acquire() as conn:
                version = await conn.fetchval('SELECT version()')
                # Assert that the version is not None, indicating a successful query
                assert version is not None, "Failed to fetch PostgreSQL version"
        else:
            pytest.fail("No pool established")
    finally:
        await repo.close()


@pytest.mark.asyncio
async def test_connection_failure_repo() -> None:
    repo = PostgresRepository(
        user="invalid_user",
        password="invalid_password",
        database="invalid_db",
        host="invalid_db",
        port="9999",
    )

    try:
        pool = await repo.connect()
        if pool:
            pytest.fail("Expected connection pool creation to fail, but it succeeded")
    except Exception as e:
        if isinstance(e, asyncpg.PostgresError):
            assert True, "Caught a PostgresError as expected"
        elif isinstance(e, socket.gaierror):
            assert True, "Caught a socket.gaierror as expected"
        else:
            pytest.fail(f"Unexpected exception type: {type(e).__name__}")
    finally:
        await repo.close()

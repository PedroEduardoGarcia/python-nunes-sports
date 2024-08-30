import asyncpg, os, pytest, socket
from typing import Optional
from repositories import PostgresRepository

@pytest.mark.asyncio
async def test_connection() -> None:
    conn: Optional[asyncpg.Connection] = None
    try:
        conn = await asyncpg.connect(
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
        )
        version = await conn.fetchval('SELECT version()')
        # Assert that the version is not None, indicating a successful query 
        assert version is not None, "Failed to fetch PostgreSQL version"
        
    except Exception as e:
        pytest.fail(f"Database connection failed: {e}")
    
    finally:
        if conn:
            await conn.close()

@pytest.mark.asyncio
async def test_connection_repo() -> None:
    repo = PostgresRepository(
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
    )

    conn = await repo.connect()
    try:
        if conn:
            version = await repo.get_version()
            # Assert that the version is not None, indicating a successful query
            assert version is not None, "Failed to fetch PostgreSQL version"
        else:
            pytest.fail("No connection established")
    finally:
        await repo.close()

@pytest.mark.asyncio
async def test_connection_failure() -> None:
    os.environ["DB_USER"] = "invalid_user"
    os.environ["DB_PASSWORD"] = "invalid_password"
    os.environ["DB_NAME"] = "invalid_db"
    os.environ["DB_HOST"] = "invalid_host"
    os.environ["DB_PORT"] = "9999"
    
    conn: Optional[asyncpg.Connection] = None
    try:
        conn = await asyncpg.connect(
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
        )
        pytest.fail("Expected connection to fail, but it succeeded")
        
    except (asyncpg.PostgresError, socket.gaierror) as e:
        # Asserts that the exception is either a PostgresError or a gaierror
        if isinstance(e, asyncpg.PostgresError):
            assert True, "Caught a PostgresError as expected"
        elif isinstance(e, socket.gaierror):
            assert True, "Caught a socket.gaierror as expected"
        else:
            pytest.fail(f"Unexpected exception type: {type(e).__name__}")
        
    finally:
        if conn:
            await conn.close()

@pytest.mark.asyncio
async def test_connection_failure_repo() -> None:
    # Temporarily set incorrect environment variables for a failed connection
    os.environ["DB_USER"] = "invalid_user"
    os.environ["DB_PASSWORD"] = "invalid_password"
    os.environ["DB_NAME"] = "invalid_db"
    os.environ["DB_HOST"] = "invalid_host"
    os.environ["DB_PORT"] = "9999"

    repo = PostgresRepository(
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
    )

    try:
        conn = await repo.connect()
        if conn:
            pytest.fail("Expected connection to fail, but it succeeded")
    except Exception as e:
        if isinstance(e, asyncpg.PostgresError):
            assert True, "Caught a PostgresError as expected"
        elif isinstance(e, socket.gaierror):
            assert True, "Caught a socket.gaierror as expected"
        else:
            pytest.fail(f"Unexpected exception type: {type(e).__name__}")
    finally:
        await repo.close()

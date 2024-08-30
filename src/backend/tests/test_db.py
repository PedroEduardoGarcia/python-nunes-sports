import pytest
import asyncpg
import os

@pytest.mark.asyncio
async def test_connection():
    try:
        conn = await asyncpg.connect(
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
        )

        version = await conn.fetchval('SELECT version()')        
        assert version is not None, "Failed to fetch PostgreSQL version"
        
    except Exception as e:
        pytest.fail(f"Database connection failed: {e}")
    
    finally:
        if conn:
            await conn.close()

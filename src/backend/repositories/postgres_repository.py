import asyncpg
from typing import Optional
from .base_repository import BaseRepository

class PostgresRepository(BaseRepository):
    def __init__(self, user: str, password: str, database: str, host: str, port: str):
        self.user = user
        self.password = password
        self.database = database
        self.host = host
        self.port = port
        self.pool: Optional[asyncpg.Pool] = None

    async def connect(self) -> Optional[asyncpg.Pool]:
        """Establish a connection pool."""
        try:
            self.pool = await asyncpg.create_pool(
                user=self.user,
                password=self.password,
                database=self.database,
                host=self.host,
                port=self.port,
                min_size=1,
                max_size=10
            )
        except Exception as e:
            print(f"Failed to create a connection pool: {e}")
        return self.pool

    async def get_version(self) -> Optional[str]:
        """Retrieve the PostgreSQL version using a connection from the pool."""
        if self.pool:
            async with self.pool.acquire() as conn:
                return await conn.fetchval('SELECT version()')
        return None

    async def close(self) -> None:
        """Close the connection pool."""
        if self.pool:
            await self.pool.close()
            self.pool = None

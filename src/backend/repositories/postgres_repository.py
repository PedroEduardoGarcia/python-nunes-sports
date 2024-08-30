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
        self.conn: Optional[asyncpg.Connection] = None

    async def connect(self) -> Optional[asyncpg.Connection]:
        """Establish and return a database connection."""
        try:
            self.conn = await asyncpg.connect(
                user=self.user,
                password=self.password,
                database=self.database,
                host=self.host,
                port=self.port,
            )
        except Exception as e:
            print(f"Failed to connect to the database: {e}")
        return self.conn

    async def get_version(self) -> Optional[str]:
        """Retrieve the PostgreSQL version."""
        if self.conn:
            return await self.conn.fetchval('SELECT version()')
        return None

    async def close(self) -> None:
        """Close the database connection."""
        if self.conn:
            await self.conn.close()
            self.conn = None

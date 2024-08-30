from abc import ABC, abstractmethod
from typing import Optional

class BaseRepository(ABC):
    @abstractmethod
    async def connect(self) -> Optional[object]:
        """Establish and return a database connection."""
        pass

    @abstractmethod
    async def get_version(self) -> Optional[str]:
        """Retrieve the PostgreSQL version."""
        pass

    @abstractmethod
    async def close(self) -> None:
        """Close the database connection."""
        pass

from typing import Any, AsyncGenerator
from ..db.session import async_session_local


# DB Dependency
async def get_session() -> AsyncGenerator[Any, Any]:
    async with async_session_local() as session:
        # async with session.begin():
        yield session

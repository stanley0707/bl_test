import asyncio

from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from settings import ProjectSettings


async def get_async_engine():
    """
    Returned async engine
    """
    return create_async_engine(ProjectSettings.data_base_url, echo=True)


async def get_async_session(engine=None) -> AsyncSession:
    """
    Returned instance of asynchronous db session
    """
    engine = engine or await get_async_engine()
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    return async_session()


def coroutine_depends_on(coroutine, *args, **kwargs):
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(coroutine())

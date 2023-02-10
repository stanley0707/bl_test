import pytest
import asyncio
from sqlalchemy import event

from fastapi import status
from httpx import AsyncClient
from api import app
from tests.factory import Factory
from db import BaseModel, Account, get_async_engine, get_async_session
from settings import ProjectSettings

GLOBAL_FACTORY = Factory()

ACCOUNTS = GLOBAL_FACTORY.cycle(3).get_fake_account()


def pytest_configure():
    pytest.ACCOUNTS = GLOBAL_FACTORY.cycle(3).get_fake_account()


@pytest.fixture(scope="session")
def event_loop():
    """
    Creates an instance of the default event loop for the test session.
    """
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="package", autouse=True)
async def init_db():
    engine = await get_async_engine()
    await BaseModel.metadata.create_all(engine)
    session = await get_async_session(engine=engine)
    session.begin_nested()
    app.tests.config.session = session

    @event.listens_for(app.tests.config.session, "after_transaction_end")
    def restart(session, transaction):
        if transaction.nested and not transaction._parent.nested:
            session.begin_nested()

    yield session

    session.close()
    trans.rollback()
    connection.close()


@pytest.fixture(scope="session")
def factory():
    return Factory()


@pytest.fixture(scope="session", autouse=True)
def account_1():
    return ACCOUNTS[0]


@pytest.fixture(scope="session", autouse=True)
def account_2():
    return ACCOUNTS[1]


@pytest.fixture
def account_3():
    return ACCOUNTS[2]


@pytest.fixture
def async_session():
    return AsyncClient(app=app, base_url=ProjectSettings.base_api_url)


@pytest.fixture
def new_async_session():
    def _new_async_session():
        return AsyncClient(app=app, base_url=ProjectSettings.base_api_url)

    return _new_async_session


@pytest.fixture
async def test_register_user_3(account_3, new_async_session):
    session = new_async_session()
    response = await session.post(
        "/accounts/register/",
        json={
            "email": account_3["username"],
            "password": account_3["password"],
            "password_confirm": account_3["password"],
            "role": "user",
        },
    )
    assert response.status_code == status.HTTP_201_CREATED
    return session


@pytest.fixture
@pytest.mark.asyncio
async def async_session_account_1(account_1, async_session):
    response = await async_session.post(
        "/accounts/login/",
        data={
            "username": account_1["username"],
            "password": account_1["password"],
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )

    assert response.status_code == status.HTTP_201_CREATED
    async_session.headers["Authorization"] = f"Bearer {response.json()['access']}"
    return async_session


@pytest.fixture
@pytest.mark.asyncio
async def async_session_account_3(account_3, test_register_user_3):
    async_session = await test_register_user_3
    response = await async_session.post(
        "/accounts/login/",
        data={
            "username": account_3["username"],
            "password": account_3["password"],
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )

    assert response.status_code == status.HTTP_201_CREATED
    async_session.headers["Authorization"] = f"Bearer {response.json()['access']}"
    return async_session


@pytest.fixture
@pytest.mark.asyncio
async def accounts_sessions(new_async_session):
    sessions = []
    for account in pytest.ACCOUNTS:
        session = new_async_session()
        response = await session.post(
            "/accounts/login/",
            data={
                "username": account["username"],
                "password": account["password"],
            },
        )
        session.headers["Authorization"] = f"Bearer {response.json()['access']}"
        assert response.status_code == status.HTTP_201_CREATED
        sessions.append(session)
    return sessions


@pytest.fixture
@pytest.mark.asyncio
async def all_accounts():
    return await Account.manager.all()

import pytest

from fastapi import status


@pytest.mark.asyncio
async def test_cant_login_if_user_does_not_exist(async_session):
    async with async_session as session:
        response = await session.post(
            "/accounts/login/",
            data={
                "username": "fake@notexist.com",
                "password": "fake_password",
            },
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.asyncio
async def test_register_user(account_1, async_session):
    async with async_session as session:
        response = await session.post(
            "/accounts/register/",
            json={
                "email": account_1["username"],
                "password": account_1["password"],
                "password_confirm": account_1["password"],
                "role": "user",
            },
        )
        assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.asyncio
async def test_can_login(account_1, async_session):
    async with async_session as session:
        response = await session.post(
            "/accounts/login/",
            data={
                "username": account_1["username"],
                "password": account_1["password"],
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.asyncio
async def test_cant_read_accounts_if_anonymous(async_session):
    async with async_session as session:
        response = await session.get("/accounts/")
        assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.asyncio
async def test_404_not_found_if_account_not_exist(async_session_account_1):
    session = await async_session_account_1
    response = await session.get("/accounts/12345/")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    del session


@pytest.mark.asyncio
async def test_404_not_found_if_event_not_exist(async_session_account_1):
    session = await async_session_account_1
    response = await session.get("/events/12345/")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    del session


@pytest.mark.asyncio
async def test_can_read_self_account(async_session_account_1):
    session = await async_session_account_1
    response = await session.get("/accounts/self/")
    assert response.status_code == status.HTTP_200_OK
    del session

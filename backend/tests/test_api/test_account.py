import pytest

from fastapi import status


@pytest.mark.asyncio
@pytest.mark.parametrize("account", pytest.ACCOUNTS)
async def test_can_create_account_1(account, async_session):
    async with async_session as session:
        response = await session.post(
            "/accounts/register/",
            json={
                "email": account["username"],
                "password": account["password"],
                "password_confirm": account["password"],
                "role": account["role"],
            },
        )
        assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.parametrize("idx,account", enumerate(pytest.ACCOUNTS))
@pytest.mark.asyncio(scope="session")
async def test_account_is_valid_data(idx, account, accounts_sessions):
    accounts_sessions = await accounts_sessions
    session = accounts_sessions[idx]
    response = await session.get("/accounts/self/")
    assert response.status_code == status.HTTP_200_OK
    del session
    account_data = response.json()

    assert account_data["email"] == account["username"]
    assert account_data["role"] == account["role"]

from typing import List

from fastapi.security import OAuth2PasswordRequestForm
from fastapi import status, Path, Depends, APIRouter, Body
from db.models import Account

from .serializers import (
    InviteSerializer,
    EventAccountInviteSerializer,
    CreateAccountSerializer,
    AccountWithEventSerializer,
    AccountSerializer,
)

account_router = APIRouter(prefix="/accounts", tags=["accounts"])


@account_router.post("/login/", status_code=status.HTTP_201_CREATED)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    return {"access": await Account.manager.create_access_token(form_data)}


@account_router.post("/register/", status_code=status.HTTP_201_CREATED)
async def create_user(data: CreateAccountSerializer = Body()):
    await Account.manager.create(data)


@account_router.get(
    "/",
    response_model=List[AccountSerializer],
    dependencies=[Depends(Account.manager.is_authorize)],
)
async def all_accounts():
    """
    Returns all accounts
    :return:
    """
    return await Account.manager.select_with_aggregated_relations()


@account_router.get("/self/", dependencies=[Depends(Account.manager.is_authorize)])
async def self(
    account: AccountSerializer = Depends(Account.manager.get_current_session_account),
):
    """
    Returns self account
    :param account:
    :return:
    """
    return account


@account_router.get(
    "/self/invites/in/",
    dependencies=[Depends(Account.manager.is_authorize)],
    response_model=List[EventAccountInviteSerializer],
)
async def self_ingoing_invites(
    account: AccountSerializer = Depends(Account.manager.get_current_session_account),
):
    """
    Returns self invites to events
    :param account:
    :return:
    """
    return await account.get_ingoing_invites()


@account_router.get(
    "/{account_id}/",
    dependencies=[Depends(Account.manager.is_authorize)],
    response_model=AccountWithEventSerializer,
)
async def account_detail(account_id: int = Path(..., description="Account id")):
    """
    :param account_id:
    :return: detail account by id
    """
    return await Account.manager.get_no_lazy(id=account_id)


@account_router.get(
    "/self/invites/out/",
    dependencies=[Depends(Account.manager.is_authorize)],
    response_model=List[InviteSerializer],
)
async def self_outgoing_invites(
    account: AccountSerializer = Depends(Account.manager.get_current_session_account),
):
    """
    Returns self invites to events
    :param account:
    :return:
    """
    return await account.get_outgoing_invites()

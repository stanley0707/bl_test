from typing import List

from fastapi import Path, Depends, APIRouter
from db.models import Event, Account

from .serializers import EventSerializer, AccountSerializer

event_router = APIRouter(prefix="/events", tags=["events"])


@event_router.get(
    "/events",
    dependencies=[Depends(Account.manager.is_authorize)],
    response_model=List[EventSerializer],
)
async def all_events():
    """
    Returns all event list
    :return:
    """
    return await Event.manager.select_with_aggregated_relations()


@event_router.get(
    "/{event_id}",
    dependencies=[Depends(Account.manager.is_authorize)],
    response_model=EventSerializer,
)
async def event_detail(event_id: int = Path(..., description="Event id")):
    """
    :param event_id:
    :return: detail event by event id
    """
    return await Event.manager.get_no_lazy(id=event_id)


@event_router.post(
    "/{event_id}/reg",
    dependencies=[Depends(Account.manager.is_authorize)],
)
async def register_on_event(
    event_id: int = Path(..., description="Event id"),
    account: AccountSerializer = Depends(Account.manager.get_current_session_account),
):
    """
    Register self account on event
    :param event_id:
    :param account curret session account:
    :return:
    """
    return await Event.manager.register(account=account, event_id=event_id)


@event_router.post("/")
async def create_event(data: dict, account: EventSerializer):
    """
    Created event
    :param data:
    :param account:
    :return:
    """
    return Event.manager.create(account=account, **data)

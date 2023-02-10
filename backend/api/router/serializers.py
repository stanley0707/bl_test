import json

from typing import Union, Optional, List
from datetime import datetime

from utils.event_date_scheduler import EventTimeFrame
from pydantic import validator, constr, EmailStr, BaseModel


class CreateAccountSerializer(BaseModel):
    email: EmailStr
    password: constr(min_length=8)
    password_confirm: str
    role: str


class AccountSerializer(BaseModel):
    id: Optional[int]
    first_name: Optional[str]
    last_name: Optional[str]
    time_created: Optional[datetime]
    time_updated: Optional[datetime]
    email: Optional[EmailStr]
    events_count: Optional[int]
    author_events_count: Optional[int]

    class Config:
        orm_mode = True


class BaseEventSerializer(BaseModel):
    id: str
    author_id: str
    title: str
    description: str
    time_created: datetime
    time_updated: Optional[datetime]

    class Config:
        orm_mode = True


class EventSerializer(BaseEventSerializer):
    has_confirmed_invites: bool
    accounts_count: int


class EventRelationSerializer(EventSerializer):
    author: AccountSerializer
    accounts: List[AccountSerializer]


class EventAccountInviteSerializer(BaseModel):
    id: str
    guest_id: str
    event_id: str
    is_confirmed: str
    time_created: datetime
    time_updated: Optional[datetime]

    class Config:
        orm_mode = True


class InviteSerializer(BaseModel):
    id: str
    inviter_id: str
    invite_id: str
    is_confirmed: str
    time_created: datetime
    time_updated: Optional[datetime]

    class Config:
        orm_mode = True


class AccountWithEventSerializer(AccountSerializer):
    events: Optional[List[BaseEventSerializer]]
    author_events: Optional[List[BaseEventSerializer]]
    ingoing_invites: Optional[List[EventAccountInviteSerializer]]
    outgoing_invites: Optional[List[InviteSerializer]]
    work_timing: Union[str, bytes, EventTimeFrame]

    @validator("work_timing")
    def check_storage_type(cls, value):
        if isinstance(value, str):
            return json.loads(value)
        return value


class EventWithInvitesSerializer(EventSerializer):
    invitations: List[AccountSerializer]

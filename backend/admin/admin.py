from sqladmin import ModelView
from db.models import Invite, EventAccountInvite, Event, Account


class AccountAdmin(ModelView, model=Account):
    column_list = [Account.id, Account.first_name, Account.last_name]


class EventAdmin(ModelView, model=Event):
    column_list = [Event.id, Event.title]


class EventInviteAdmin(ModelView, model=EventAccountInvite):
    column_list = [
        EventAccountInvite.id,
        EventAccountInvite.guest,
        EventAccountInvite.is_confirmed,
    ]


class InviteAdmin(ModelView, model=Invite):
    column_list = [Invite.id, Invite.inviter, Invite.is_confirmed]

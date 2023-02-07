from enum import Enum

from sqlalchemy import String, Integer, Column

from .mixins import AccountMixin
from ..mixins import TimeCreateUpdateMixin, ScheduleAccountMixin
from ..base import BaseModel


class Account(AccountMixin, TimeCreateUpdateMixin, ScheduleAccountMixin, BaseModel):
    """
    Account model table extended on TimeCreateUpdateMixin
    created and updated fields.
    Relationships:
        events: all events in which the user participates like guest,
        author_events: all events in which the user participates like author,
        outgoing_invites: all outgoing event invocations to the user,

    """

    class AccountRole(str, Enum):
        user = "user"
        admin = "admin"

    __tablename__ = "Account"

    id = Column("id", Integer, primary_key=True)
    first_name = Column("first_name", String)
    last_name = Column("last_name", String)
    email = Column("email", String, unique=True)
    password = Column("password", String, nullable=False)
    role = Column("role", String, server_default=AccountRole.admin, nullable=False)

    def __str__(self):
        return f"<Account: {self.id}, {self.first_name} {self.last_name}>"

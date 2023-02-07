from sqlalchemy.sql import func
from sqlalchemy.orm import relationship, backref
from sqlalchemy import String, Integer, ForeignKey, DateTime, Column, Boolean
from managers import EventManager

from .mixins import EventMixin
from ..mixins import TimeCreateUpdateMixin
from ..base import BaseModel


class Invite(TimeCreateUpdateMixin, BaseModel):
    __tablename__ = "Invite"

    id = Column("id", Integer, primary_key=True)
    inviter_id = Column(
        "inviter_id",
        Integer,
        ForeignKey("Account.id", ondelete="SET NULL"),
        nullable=False,
    )
    inviter = relationship("Account", backref=backref("outgoing_invites"))
    invite_id = Column(
        "invite_id",
        Integer,
        ForeignKey("EventAccountInvite.id", ondelete="CASCADE"),
        nullable=False,
    )
    invitation = relationship(
        "EventAccountInvite", backref=backref("invite", uselist=False)
    )
    is_confirmed = Column("is_confirmed", Boolean, default=False)

    def __str__(self):
        return f"<Invite: from {self.inviter}, on {self.invite_id}>"


class EventAccountInvite(TimeCreateUpdateMixin, BaseModel):
    """
    EventInvite model: All users can send invite to any user,
    every one invite belong to only one event and hase a one
    author.
    """

    __tablename__ = "EventAccountInvite"

    id = Column("id", Integer, primary_key=True)
    event_id = Column(
        "event_id", Integer, ForeignKey("Event.id", ondelete="CASCADE"), nullable=False
    )
    event = relationship("Event", backref="invites", viewonly=True)
    guest_id = Column(
        "guest_id",
        Integer,
        ForeignKey("Account.id", ondelete="SET NULL"),
        nullable=False,
    )
    guest = relationship("Account", backref=backref("ingoing_invites"), viewonly=True)
    is_confirmed = Column("is_confirmed", Boolean, default=False)

    def __str__(self):
        return f"<EventAccountInvite: {self.id}, to {self.guest} on {self.event}>"


class Event(EventMixin, TimeCreateUpdateMixin, BaseModel):
    """
    Event model table extended on TimeCreateUpdateMixins
    created and updated fields
    """

    __tablename__ = "Event"

    id = Column("id", Integer, primary_key=True)
    accounts = relationship("Account", secondary="EventAccountInvite", backref="events")
    author_id = Column(
        "author_id",
        Integer,
        ForeignKey("Account.id", ondelete="SET NULL"),
        nullable=False,
    )
    author = relationship("Account", backref=backref("author_events"))
    title = Column("title", String, nullable=False)
    description = Column("description", String)
    meeting_url = Column("meeting_url", String, nullable=True)
    time_start = Column(
        "time_start", DateTime(timezone=True), server_default=func.now()
    )
    time_end = Column("time_end", DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<Event: {self.id}, {self.title} start: {self.time_start} end:{self.time_end}>"

    manager = EventManager()

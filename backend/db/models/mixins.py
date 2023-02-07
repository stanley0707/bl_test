from typing import Callable

from sqlalchemy.sql import select, func, and_
from managers import EventManager, AccountManager, BaseManager


class BaseMixin:
    id: int
    manager: Callable

    @classmethod
    async def get_manage_instance(cls) -> BaseManager:
        return cls.manager

    @staticmethod
    async def get_relations_join_by_model(model, manage_instance, having):
        """
        :return: all EventAccountInvite models where account
        actual instance model is guest
        """
        return await manage_instance.execute(
            select(model).join(manage_instance.model).filter(having).group_by(model.id),
        )


class AccountMixin(BaseMixin):
    role: str

    @property
    def is_admin(self):
        return self.role == self.AccountRole.admin

    @property
    def is_user(self):
        return self.role == self.AccountRole.user

    async def get_ingoing_invites(self):
        """
        :return: all EventAccountInvite models where account
        actual instance model is guest
        """
        manage_instance = await self.get_manage_instance()
        model_instance = manage_instance.relation_dict["EventAccountInvite"]
        return await self.get_relations_join_by_model(
            model=model_instance,
            manage_instance=manage_instance,
            having=model_instance.guest_id == self.id,
        )

    async def get_outgoing_invites(self):
        """
        :return: all Invite models where account actual
        instance model is guest
        """
        manage_instance = await self.get_manage_instance()
        model_instance = manage_instance.relation_dict["Invite"]
        return await self.get_relations_join_by_model(
            model=model_instance,
            manage_instance=manage_instance,
            having=model_instance.inviter_id == self.id,
        )

    @classmethod
    def events_count_subquery(cls, label: str) -> select:
        """
        :return: event count most usage in subquery
        """
        Event = cls.manager.relation_dict["Event"]
        EventAccountInvite = cls.manager.relation_dict["EventAccountInvite"]
        return (
            select(EventAccountInvite.guest_id, func.count(Event.id).label(label))
            .group_by(EventAccountInvite.guest_id)
            .subquery()
        )

    @classmethod
    def author_events_count_subquery(cls, label: str) -> select:
        """
        :return: event count most usage in subquery
        """
        Event = cls.manager.relation_dict["Event"]
        return (
            select(Event.author_id, func.count(Event.id).label(label))
            .group_by(Event.author_id)
            .subquery()
        )

    manager = AccountManager()


class EventMixin(BaseMixin):
    @classmethod
    def accounts_count_subquery(cls, label: str) -> select:
        """
        :return: accounts count most usage in subquery
        """
        Account = cls.manager.relation_dict["Account"]
        EventAccountInvite = cls.manager.relation_dict["EventAccountInvite"]

        return (
            select(
                EventAccountInvite.event_id,
                func.count(Account.id).label(label),
            )
            .group_by(Account.id, EventAccountInvite.event_id)
            .subquery()
        )

    @classmethod
    def is_confirmed_invites_count_subquery(cls, label: str) -> select:
        """
        :return: accounts count most usage in subquery
        """
        Account = cls.manager.relation_dict["Account"]
        EventAccountInvite = cls.manager.relation_dict["EventAccountInvite"]

        return (
            select(
                EventAccountInvite.event_id,
                func.count(EventAccountInvite.id).label(label),
            )
            .where(
                and_(
                    EventAccountInvite.is_confirmed.is_(True),
                    EventAccountInvite.guest_id == Account.id,
                    EventAccountInvite.event_id == cls.id,
                )
            )
            .group_by(EventAccountInvite.event_id)
            .subquery()
        )

    manager = EventManager()

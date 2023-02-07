from typing import Optional, List, Dict, Callable

from sqlalchemy.sql import select, case
from sqlalchemy.orm import joinedload
from pydantic import EmailStr, BaseModel
from fastapi import status, HTTPException

from .model_manager import ModelManager
from .auth_jwt_mixins import AuthJWTMixin


class AccountManager(AuthJWTMixin, ModelManager):
    @property
    def labeled_field_dict(self) -> Dict:
        return dict(
            (i.name, i)
            for i in [
                self.model.id.label("id"),
                self.model.first_name.label("first_name"),
                self.model.last_name.label("last_name"),
                self.model.email.label("email"),
                self.model.role.label("role"),
                self.model.time_created.label("time_created"),
            ]
        )

    async def get_no_lazy(self, **kwargs) -> Optional[Callable]:
        """
        Set all relation models to one query in GET Detail
        :param kwargs:
        :return:
        """
        return await self.get(
            select(self.model)
            .options(
                joinedload(self.model.events),
                joinedload(self.model.author_events),
                joinedload(self.model.outgoing_invites),
                joinedload(self.model.ingoing_invites),
            )
            .where(self.relation_dict["EventAccountInvite"].is_confirmed.is_(False))
            .filter_by(**kwargs)
            .group_by(self.model.id),
            raise_on=True,
        )

    async def select_with_aggregated_relations(
        self,
        event_count_label: str = "events_count",
        author_event_count_label: str = "author_events_count",
    ) -> List[Dict]:
        """
        :param author_event_count_label:
        :param event_count_label - account event count lable name
        :return: All account  with event_count_label
        """
        fields = self.labeled_field_dict
        event_counter = self.model.events_count_subquery(event_count_label)
        author_event_counter = self.model.author_events_count_subquery(
            author_event_count_label
        )

        fields[event_count_label] = case(
            (event_counter.c.events_count.is_(None), 0),
            else_=event_counter.c.events_count,
        )
        fields[author_event_count_label] = case(
            (author_event_counter.c.author_events_count.is_(None), 0),
            else_=author_event_counter.c.author_events_count,
        )
        return [
            dict(zip(fields.keys(), row))
            for row in await self.execute(
                select(*fields.values())
                .outerjoin(event_counter, event_counter.c.guest_id == self.model.id)
                .outerjoin(
                    author_event_counter,
                    author_event_counter.c.author_id == self.model.id,
                )
                .group_by(
                    self.model.id,
                    event_counter.c.events_count,
                    author_event_counter.c.author_events_count,
                ),
                iterable=True,
            )
        ]

    async def create(self, data: BaseModel, *args, **kwargs):
        """
        Validate and create account with required parameters
        email and password
        :param data:
        :return:
        """
        if data.password != data.password_confirm:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Passwords do not match"
            )
        del data.password_confirm
        data.email = EmailStr(data.email.lower())
        data.password = self.hash_password(data.password)
        return await super().create(data=data.dict(), *args, **kwargs)

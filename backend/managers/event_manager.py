from typing import List, Dict

from sqlalchemy.sql import select, insert, func, case
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import status, HTTPException
from db.utils import get_async_session, coroutine_depends_on

from .model_manager import ModelManager


class EventManager(ModelManager):
    @property
    def labeled_field_dict(self) -> Dict:
        """
        :return:
        """
        return dict(
            (i.name, i)
            for i in [
                self.model.id.label("id"),
                self.model.title.label("title"),
                self.model.description.label("description"),
                self.model.meeting_url.label("meeting_url"),
                self.model.time_start.label("time_start"),
                self.model.time_end.label("time_end"),
                self.model.time_created.label("time_created"),
                self.model.time_updated.label("time_updated"),
                self.model.author_id.label("author_id"),
            ]
        )

    async def get_no_lazy(self, **kwargs):
        """
        Set all relation models to one query in GET Detail
        :param kwargs:
        :return:
        """
        return await self.get(
            select(self.model)
            .options(
                joinedload(self.model.accounts),
                joinedload(self.model.invites),
            )
            .filter_by(**kwargs)
            .group_by(self.model.id),
            raise_on=True,
        )

    async def select_with_aggregated_relations(
        self,
        accounts_count_label: str = "accounts_count",
        has_confirmed_invites_label: str = "has_confirmed_invites",
    ) -> List[Dict]:
        """
        :param accounts_count_label:
        :param has_confirmed_invites_label:
        :return: All account  with event_count_label
        """
        fields = self.labeled_field_dict
        accounts_counter = self.model.accounts_count_subquery(accounts_count_label)
        is_confirmed_invites_counter = self.model.is_confirmed_invites_count_subquery(
            has_confirmed_invites_label
        )

        fields[accounts_count_label] = case(
            (accounts_counter.c.accounts_count.is_(None), 0),
            else_=accounts_counter.c.accounts_count,
        )

        fields[has_confirmed_invites_label] = (
            func.sum(
                case(
                    (is_confirmed_invites_counter.c.has_confirmed_invites.is_(None), 0),
                    else_=is_confirmed_invites_counter.c.has_confirmed_invites,
                )
            )
            > 0
        )

        return [
            dict(zip(fields.keys(), row))
            for row in await self.execute(
                select(
                    *fields.values(),
                )
                .outerjoin(
                    accounts_counter, accounts_counter.c.event_id == self.model.id
                )
                .outerjoin(
                    is_confirmed_invites_counter,
                    is_confirmed_invites_counter.c.event_id == self.model.id,
                )
                .group_by(
                    self.model.id,
                    is_confirmed_invites_counter.c.has_confirmed_invites,
                    accounts_counter.c.accounts_count,
                ),
                iterable=True,
            )
        ]

    async def register(
        self,
        account,
        event_id,
        session: AsyncSession = coroutine_depends_on(get_async_session),
    ) -> bool:
        """
        :param account:
        :param event_id:
        :param session:
        :return:
        """
        EventAccountInvite = self.relation_dict["EventAccountInvite"]
        if event := await self.get(id=event_id):
            async with session.begin():
                try:
                    await session.execute(
                        insert(EventAccountInvite).values(
                            {
                                "guest_id": account.id,
                                "event_id": event.id,
                                "is_confirmed": True,
                            }
                        )
                    )
                except Exception as exc:
                    msg = f"Account Event register error: {str(exc)}"
                    self.logger.error(msg)
                    await session.rollback()
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST, detail=msg
                    )
                else:
                    await session.commit()
                    return True
        return False

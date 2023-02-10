from typing import Union, Tuple, Optional, List, Iterator, Dict, Callable

from sqlalchemy.sql import update, select, insert, delete
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import status, HTTPException
from db.utils import get_async_session, coroutine_depends_on
from db.base import BaseModel

from .base_manager import BaseManager


class ModelManager(BaseManager):
    @property
    def labeled_field_dict(self):
        return dict(
            (i.name, i)
            for i in [
                self.model.id.label("id"),
            ]
        )

    @property
    def relation_dict(self):
        return {
            model.__tablename__: model
            for model in BaseModel.registry._class_registry.values()
            if hasattr(model, "__tablename__")
        }

    async def execute(
        self,
        query: Optional[Callable] = None,
        iterable: bool = False,
        scalars: bool = False,
        session: AsyncSession = coroutine_depends_on(get_async_session),
    ) -> Union[Iterator, List]:
        """
        SELECT all fields from manager modelss
        :param scalars:
        :param session: AsyncSession or AsyncSession from default Depends
        :param query: sqlalchemy sql
        :param iterable: iterator or not
        :return: Monad(QueryIterator or QueryList)
        """
        query = query if query is not None else select(self.model)
        res = await session.execute(query)
        if scalars:
            return res.scalars()
        return res.iterator if iterable else [i for i in res.iterator]

    async def get(
        self, query: Callable = None, raise_on: bool = False, **kwargs
    ) -> Optional[Callable]:
        """
        Returned one item by keys
        :return: Monad(QueryIterator or QueryList)
        """
        query = query if query is not None else select(self.model)
        if res := next(
            await self.execute(
                query.filter_by(**kwargs),
                iterable=True,
            ),
            None,
        ):
            return res
        if raise_on:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="No results found"
            )

    async def select_for_update(
        self,
        search_by: dict,
        session: AsyncSession = coroutine_depends_on(get_async_session),
        **kwargs,
    ):
        """
        :return:
        """
        try:
            record = await session.execute(
                select(self.model).filter_by(**search_by).with_for_update(nowait=True)
            )
            updated_record = record.scalar_one()
            for key, value in kwargs.items():
                setattr(updated_record, key, value)

            await session.flush()
            await session.refresh(updated_record)
            await session.commit()
        except Exception as exc:
            self.logger.error("update - an error occurred", error=str(exc))
            await session.rollback()
            raise ValueError("Record can not be updated.")

    async def get_or_create(
        self,
        data: Dict,
        scalars: bool = True,
        session: Optional[AsyncSession] = coroutine_depends_on(get_async_session),
    ) -> Union[Tuple[BaseModel], BaseModel]:
        """
        Get and create model if not exist by kwargs.
        Params:
            scalars: scalar or iterable chunk option of query response from session.execute method.
            data: Dict model field query searching for.
        Returns:
            Monad Union tuple of models or just one model like result session execution calling.
        """
        try:
            if res := await self.get(scalars=scalars, session=session, **data):
                return res
            await self.create(data=data, session=session)

        except Exception as exc:
            self.logger.error("update - an error occurred", error=str(exc))
            await session.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)
            )
        else:
            return await self.get(scalars=scalars, session=session, **data)

    async def create(
        self,
        data: Dict,
        session: AsyncSession = coroutine_depends_on(get_async_session),
    ):
        """
        Base model creation method. Use more detail error
        exception construction in child realization.
        """
        async with session.begin():
            try:
                res = await session.execute(insert(self.model).values(data))
            except Exception as exc:
                self.logger.error(f"create - an error occurred {str(exc)}")
                await session.rollback()
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)
                )
            else:
                await session.commit()
                return res

    async def update(
        self,
        model_id: str,
        session: AsyncSession = coroutine_depends_on(get_async_session),
        **kwargs,
    ):
        """
        Base model update method. Use more detail error
        exception construction in child realization. Called
        self.get for check existing before update.
        """
        async with session.begin():
            if _ := await self.get(id=model_id, raise_on=True, session=session):
                try:
                    res = await session.execute(
                        update(self.model)
                        .where(self.model.id == model_id)
                        .values(**kwargs)
                        .execution_options(synchronize_session="fetch")
                    )

                except Exception as exc:
                    self.logger.error(f"updated an error occurred {str(exc)}")
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)
                    )
                else:
                    await session.commit()
                    return res

    async def delete(
        self,
        pk: str,
        session: AsyncSession = coroutine_depends_on(get_async_session),
    ):
        """
        Base model delete method. Use more detail error
        exception construction in child realization. Called
        self.get for check existing before delete.
        """
        if _ := await self.get(id=pk, session=session, raise_on=True):
            with session.begin():
                try:
                    res = await session.execute(
                        delete(self.model).where(self.model.id == pk)
                    )
                except Exception as exc:
                    self.logger.error(f"deleted an error occurred {str(exc)}")
                    await session.rollback()
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)
                    )
                else:
                    await session.commit()
                    return res

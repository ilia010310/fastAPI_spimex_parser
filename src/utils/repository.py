import logging
from abc import ABC, abstractmethod
from datetime import datetime

from fastapi import HTTPException
from sqlalchemy import insert, select, update, distinct, desc
from sqlalchemy.ext.asyncio import AsyncSession

from schemas.trading_result import TradingResultSchema


class AbstractRepository(ABC):
    @abstractmethod
    async def add_one(self):
        raise NotImplementedError

    @abstractmethod
    async def find_all(self):
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository):
    model = None

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_one(self, data: dict) -> int:
        stmt = insert(self.model).values(**data).returning(self.model.id)
        res = await self.session.execute(stmt)
        return res.scalar_one()

    async def edit_one(self, id: int, data: dict) -> int:
        stmt = update(self.model).values(**data).filter_by(id=id).returning(self.model.id)
        res = await self.session.execute(stmt)
        return res.scalar_one()

    async def find_all(self):
        query = select(self.model)
        res = await self.session.execute(query)
        res = [row[0].to_read_model() for row in res.all()]
        return res

    async def find_one(self, **filter_by):
        stmt = select(self.model).filter_by(**filter_by)
        res = await self.session.execute(stmt)
        res = res.scalar_one().to_read_model()
        return res

    async def all_dates(self) -> list | HTTPException:
        try:
            query = select(distinct(self.model.date)).order_by(desc(self.model.date)).limit(
                1000)
            res = await self.session.execute(query)
            res = res.scalars().all()
            return res

        except Exception as e:
            logging.error(f'Не получилось забрать данные из БД ошибка: {e}')
            return HTTPException(status_code=500, detail=
            {
                "status": "error",
                "data": None,
                "detail": None,
            })

    async def get_dynamics(
            self,
            start_date: str,
            end_date: str,
            oil_id: str | None,
            delivery_type_id: str | None,
            delivery_basis_id: str | None,
            page: int,
            page_size: int
    ) -> list[TradingResultSchema] | HTTPException:
        try:
            start = datetime.strptime(start_date, "%d.%m.%Y")
            end = datetime.strptime(end_date, "%d.%m.%Y")
            offset = (page - 1) * page_size

        except ValueError:
            raise HTTPException(status_code=400, detail=f"Некорректная дата")
        query = (
            select(self.model)
            .where(self.model.date >= start)
            .where(self.model.date <= end)
            .order_by(self.model.date)
            .limit(page_size)
            .offset(offset)
        )

        if oil_id is not None:
            query = query.where(self.model.oil_id == oil_id)
        if delivery_type_id is not None:
            query = query.where(self.model.delivery_type_id == delivery_type_id)
        if delivery_basis_id is not None:
            query = query.where(self.model.delivery_basis_id == delivery_basis_id)

        result = await self.session.execute(query)

        res = result.scalars().all()
        res = [item.to_read_model() for item in res]
        return res

    async def get_last_result(self,
                              oil_id: str | None,
                              delivery_type_id: str | None,
                              delivery_basis_id: str | None,
                              page: int,
                              page_size: int
                              ):
        offset = (page - 1) * page_size
        query = select(self.model).limit(page_size).offset(offset)
        if oil_id is not None:
            query = query.where(self.model.oil_id == oil_id)
        if delivery_type_id is not None:
            query = query.where(self.model.delivery_type_id == delivery_type_id)
        if delivery_basis_id is not None:
            query = query.where(self.model.delivery_basis_id == delivery_basis_id)

        query = query.order_by(self.model.date.desc())

        result = await self.session.execute(query)
        res = result.scalars().all()
        res = [item.to_read_model() for item in res]
        return res

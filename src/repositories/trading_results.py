from datetime import datetime
from typing import List, Sequence

from fastapi import HTTPException
from sqlalchemy import select, distinct, desc

from models.trading_results import SpimexTradingResults
from schemas.trading_result import TradingResultSchema
from utils.repository import SQLAlchemyRepository


class TradingResultsRepository(SQLAlchemyRepository):
    model = SpimexTradingResults

    async def all_dates(self) -> list | HTTPException:
        try:
            query = select(distinct(self.model.date)).order_by(desc(self.model.date)).limit(
                1000)
            res = await self.session.execute(query)
            res = res.scalars().all()
            print(type(res[0]))
            return res

        except Exception:
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


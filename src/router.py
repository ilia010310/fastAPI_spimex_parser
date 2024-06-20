from fastapi import APIRouter, Query

from datetime import datetime
from typing import Optional

from fastapi_cache.decorator import cache
from sqlalchemy import select, distinct, desc
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import Depends, HTTPException

from .database import get_async_session
from .models import SpimexTradingResults
from .utils import get_expire_time

router = APIRouter(
    prefix="/home",
    tags=["Trading"]
)


@router.get("/last_trading_dates/")
@cache(expire=get_expire_time())
async def get_last_trading_dates(session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(distinct(SpimexTradingResults.date)).order_by(desc(SpimexTradingResults.date)).limit(1000)
        result = await session.execute(query)
        rows = result.scalars().all()
        return rows
    except Exception:
        return HTTPException(status_code=500, detail=
        {
            "status": "error",
            "data": None,
            "detail": None,
        })


@router.get("/dynamics/")
@cache(expire=get_expire_time())
async def get_dynamics(
        start_date: str,
        end_date: str,
        oil_id: Optional[int] = None,
        delivery_type_id: Optional[int] = None,
        delivery_basis_id: Optional[int] = None,
        page: int = Query(1, ge=1),
        page_size: int = Query(10, ge=1, le=100),
        session: AsyncSession = Depends(get_async_session)
):
    try:
        start = datetime.strptime(start_date, "%d.%m.%Y")
        end = datetime.strptime(end_date, "%d.%m.%Y")
        offset = (page - 1) * page_size
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Некорректная дата")
    query = (
        select(SpimexTradingResults)
        .where(SpimexTradingResults.date >= start)
        .where(SpimexTradingResults.date <= end)
        .order_by(SpimexTradingResults.date)
        .limit(page_size)
        .offset(offset)
    )

    if oil_id is not None:
        query = query.where(SpimexTradingResults.oil_id == oil_id)
    if delivery_type_id is not None:
        query = query.where(SpimexTradingResults.delivery_type_id == delivery_type_id)
    if delivery_basis_id is not None:
        query = query.where(SpimexTradingResults.delivery_basis_id == delivery_basis_id)

    result = await session.execute(query)
    rows = result.scalars().all()

    return rows


@router.get("/trading_results/")
@cache(expire=get_expire_time())
async def get_trading_results(
        oil_id: Optional[int] = None,
        delivery_type_id: Optional[int] = None,
        delivery_basis_id: Optional[int] = None,
        page: int = Query(1, ge=1),
        page_size: int = Query(10, ge=1, le=100),
        session: AsyncSession = Depends(get_async_session)
):
    offset = (page - 1) * page_size
    query = select(SpimexTradingResults).limit(page_size).offset(offset)

    if oil_id is not None:
        query = query.where(SpimexTradingResults.oil_id == oil_id)
    if delivery_type_id is not None:
        query = query.where(SpimexTradingResults.delivery_type_id == delivery_type_id)
    if delivery_basis_id is not None:
        query = query.where(SpimexTradingResults.delivery_basis_id == delivery_basis_id)

    query = query.order_by(SpimexTradingResults.date.desc())

    result = await session.execute(query)
    rows = result.scalars().all()

    return rows

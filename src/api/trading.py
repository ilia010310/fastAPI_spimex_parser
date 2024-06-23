from fastapi import APIRouter, Query

from typing import Optional, Sequence

from fastapi_cache.decorator import cache
from sqlalchemy import select

from api.dependencies import UOWDep
from models.trading_results import SpimexTradingResults
from services.trading_results import TradingResults
from utils.cache_time import get_expire_time

router = APIRouter(
    prefix="/trading",
    tags=["Trading"]
)


@router.get("/last_dates/")
@cache(expire=get_expire_time())
async def get_last_trading_dates(
        uow: UOWDep
) -> list:
    """Возвращает даты последних торгов (1000 уникальных дат) от самых недавных к самым поздним"""

    all_dates: list = await TradingResults().get_all_last_trading_dates(uow)
    return all_dates


@router.get("/dynamics/")
@cache(expire=get_expire_time())
async def get_dynamics(
        uow: UOWDep,
        start_date: str,
        end_date: str,
        oil_id: Optional[int] = None,
        delivery_type_id: Optional[int] = None,
        delivery_basis_id: Optional[int] = None,
        page: int = Query(1, ge=1),
        page_size: int = Query(10, ge=1, le=100),

) -> list:
    """Cписок торгов за заданный период
    (фильтрация по oil_id, delivery_type_id, delivery_basis_id, start_date, end_date)"""
    data: list[TradingResults] = await TradingResults().get_dynamics(
        uow,
        start_date,
        end_date,
        oil_id,
        delivery_type_id,
        delivery_basis_id,
        page,
        page_size,
    )
    return data


@router.get("/results/")
@cache(expire=get_expire_time())
async def get_trading_results(
        uow: UOWDep,
        oil_id: Optional[str] = None,
        delivery_type_id: Optional[str] = None,
        delivery_basis_id: Optional[str] = None,
        page: int = Query(1, ge=1),
        page_size: int = Query(10, ge=1, le=100),
):
    """Список последних торгов"""
    list_results = await TradingResults().find_all_results(uow,
                                                           oil_id,
                                                           delivery_type_id,
                                                           delivery_basis_id,
                                                           page,
                                                           page_size)
    return list_results

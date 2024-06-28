import fastapi

from src.schemas.trading_result import TradingResultSchema
from src.utils.unitofwork import IUnitOfWork


class TradingResults:
    async def get_all_last_trading_dates(self, uow: IUnitOfWork) -> list | fastapi.HTTPException:
        async with uow:
            result: list | fastapi.HTTPException = await uow.trading_results.all_dates()
            return result

    async def get_dynamics(
            self,
            uow: IUnitOfWork,
            start_date: str,
            end_date: str,
            oil_id: str | None,
            delivery_type_id: str | None,
            delivery_basis_id: str | None,
            page: int,
            page_size: int,
    ) -> list:
        async with uow:
            result = await uow.trading_results.get_dynamics(
                start_date,
                end_date,
                oil_id,
                delivery_type_id,
                delivery_basis_id,
                page,
                page_size)
            return result

    async def find_all_results(self,
                               uow: IUnitOfWork,
                               oil_id: str | None,
                               delivery_type_id: str | None,
                               delivery_basis_id: str | None,
                               page: int,
                               page_size: int
                               ):
        async with uow:
            result = await uow.trading_results.get_last_result(
                oil_id,
                delivery_type_id,
                delivery_basis_id,
                page,
                page_size)
        return result

    async def add_one(self, data: TradingResultSchema, uow: IUnitOfWork) -> int:
        async with uow:
            result = await uow.trading_results.add_one(dict(data))
        return result

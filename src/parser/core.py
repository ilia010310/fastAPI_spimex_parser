from datetime import datetime

from database import async_session
from models import SpimexTradingResults


# async def create_tables():
#     """Удаление и создание таблиц"""
#
#     async with async_engine.begin() as conn:
#         await conn.run_sync(Base.metadata.drop_all)
#         await conn.run_sync(Base.metadata.create_all)


async def async_inset_data(data_list: list[tuple]) -> None:
    """Добавление данных"""

    async with async_session() as s:
        for data in data_list:
            data_obj = SpimexTradingResults(
                exchange_product_id=data[0],
                exchange_product_name=data[1],
                oil_id=data[2],
                delivery_basis_id=data[3],
                delivery_basis_name=data[4],
                delivery_type_id=data[5],
                volume=data[6],
                total=data[7],
                count=data[8],
                date=datetime.strptime(data[9], "%d.%m.%Y"),
            )
            s.add(data_obj)
        await s.commit()

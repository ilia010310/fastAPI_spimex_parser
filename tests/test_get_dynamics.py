import pytest
from httpx import AsyncClient

from main import app
from src.repositories.trading_results import TradingResultsRepository
import asyncio

from tests.conftest import client


async def test_add_trading_result(ac: AsyncClient):
    response = await ac.post("/trading", json={
        "exchange_product_id": "test1",
        "exchange_product_name": "test2",
        "oil_id": "A100",
        "delivery_basis_id": "NYC",
        "delivery_basis_name": "W",
        "delivery_type_id": "NUW",
        "volume": 1,
        "total": 2,
        "count": 3,
        "date": "2024-07-25T19:32:10.141"
    })
    print(response.json()["result"])
    assert response.status_code == 200
    assert response.json()["status"] == "success"

async def test_get_last_trading_dates(ac: AsyncClient):
    response = await ac.get("/trading/last_dates")
    assert response.status_code == 200

# @pytest.mark.anyio
# async def test_get_specific_operations(ac: AsyncClient):
#     response = await ac.get("/trading/last_dates")
#     print(response.url)
#     print(response.status_code)
#     print(response.text)
#     print(response.headers["Location"])
#     assert 1 == 1

#     assert response.status_code == 200
#     assert response.json()["status"] == "success"
# assert len(response.json()["data"]) == 1

# @pytest.mark.parametrize(
#     """start_date,
#         end_date,
#         oil_id,
#         delivery_type_id,
#         delivery_basis_id,
#         page,
#         page_size,""", [
#         ('01.01.2024', '01.02.2024', None, None, None, 1, 10),
#         ('01.01.2024', "01.02.2024", 'A592', None, None, 1, 10),
#         ('01.01.2024', '01.02.2024', 'A592', None, None, 1, 10),
#         ('01.01.2024', '01.02.2024', None, 'W', None, 1, 10),
#         ('01.01.2024', '01.02.2024', None, None, 'ABS', 1, 10),
#         ('01.01.2024', '01.02.2024', 'A10K', 'W', 'ZLY', 1, 10),
#         ('01.01.2024', '01.02.2024', 'A10K', 'W', 'ZLY', 2, 100),
#
#     ]
# )
# async def test_get_dynamics_from_repo(self,
#                                 start_date,
#                                 end_date,
#                                 oil_id,
#                                 delivery_type_id,
#                                 delivery_basis_id,
#                                 page,
#                                 page_size
#                                 ):
#     result = await TradingResultsRepository.get_dynamics(
#         start_date,
#         end_date,
#         oil_id,
#         delivery_type_id,
#         delivery_basis_id,
#         page,
#         page_size
#     )
#     assert type(result) == list

import time

import pytest
from httpx import AsyncClient

from main import app
from src.repositories.trading_results import TradingResultsRepository
import asyncio

from tests.conftest import client


class TestTradingsAPI:
    async def test_add_trading_results(self, ac: AsyncClient):
        response = await ac.post("/api/trading", json={
            "exchange_product_id": "test1",
            "exchange_product_name": "test2",
            "oil_id": "A592",
            "delivery_basis_id": "NYC",
            "delivery_basis_name": "in",
            "delivery_type_id": "W",
            "volume": 1,
            "total": 2,
            "count": 3,
            "date": "2024-01-01T12:10:10.141"
        })
        assert response.status_code == 200
        assert response.json()["status"] == "success"
        assert response.json()["result"] == 1
        assert response.json()["message"] == "Trading item created successfully"
        for _ in range(15):
            response_2 = await ac.post("/api/trading", json={
                "exchange_product_id": "test2",
                "exchange_product_name": "test2",
                "oil_id": "A10K",
                "delivery_basis_id": "ZLY",
                "delivery_basis_name": "in",
                "delivery_type_id": "W",
                "volume": 1,
                "total": 2,
                "count": 3,
                "date": "2024-02-11T22:32:10.141"
            })
            assert response_2.json()["status"] == "success"

    async def test_get_last_trading_dates(self, ac: AsyncClient):
        response = await ac.get("/api/trading/last_dates/")
        assert response.status_code == 200
        assert len(list(response.json())) == 2

    @pytest.mark.parametrize(
        "start_date, end_date, oil_id, delivery_type_id, delivery_basis_id, page, page_size",
        [
            ('01.01.2024', '01.02.2025', None, None, None, 1, 10),
            ('01.01.2024', '01.02.2025', 'A592', None, None, 1, 10),
            ('01.01.2024', '01.02.2025', 'A592', None, None, 1, 10),
            ('01.01.2024', '01.02.2025', None, 'W', None, 1, 10),
            ('01.01.2024', '01.02.2025', None, None, 'ABS', 1, 10),
            ('01.01.2024', '01.02.2025', 'A10K', 'W', 'ZLY', 1, 10),
            ('01.01.2024', '01.02.2025', 'A10K', 'W', 'ZLY', 2, 100),
        ]
    )
    async def test_get_dynamics(self, ac: AsyncClient, start_date, end_date, oil_id, delivery_type_id,
                                delivery_basis_id, page, page_size):
        url = "/api/trading/dynamics/"
        params = {
            "start_date": start_date,
            "end_date": end_date,
            "oil_id": oil_id,
            "delivery_type_id": delivery_type_id,
            "delivery_basis_id": delivery_basis_id,
            "page": page,
            "page_size": page_size,
        }
        response = await ac.get(url, params=params)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    async def test_get_trading_results(self, ac: AsyncClient):
        params = {
            "oil_id": "A592",
            "delivery_type_id": "W",
            "delivery_basis_id": "NYC",
            "page": 1,
            "page_size": 10,
        }

        response = await ac.get("/api/trading/results/", params=params)

        assert response.status_code == 200

        data = response.json()
        assert isinstance(data, list)

        assert len(data) > 0

        assert all("exchange_product_id" in item for item in data)
        assert all("volume" in item for item in data)

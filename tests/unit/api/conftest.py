from datetime import datetime

import pytest

from src.models.trading_results import SpimexTradingResults

@pytest.fixture(scope="session")
async def add_test_data(db_session):
    # Здесь можно использовать вашу логику добавления тестовых данных в БД
    # Например, с использованием SQLAlchemy ORM
    data = [
        SpimexTradingResults(
            exchange_product_id="test1",
            exchange_product_name="test2",
            oil_id="A592",
            delivery_basis_id="NYC",
            delivery_basis_name="in",
            delivery_type_id="W",
            volume=1,
            total=2,
            count=3,
            date=datetime(2024, 1, 1, 12, 32, 10, 141)
        ),
        SpimexTradingResults(
            exchange_product_id="test2",
            exchange_product_name="test2",
            oil_id="A10K",
            delivery_basis_id="ZLY",
            delivery_basis_name="in",
            delivery_type_id="W",
            volume=1,
            total=2,
            count=3,
            date=datetime(2024, 2, 15, 12, 32, 10, 141)
        )
    ]

    db_session.add_all(data)
    await db_session.commit()

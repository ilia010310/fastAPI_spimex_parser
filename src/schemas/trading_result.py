from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class TradingResultSchema(BaseModel):
    exchange_product_id: str
    exchange_product_name: str
    oil_id: str
    delivery_basis_id: str
    delivery_basis_name: str
    delivery_type_id: str
    volume: int
    total: int
    count: int
    date: datetime

    model_config = ConfigDict(from_attributes=True)

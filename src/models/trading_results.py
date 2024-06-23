from datetime import datetime
from typing import Annotated

from sqlalchemy import DateTime, Index
from sqlalchemy.orm import mapped_column, Mapped

from db.database import Base
from schemas.trading_result import TradingResultSchema

int_pk = Annotated[int, mapped_column(primary_key=True)]


class SpimexTradingResults(Base):
    __tablename__ = 'spimex_trading_results'

    id: Mapped[int_pk]
    exchange_product_id: Mapped[str]
    exchange_product_name: Mapped[str]
    oil_id: Mapped[str]
    delivery_basis_id: Mapped[str]
    delivery_basis_name: Mapped[str]
    delivery_type_id: Mapped[str]
    volume: Mapped[int]
    total: Mapped[int]
    count: Mapped[int]
    date: Mapped[datetime] = mapped_column(DateTime)
    created_on: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now
    )
    updated_on: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now,
        onupdate=datetime.now
    )

    def to_read_model(self) -> TradingResultSchema:
        return TradingResultSchema(
            id=self.id,
            exchange_product_id=self.exchange_product_id,
            exchange_product_name=self.exchange_product_name,
            oil_id=self.oil_id,
            delivery_basis_id=self.delivery_basis_id,
            delivery_basis_name=self.delivery_basis_name,
            delivery_type_id=self.delivery_type_id,
            volume=self.volume,
            total=self.total,
            count=self.count,
            date=self.date
        )

    __table_args__ = (
        Index('ix_spimex_trading_results_date', 'date'),
    )

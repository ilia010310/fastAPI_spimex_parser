from src.models.trading_results import SpimexTradingResults
from src.utils.repository import SQLAlchemyRepository


class TradingResultsRepository(SQLAlchemyRepository):
    model = SpimexTradingResults




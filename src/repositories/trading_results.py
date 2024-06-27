from models.trading_results import SpimexTradingResults
from utils.repository import SQLAlchemyRepository


class TradingResultsRepository(SQLAlchemyRepository):
    model = SpimexTradingResults




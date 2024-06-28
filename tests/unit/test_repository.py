# from typing import Sequence
#
# from src.utils.repository import SQLAlchemyRepository
# from src.models.trading_results import SpimexTradingResults
#
# class TestSqlAlchemyRepository:
#
#     class _SqlAlchemyRepository(SQLAlchemyRepository):
#         model = SpimexTradingResults
#
#     async def test_add_one(
#             self, clean_users, users, get_users, comparing_two_sequence, async_session
#     ):
#         await clean_users()
#         sql_alchemy_repository = self._SqlAlchemyRepository(session=async_session)
#         for user_schema in users:
#             await sql_alchemy_repository.add_one(**user_schema.model_dump())
#             await sql_alchemy_repository.session.commit()
#
#         users_in_db: Sequence[SpimexTradingResults] = await get_users()
#         assert comparing_two_sequence(
#             users, [user.to_pydantic_schema() for user in users_in_db]
#         )
#         await async_session.close()
# from config import settings
# from models.base import BaseModel
# #
# #
# async def test_setup_db(async_engine):
#     assert settings.MODE == "TEST"
#     async with async_engine.begin() as db_conn:
#         await db_conn.run_sync(BaseModel.metadata.drop_all)
#         await db_conn.run_sync(BaseModel.metadata.create_all)
#         await db_conn.run_sync(BaseModel.metadata.drop_all)


# @pytest.mark.parametrize(
#     "x, y, res",
#     [
#         (1, 2, 0.5),
#         (-1, 5, -5)
#     ]
# )
# def test_first():
#     assert type(origins) == list



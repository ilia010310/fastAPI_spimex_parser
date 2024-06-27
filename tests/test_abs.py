from config import settings
from db.database import Base, async_engine
from src.main import origins
import pytest

# @pytest.mark.parametrize(
#     "x, y, res",
#     [
#         (1, 2, 0.5),
#         (-1, 5, -5)
#     ]
# )
# def test_first():
#     assert type(origins) == list



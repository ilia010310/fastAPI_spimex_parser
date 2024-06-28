from typing import Annotated, Type

from fastapi import Depends

from src.utils.unitofwork import IUnitOfWork, UnitOfWork

UOWDep: Type[IUnitOfWork] = Annotated[IUnitOfWork, Depends(UnitOfWork)]
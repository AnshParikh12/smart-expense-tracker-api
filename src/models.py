from datetime import date

from pydantic import BaseModel, ConfigDict, Field


class ExpenseBase(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True
    )

    title: str = Field(..., min_length=1)
    amount: float = Field(..., gt=0)
    category: str = Field(..., min_length=1)
    date: date


class ExpenseCreate(ExpenseBase):
    pass


class Expense(ExpenseBase):
    id: int


class ExpenseTotal(BaseModel):
    category: str
    total: float
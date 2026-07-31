from typing import Annotated

from fastapi import APIRouter, HTTPException, Query, Response, status

from src.models import Expense, ExpenseCreate, ExpenseTotal
from src.storage import (
    add_expense,
    calculate_total,
    delete_expense,
    get_all_expenses,
    get_expenses_by_category,
    search_expenses,
)

router = APIRouter()


@router.get("/")
def root():
    return {
        "name": "Smart Expense Tracker API",
        "version": "1.0.0",
        "status": "running",
    }

@router.post(
    "/expenses",
    response_model=Expense,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new expense",
)
def create_expense(expense: ExpenseCreate) -> Expense:
    """
    Create a new expense and store it.
    """
    return add_expense(expense)


@router.get(
    "/expenses",
    response_model=list[Expense],
    summary="Get expenses",
)
def get_expenses(
    category: Annotated[str | None, Query()] = None,
) -> list[Expense]:
    """
    Retrieve all expenses, optionally filtered by category.
    """
    if category:
        return get_expenses_by_category(category)

    return get_all_expenses()


@router.get(
    "/expenses/search",
    response_model=list[Expense],
    summary="Search expenses",
)
def search(
    q: Annotated[
        str,
        Query(
            min_length=1,
            description="Search by title or category",
        ),
    ],
) -> list[Expense]:
    """
    Search expenses by title or category.
    """
    return search_expenses(q)


@router.get(
    "/expenses/total",
    response_model=ExpenseTotal,
    summary="Calculate expense totals",
)
def get_total(
    category: Annotated[str | None, Query()] = None,
) -> ExpenseTotal:
    return ExpenseTotal(
        category=category or "Overall",
        total=calculate_total(category),
    )


@router.delete(
    "/expenses/{expense_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete an expense",
)
def delete_expense_by_id(expense_id: int) -> Response:
    """
    Delete an expense by its ID.
    """
    deleted = delete_expense(expense_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Expense with id {expense_id} not found.",
        )

    return Response(status_code=status.HTTP_204_NO_CONTENT)
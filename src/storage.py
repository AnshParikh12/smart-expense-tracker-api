import json
import os
from pathlib import Path
from typing import Any

from src.models import Expense, ExpenseCreate


def get_data_file() -> Path:
    """Return the JSON file used for storing expenses."""
    return Path(
        os.getenv(
            "EXPENSES_FILE",
            Path(__file__).parent / "expenses.json",
        )
    )


def initialize_storage() -> None:
    """Create the storage file if it doesn't exist."""
    data_file = get_data_file()

    if not data_file.exists():
        data_file.write_text("[]", encoding="utf-8")


def load_expenses() -> list[dict[str, Any]]:
    """Load all expenses from the JSON file."""
    with get_data_file().open("r", encoding="utf-8") as f:
        return json.load(f)


def save_expenses(expenses: list[dict[str, Any]]) -> None:
    """Save all expenses to the JSON file."""
    with get_data_file().open("w", encoding="utf-8") as f:
        json.dump(expenses, f, indent=4)


def get_next_id(expenses: list[dict[str, Any]]) -> int:
    """Generate the next available expense ID."""
    if not expenses:
        return 1

    return max(expense["id"] for expense in expenses) + 1


def get_all_expenses() -> list[Expense]:
    """Return all expenses."""
    return [Expense(**expense) for expense in load_expenses()]


def add_expense(expense: ExpenseCreate) -> Expense:
    """Add a new expense."""
    expenses = load_expenses()

    new_expense = expense.model_dump(mode="json")
    new_expense["id"] = get_next_id(expenses)

    expenses.append(new_expense)
    save_expenses(expenses)

    return Expense(**new_expense)


def delete_expense(expense_id: int) -> bool:
    """Delete an expense by ID."""
    expenses = load_expenses()

    updated_expenses = [
        expense
        for expense in expenses
        if expense["id"] != expense_id
    ]

    if len(updated_expenses) == len(expenses):
        return False

    save_expenses(updated_expenses)
    return True


def get_expenses_by_category(category: str) -> list[Expense]:
    """Return all expenses in a category."""
    return [
        Expense(**expense)
        for expense in load_expenses()
        if expense["category"].lower() == category.lower()
    ]


def calculate_total(category: str | None = None) -> float:
    """Calculate total expenses, optionally filtered by category."""
    expenses = load_expenses()

    if category:
        expenses = [
            expense
            for expense in expenses
            if expense["category"].lower() == category.lower()
        ]

    return sum(expense["amount"] for expense in expenses)


def search_expenses(query: str) -> list[Expense]:
    """Search expenses by title or category."""
    query = query.lower()

    return [
        Expense(**expense)
        for expense in load_expenses()
        if query in expense["title"].lower()
        or query in expense["category"].lower()
    ]
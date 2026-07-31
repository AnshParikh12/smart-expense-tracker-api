import os
import sys
from pathlib import Path

import pytest

# Add the project root to Python's path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

os.environ["EXPENSES_FILE"] = str(
    Path(__file__).parent / "test_expenses.json"
)

from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_test_file():
    """Reset test data before every test."""
    test_file = Path(os.environ["EXPENSES_FILE"])
    test_file.write_text("[]", encoding="utf-8")


def create_sample_expense(
    title="Coffee",
    amount=5.25,
    category="Food",
    date="2026-07-31",
):
    return client.post(
        "/expenses",
        json={
            "title": title,
            "amount": amount,
            "category": category,
            "date": date,
        },
    )


def test_create_expense():
    response = create_sample_expense()

    assert response.status_code == 201

    body = response.json()

    assert body["id"] == 1
    assert body["title"] == "Coffee"
    assert body["amount"] == 5.25
    assert body["category"] == "Food"
    assert body["date"] == "2026-07-31"


def test_get_all_expenses():
    create_sample_expense()

    response = client.get("/expenses")

    assert response.status_code == 200

    expenses = response.json()

    assert len(expenses) == 1
    assert expenses[0]["title"] == "Coffee"


def test_filter_expenses_by_category():
    create_sample_expense(
        title="Coffee",
        amount=5,
        category="Food",
    )

    create_sample_expense(
        title="Uber",
        amount=20,
        category="Travel",
    )

    response = client.get("/expenses?category=Food")

    assert response.status_code == 200

    expenses = response.json()

    assert len(expenses) == 1
    assert expenses[0]["category"] == "Food"
    assert expenses[0]["title"] == "Coffee"


def test_filter_is_case_insensitive():
    create_sample_expense(category="Food")

    response = client.get("/expenses?category=food")

    assert response.status_code == 200
    assert len(response.json()) == 1


def test_search_expenses():
    create_sample_expense(
        title="Coffee",
        category="Food",
    )

    create_sample_expense(
        title="Uber",
        category="Travel",
    )

    response = client.get("/expenses/search?q=coffee")

    assert response.status_code == 200

    expenses = response.json()

    assert len(expenses) == 1
    assert expenses[0]["title"] == "Coffee"


def test_search_by_category():
    create_sample_expense(
        title="Coffee",
        category="Food",
    )

    create_sample_expense(
        title="Lunch",
        category="Food",
    )

    response = client.get("/expenses/search?q=food")

    assert response.status_code == 200
    assert len(response.json()) == 2


def test_calculate_total():
    create_sample_expense(amount=10)
    create_sample_expense(title="Lunch", amount=20)

    response = client.get("/expenses/total")

    assert response.status_code == 200

    body = response.json()

    assert body["category"] == "Overall"
    assert body["total"] == 30


def test_calculate_category_total():
    create_sample_expense(amount=10, category="Food")
    create_sample_expense(title="Uber", amount=25, category="Travel")
    create_sample_expense(title="Lunch", amount=15, category="Food")

    response = client.get("/expenses/total?category=Food")

    assert response.status_code == 200

    body = response.json()

    assert body["category"] == "Food"
    assert body["total"] == 25


def test_category_total_with_no_matches():
    create_sample_expense(category="Food")

    response = client.get("/expenses/total?category=Travel")

    assert response.status_code == 200

    body = response.json()

    assert body["category"] == "Travel"
    assert body["total"] == 0


def test_delete_expense():
    create_sample_expense()

    response = client.delete("/expenses/1")

    assert response.status_code == 204

    response = client.get("/expenses")

    assert response.status_code == 200
    assert response.json() == []


def test_delete_nonexistent_expense():
    response = client.delete("/expenses/999")

    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_invalid_amount():
    response = client.post(
        "/expenses",
        json={
            "title": "Coffee",
            "amount": -5,
            "category": "Food",
            "date": "2026-07-31",
        },
    )

    assert response.status_code == 422


def test_empty_title():
    response = client.post(
        "/expenses",
        json={
            "title": "",
            "amount": 5,
            "category": "Food",
            "date": "2026-07-31",
        },
    )

    assert response.status_code == 422


def test_invalid_date():
    response = client.post(
        "/expenses",
        json={
            "title": "Coffee",
            "amount": 5,
            "category": "Food",
            "date": "not-a-date",
        },
    )

    assert response.status_code == 422
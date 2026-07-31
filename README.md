# Smart Expense Tracker API

A RESTful API built with **FastAPI** for managing personal expenses. The application allows users to create, view, filter, summarize, and delete expenses while storing data locally in a JSON file. No database is required.

## Features

* Add a new expense
* View all expenses
* Filter expenses by category
* Calculate total expenses
* Calculate total expenses by category
* Delete an expense
* Interactive API documentation via Swagger UI and ReDoc
* Automated test suite using Pytest
* Search expenses by title or category *(Bonus Feature)*

## Tech Stack

* Python 3.11+
* FastAPI
* Uvicorn
* Pydantic
* Pytest

## Project Structure

```text
smart-expense-tracker-api/
│
├── README.md
├── AI_NOTES.md
├── requirements.txt
├── .gitignore
│
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── models.py
│   ├── routes.py
│   ├── storage.py
│   └── expenses.json
│
└── tests/
    └── test_api.py
```

## Installation

### 1. Clone the repository

```bash
git clone <repository-url>
cd smart-expense-tracker-api
```

### 2. Create a virtual environment

**Windows**

```bash
python -m venv .venv
.venv\Scripts\activate
```

**macOS / Linux**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

## Run the Server

Start the FastAPI development server:

```bash
uvicorn src.main:app --reload
```

The API will be available at:

* API: http://127.0.0.1:8000
* Swagger UI: http://127.0.0.1:8000/docs
* ReDoc: http://127.0.0.1:8000/redoc

## Running the Tests

Run the complete test suite:

```bash
pytest
```

or

```bash
python -m pytest
```

All tests should pass successfully.

## API Endpoints

| Method | Endpoint                              | Description                             |
| ------ | ------------------------------------- | --------------------------------------- |
| GET    | `/`                                   | API status                              |
| POST   | `/expenses`                           | Create a new expense                    |
| GET    | `/expenses`                           | Retrieve all expenses                   |
| GET    | `/expenses?category={category}`       | Filter expenses by category             |
| GET    | `/expenses/total`                     | Calculate total expenses                |
| GET    | `/expenses/total?category={category}` | Calculate total expenses for a category |
| DELETE | `/expenses/{expense_id}`              | Delete an expense by ID                 |
| GET    | `/expenses/search?q={query}` | Search expenses by title or category |


## Data Storage

Expense data is stored in a local JSON file located at:

```text
src/expenses.json
```

No external database or additional configuration is required.

## Dependencies

The project dependencies are listed in `requirements.txt` and include:

* FastAPI
* Uvicorn
* Pydantic
* Pytest
* HTTPX

## Notes

* Expense IDs are generated automatically.
* Deleted expense IDs are not reused.
* Category filtering is case-insensitive.
* Input validation is handled using Pydantic models.
* The application automatically creates the JSON storage file if it does not already exist.

## Bonus Feature

This project implements the **Search Expenses** bonus feature.

Endpoint:

```text
GET /expenses/search?q=<search_term>
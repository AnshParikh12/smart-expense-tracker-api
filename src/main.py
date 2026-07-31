from fastapi import FastAPI

app = FastAPI(
    title="Smart Expense Tracker API",
    description="A REST API for tracking and managing personal expenses efficiently.",
    version="1.0.0"
)

@app.get("/")
def root():
    return {"message": "Welcome to the Smart Expense Tracker API!"}
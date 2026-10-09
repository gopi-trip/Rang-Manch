from fastapi import FastAPI
from contextlib import asynccontextmanager
from database import (create_tables)
from routes.reviews import router as reviews_router
from exceptions import (NoReviewsFound,no_reviews_found_handler)

@asynccontextmanager
async def lifespan(app:FastAPI):
    create_tables()
    print("Database tables have been created")
    yield
    #What happens when the server is shutting down i.e. the cleanup
    print("Shutting down the app")

app = FastAPI(
    title="Rang Manch Reviews API",
    description="Theatre Reviews API for Pune Rangmanch",
    lifespan=lifespan
)

app.add_exception_handler(NoReviewsFound,no_reviews_found_handler)

app.include_router(reviews_router)

@app.get("/")
def get_root():
    return {
        "Message":"Welcome to the Rang Manch API"
    }


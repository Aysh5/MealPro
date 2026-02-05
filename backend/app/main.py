from fastapi import FastAPI

from app.db import init_db
from app.router.health import router as health_router
from app.router.recipie import router as recipe_router

app = FastAPI(title="MealPro API", version="0.1.0")


@app.on_event("startup")
def on_startup():
    init_db()


app.include_router(health_router)
app.include_router(recipe_router)


@app.get("/")
def root():
    return {"name": "MealPro API", "status": "running"}

from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.core.database import create_db_and_tables
from app.routes.admin_routes import admin_router
from app.routes.user_routes import users_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(
    lifespan=lifespan,
    title = "NVC API",
    description = "API for NVC",
    version = "0.0.1",
)
app.include_router(users_router, prefix="/users")
app.include_router(admin_router, prefix="/admin")




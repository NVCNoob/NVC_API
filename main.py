from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.core.database import create_db_and_tables
from app.routes.admin_routes import admin_router
from app.routes.user_routes import users_router
from fastapi.middleware.cors import CORSMiddleware

@asynccontextmanager
async def lifespan(_: FastAPI):
    create_db_and_tables()
    yield

origins = [
    "http://0.0.0.0:8000", "https://nvc-official-frontend.vercel.app", "http://localhost:3000"
]

app = FastAPI(
    lifespan=lifespan,
    title = "NVC API",
    description = "API for NVC",
    version="0.0.1"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(users_router, prefix="/users")
app.include_router(admin_router, prefix="/admin")




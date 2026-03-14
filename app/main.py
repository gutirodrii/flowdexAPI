from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.router import api_router
from app.core.config import get_settings
from scripts.create_admin import ensure_admin

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    if settings.SEED_ADMIN_ON_STARTUP:
        await ensure_admin()
    yield


app = FastAPI(
    title="Flowdex API",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://erp.flowdex.es"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/healthz", include_in_schema=False)
async def healthcheck():
    return JSONResponse({"status": "ok"})


app.include_router(api_router, prefix=settings.API_V1_STR)

from fastapi import FastAPI
from app.core.config import settings
from app.api.v1.routers.health import router as health_router
from app.api.v1.routers import reports as reports_router 

def create_app() -> FastAPI:
    app = FastAPI(title="Report Service (DEV)", version="0.1.0")
    # CORS opcional
    origins = [o.strip() for o in settings.CORS_ORIGINS.split(",") if o.strip()]
    if origins:
        from fastapi.middleware.cors import CORSMiddleware
        app.add_middleware(
            CORSMiddleware,
            allow_origins=origins, allow_credentials=True,
            allow_methods=["*"], allow_headers=["*"],
        )
    app.include_router(health_router)
    app.include_router(reports_router.router)
    return app

app = create_app()
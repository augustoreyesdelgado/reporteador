import os

folders = [
    "app",
    "app/api/v1/routers",
    "app/core"
]

files = {
    "app/__init__.py": "",
    "app/main.py": '''from fastapi import FastAPI
from app.core.config import settings
from app.api.v1.routers.health import router as health_router

def create_app() -> FastAPI:
    app = FastAPI(title="Report Service", version="0.1.0")
    app.include_router(health_router)
    return app

app = create_app()
''',
    "app/core/__init__.py": "",
    "app/core/config.py": '''from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_ENV: str = "development"
    CORS_ORIGINS: str = ""

    class Config:
        env_file = ".env.dev"

settings = Settings()
''',
    "app/api/__init__.py": "",
    "app/api/v1/__init__.py": "",
    "app/api/v1/routers/__init__.py": "",
    "app/api/v1/routers/health.py": '''from fastapi import APIRouter

router = APIRouter(prefix="/v1", tags=["health"])

@router.get("/health")
def health():
    return {"status": "ok"}

@router.get("/ready")
def ready():
    return {"status": "ready"}
'''
}

for folder in folders:
    os.makedirs(folder, exist_ok=True)

for path, content in files.items():
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

print("Proyecto FastAPI base creado ✅")

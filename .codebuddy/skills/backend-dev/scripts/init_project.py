#!/usr/bin/env python3
"""后端项目初始化脚本 - 创建 FastAPI 项目骨架

用法:
    python scripts/init_project.py [target_dir]
    默认: src/backend
"""

import os
import sys


def write_file(path: str, content: str) -> None:
    """Write content to file if it doesn't exist."""
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"  Created: {path}")
    else:
        print(f"  Skipped (exists): {path}")


def create_project(base_dir: str) -> None:
    print(f"\n🚀 Initializing backend project at {base_dir}...\n")

    # 1. Create directory structure
    dirs = [
        f"{base_dir}/app",
        f"{base_dir}/app/models",
        f"{base_dir}/app/schemas",
        f"{base_dir}/app/api/v1",
        f"{base_dir}/app/services",
        f"{base_dir}/app/repositories",
        f"{base_dir}/app/middleware",
        f"{base_dir}/alembic/versions",
        f"{base_dir}/tests",
        f"{base_dir}/tests/unit",
        f"{base_dir}/tests/integration",
        f"{base_dir}/tests/api",
    ]

    for d in dirs:
        os.makedirs(d, exist_ok=True)

    # 2. Create __init__.py files
    init_dirs = [
        f"{base_dir}/app",
        f"{base_dir}/app/models",
        f"{base_dir}/app/schemas",
        f"{base_dir}/app/api",
        f"{base_dir}/app/api/v1",
        f"{base_dir}/app/services",
        f"{base_dir}/app/repositories",
        f"{base_dir}/app/middleware",
    ]

    for d in init_dirs:
        write_file(os.path.join(d, "__init__.py"), "")

    # 3. Create main.py
    write_file(f"{base_dir}/app/main.py", '''"""FastAPI Application Entry Point."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.api.router import api_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
)

# CORS - NOT wildcard in production
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")


@app.get("/api/v1/health")
async def health_check():
    return {"status": "ok", "version": settings.VERSION}
''')

    # 4. Create config.py
    write_file(f"{base_dir}/app/config.py", '''"""Application Configuration - all secrets from environment variables."""

from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    PROJECT_NAME: str = "My App"
    VERSION: str = "0.1.0"
    DEBUG: bool = False

    # Database
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/myapp"

    # Auth
    SECRET_KEY: str = "change-me-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ALGORITHM: str = "HS256"

    # CORS
    ALLOWED_ORIGINS: List[str] = ["http://localhost:5173", "http://localhost:3000"]

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
''')

    # 5. Create database.py
    write_file(f"{base_dir}/app/database.py", '''"""Database Connection and Session Management."""

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from app.config import settings

engine = create_async_engine(settings.DATABASE_URL, echo=settings.DEBUG)
async_session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


async def get_db():
    async with async_session_maker() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
''')

    # 6. Create router.py
    write_file(f"{base_dir}/app/api/router.py", '''"""Main API Router - register all v1 routers."""

from fastapi import APIRouter

api_router = APIRouter()

# Import and include entity routers here:
# from app.api.v1.users import router as users_router
# api_router.include_router(users_router)
''')

    # 7. Create requirements.txt
    write_file(f"{base_dir}/requirements.txt", '''fastapi>=0.110.0
uvicorn[standard]>=0.27.0
sqlalchemy[asyncio]>=2.0.0
alembic>=1.13.0
pydantic>=2.5.0
pydantic-settings>=2.1.0
asyncpg>=0.29.0
python-jose[cryptography]>=3.3.0
passlib[bcrypt]>=1.7.4
httpx>=0.26.0
pytest>=7.4.0
pytest-asyncio>=0.23.0
''')

    # 8. Create alembic.ini
    write_file(f"{base_dir}/alembic.ini", '''[alembic]
script_location = alembic
sqlalchemy.url = postgresql+asyncpg://postgres:postgres@localhost:5432/myapp

[loggers]
keys = root,sqlalchemy,alembic

[handlers]
keys = console

[formatters]
keys = generic

[logger_root]
level = WARN
handlers = console

[logger_sqlalchemy]
level = WARN
handlers =
qualname = sqlalchemy.engine

[logger_alembic]
level = INFO
handlers =
qualname = alembic

[handler_console]
class = StreamHandler
args = (sys.stderr,)
level = NOTSET
formatter = generic

[formatter_generic]
format = %(levelname)-5.5s [%(name)s] %(message)s
datefmt = %H:%M:%S
''')

    # 9. Create alembic env.py
    write_file(f"{base_dir}/alembic/env.py", '''"""Alembic migration environment."""

import asyncio
from logging.config import fileConfig
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import async_engine_from_config
from alembic import context
from app.database import Base
from app.config import settings

config = context.config
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(url=url, target_metadata=target_metadata, literal_binds=True)
    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection):
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)
    await connectable.dispose()


def run_migrations_online() -> None:
    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
''')

    # 10. Create .env.example
    write_file(f"{base_dir}/.env.example", '''# Application
PROJECT_NAME=My App
VERSION=0.1.0
DEBUG=false

# Database
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/myapp

# Auth - MUST change in production
SECRET_KEY=change-me-in-production
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS
ALLOWED_ORIGINS=["http://localhost:5173","http://localhost:3000"]
''')

    write_file(f"{base_dir}/.env", '''# Application
PROJECT_NAME=My App
VERSION=0.1.0
DEBUG=true

# Database
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/myapp

# Auth - MUST change in production
SECRET_KEY=change-me-in-production
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS
ALLOWED_ORIGINS=["http://localhost:5173","http://localhost:3000"]
''')

    # 11. Create test conftest.py
    write_file(f"{base_dir}/tests/conftest.py", '''"""Test configuration and fixtures."""

import asyncio
import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from app.database import Base, get_db
from app.main import app
from app.config import settings

# Use a separate test database
TEST_DATABASE_URL = settings.DATABASE_URL.replace("/myapp", "/myapp_test")
test_engine = create_async_engine(TEST_DATABASE_URL, echo=False)
TestSessionMaker = async_sessionmaker(test_engine, class_=AsyncSession, expire_on_commit=False)


async def override_get_db():
    async with TestSessionMaker() as session:
        yield session


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(autouse=True)
async def setup_database():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
''')

    print(f"\n✅ Backend project initialized at {base_dir}")
    print(f"   Run 'cd {base_dir} && uvicorn app.main:app --reload' to start dev server")


if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "src/backend"
    create_project(target)

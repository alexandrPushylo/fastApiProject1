import pytest
from sqlalchemy.ext.asyncio import create_async_engine

from src.database import Base, engine_null_pool
from src.main import app
from src.models import *
from src.config import settings
from httpx import AsyncClient, ASGITransport

@pytest.fixture(scope="session", autouse=True)
async def check_test_mode():
    assert settings.MODE == "TEST"


@pytest.fixture(scope="session", autouse=True)
async def setup_database(check_test_mode):
    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@pytest.fixture(scope="session", autouse=True)
async def test_register_user(setup_database):
    async with AsyncClient(transport=ASGITransport(app=app), base_url='http://test') as ac:
        response = await ac.post("/auth/register",
                                 json={
                                     "email": "test@user.com",
                                     "password": "1234"
                                 })
from typing import Any, AsyncGenerator

import json
from unittest import mock
mock.patch("fastapi_cache.decorator.cache", lambda *args, **kwargs: lambda fn: fn).start()

import pytest

from src.api.dependencies import get_db
from schemas.hotels import HotelAdd
from schemas.rooms import RoomAdd
from src.database import Base, engine_null_pool, async_session_maker_null_pool
from src.main import app
from src.models import *
from src.config import settings
from httpx import AsyncClient, ASGITransport

from src.utils.db_manager import DBManager


@pytest.fixture(scope="session", autouse=True)
async def check_test_mode():
    assert settings.MODE == "TEST"


async def get_db_null_pool() -> AsyncGenerator[DBManager, Any]:
    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        yield db

@pytest.fixture(scope='function')
async def db() -> AsyncGenerator[DBManager, Any]:
    async for db in get_db_null_pool():
        yield db

app.dependency_overrides[get_db] = get_db_null_pool

@pytest.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, Any]:
    async with AsyncClient(transport=ASGITransport(app=app), base_url='http://test') as ac:
        yield ac

@pytest.fixture(scope="session", autouse=True)
async def setup_database(check_test_mode):
    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    with open('tests/mock_hotels.json', encoding='utf-8') as json_file:
        json_data = json.load(json_file)
    hotel_data = [HotelAdd.model_validate(hotel) for hotel in json_data]
    with open('tests/mock_rooms.json', encoding='utf-8') as json_file:
        json_data = json.load(json_file)
    room_data = [RoomAdd.model_validate(room) for room in json_data]

    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        await db.hotels.add_bulk(hotel_data)
        await db.rooms.add_bulk(room_data)
        await db.commit()


@pytest.fixture(scope="session", autouse=True)
async def register_user(setup_database, ac):
    await ac.post("/auth/register",
                  json={
                      "email": "test@user.com",
                      "password": "1234"
                  })


@pytest.fixture(scope="session")
async def authenticated_ac(register_user, ac):
    response = await ac.post("/auth/login", json={
        "email": "test@user.com",
        "password": "1234"
    })
    assert response.status_code == 200
    assert ac.cookies["access_token"]
    yield ac



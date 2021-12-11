import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.commons.database import DBSession, new_connection_pool
from app.interfaces.http import (init_routes, init_event_handlers,
                                 init_error_handling, init_middleware)


NUMBER_OF_SEED_DATA = 326
PLAYER_NAME = "Todd Gurley"
SORT_TD_ASC = "total_rushing_touch_down,asc"
SORT_TD_DESC = "total_rushing_touch_down,desc"
HIGH_TD = 18
LOW_TD = 0


@pytest.fixture
@pytest.mark.asyncio
async def db_session() -> DBSession:
    db_pool = new_connection_pool()
    await db_pool.connect()
    db_session = DBSession(db_pool)
    yield db_session
    await db_pool.close()


@pytest.fixture
async def db_connector():
    db = new_connection_pool()
    await db.connect()
    return db


@pytest.fixture
def app(db_connector):
    rest_api = FastAPI(
        title="Rushing Service REST api",
        description="",
        docs_url="/docs",
    )
    rest_api.db_connector = db_connector
    init_routes(rest_api)
    init_error_handling(rest_api)
    init_middleware(rest_api)
    init_event_handlers(rest_api)

    return rest_api


@pytest.fixture
def app_client(app):
    client = TestClient(app, raise_server_exceptions=False)
    return client

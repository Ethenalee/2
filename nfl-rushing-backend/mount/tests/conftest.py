import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.interfaces.http import (init_routes,
                                 init_error_handling, init_middleware)


@pytest.fixture
def app():
    rest_api = FastAPI(
        title="Rushing Service REST api",
        description="",
        docs_url="/docs",
    )
    init_routes(rest_api)
    init_error_handling(rest_api)
    init_middleware(rest_api)

    return rest_api


@pytest.fixture
def app_client(app):
    client = TestClient(app, raise_server_exceptions=False)
    return client

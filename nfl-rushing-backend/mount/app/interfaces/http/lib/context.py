from starlette.requests import Request

from app.commons.database import DBSession


class RequestContext:
    def __init__(self, request: Request):
        self._request = request

    @property
    def db(self) -> DBSession:
        return self._request.state.db

from typing import List, Optional, Union
import math

from fastapi import APIRouter, Security, Query
from pydantic import BaseModel

from app.commons import logger
from app.commons.exceptions import AppErrorCode, AppErrorMessage
from app.interfaces.http.lib.auth import no_auth
from app.interfaces.http.lib.context import RequestContext
from app.interfaces.http.lib.responses import ErrorResponse, SuccessResponse, \
    ValidationErrorResponse, FieldError
from app.usecases.rushing import RushingUsecases, GetRushingResponse

router = APIRouter()


class PaginationMeta(BaseModel):
    page: Optional[int]
    per_page: Optional[int]
    total_results: Optional[int]
    total_pages: Optional[int]


@router.get("/rushings", status_code=200,
            response_model=List[GetRushingResponse])
async def get_all(
    name: Optional[str] = Query(None),
    sort: Optional[List[str]] = Query(None),
    page: Optional[int] = Query(None),
    per_page: Optional[int] = Query(None),
    ctx: RequestContext = Security(no_auth),
) -> Union[SuccessResponse, ErrorResponse]:
    logger.debug("received get rushing request")
    try:
        data, count = await RushingUsecases(ctx.db) \
            .get_all(name=name, sort=sort, page=page, per_page=per_page)

    except ValueError as exc:
        logger.error(f"Invalid params: {exc}")
        return ValidationErrorResponse(
            [
                FieldError(
                    code=AppErrorCode.INVALID_PARAMS.value,
                    field="query",
                    message=AppErrorMessage.INVALID_PARAMS.value,
                ),
            ]
        )

    meta = PaginationMeta(
        page=page if page and per_page else 1,
        per_page=per_page if per_page and page else count,
        total_results=count,
        total_pages=math.ceil(count/per_page) if per_page and page else 1
    )

    return SuccessResponse([rushing.dict() for rushing in data],
                           meta=meta.dict())

from datetime import datetime
from decimal import Decimal
from typing import List, Optional, Tuple
from pydantic import BaseModel

from app.commons.database import DBSession
from app.repositories.rushing import \
    RushingRepo, RushingFilters, SortFilter, PageFilter


class GetRushingResponse(BaseModel):
    name: str
    team_abbreviation: str
    position: str
    att: int
    att_per_game_avg: Decimal
    total_rushing_yards: int
    rushing_avg_yds_per_att: Decimal
    rushing_yds_per_game: Decimal
    total_rushing_touch_down: int
    lng_rush: str
    rushing_1st_down: int
    rushing_1st_down_perc: Decimal
    rushing_20_plus_yds_each: Decimal
    rushing_40_plus_yds_each: Decimal
    fum: Decimal
    updated_at: datetime
    created_at: datetime


class RushingUsecases:
    def __init__(self, db: DBSession):
        self._db = db

    async def get_all(
        self,
        name: Optional[str] = None,
        page: Optional[int] = None,
        per_page: Optional[int] = None,
        sort: Optional[List[str]] = None,
    ) -> Tuple[List[GetRushingResponse], int]:
        repo = RushingRepo(self._db)
        if sort:
            sort = [SortFilter.create_from_params(sort_pair)
                    for sort_pair in sort]

        filters = RushingFilters(
            name=name,
            page=PageFilter(offset=(page*per_page), limit=per_page)
            if page and per_page else None,
            sort=sort if sort else None
        )
        rushings = await repo.get_with_filters(filters=filters)
        count = await repo.count_with_filters(filters=filters)
        return [
            GetRushingResponse(
                name=rushing.name,
                team_abbreviation=rushing.team_abbreviation,
                position=rushing.position,
                att=rushing.att,
                att_per_game_avg=rushing.att_per_game_avg,
                total_rushing_yards=int(rushing.total_rushing_yards
                                        .replace(',', '')),
                rushing_avg_yds_per_att=rushing.rushing_avg_yds_per_att,
                rushing_yds_per_game=rushing.rushing_yds_per_game,
                total_rushing_touch_down=rushing.total_rushing_touch_down,
                lng_rush=rushing.lng_rush,
                rushing_1st_down=rushing.rushing_1st_down,
                rushing_1st_down_perc=rushing.rushing_1st_down_perc,
                rushing_20_plus_yds_each=rushing.rushing_20_plus_yds_each,
                rushing_40_plus_yds_each=rushing.rushing_40_plus_yds_each,
                fum=rushing.fum,
                updated_at=rushing.updated_at,
                created_at=rushing.created_at,
            ) for rushing in rushings
        ], count

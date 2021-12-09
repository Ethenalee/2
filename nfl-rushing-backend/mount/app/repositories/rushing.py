from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import List
from uuid import UUID

from app.commons.database import DBSession


@dataclass(frozen=True)
class Rushing:
    rec_id: int
    rushing_id: UUID
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

    @staticmethod
    def from_rec(rec) -> Rushing:
        return Rushing(
            rec_id=rec.get("rec_id"),
            rushing_id=rec.get("rushing_id"),
            name=rec.get("name"),
            team_abbreviation=rec.get("team_abbreviation"),
            position=rec.get("position"),
            att=rec.get("att"),
            att_per_game_avg=rec.get("att_per_game_avg"),
            total_rushing_yards=rec.get("total_rushing_yards"),
            rushing_avg_yds_per_att=rec.get("rushing_avg_yds_per_att"),
            rushing_yds_per_game=rec.get("rushing_yds_per_game"),
            total_rushing_touch_down=rec.get("total_rushing_touch_down"),
            lng_rush=rec.get("lng_rush"),
            rushing_1st_down=rec.get("rushing_1st_down"),
            rushing_1st_down_perc=rec.get("rushing_1st_down_perc"),
            rushing_20_plus_yds_each=rec.get("rushing_20_plus_yds_each"),
            rushing_40_plus_yds_each=rec.get("rushing_40_plus_yds_each"),
            fum=rec.get("fum"),
            updated_at=rec.get("updated_at"),
            created_at=rec.get("created_at"),
        )


class RushingRepo:
    def __init__(self, db: DBSession):
        self._queries = _QueryBuilder()
        self._db = db

    async def get_all(self, offset: int, limit: int) -> List[Rushing]:
        sql = self._queries.get_all()
        rec = await self._db.exec_read(sql, {"limit": limit, "offset": offset})
        return [Rushing.from_record(tx) for tx in rec]


class _QueryBuilder:
    TABLE = "rushings"

    READ_PARAMS = """
                rec_id,
                rushing_id,
                name,
                team_abbreviation,
                position,
                att,
                att_per_game_avg,
                total_rushing_yards,
                rushing_avg_yds_per_att,
                rushing_yds_per_game,
                total_rushing_touch_down,
                lng_rush,
                rushing_1st_down,
                rushing_1st_down_perc,
                rushing_20_plus_yds_each,
                rushing_40_plus_yds_each,
                fum,
                updated_at,
                created_at
                     """

    BASE_READ = f"""
            SELECT {READ_PARAMS} FROM {TABLE}
        """

    def get_all(self) -> str:
        return f"""
                {self.BASE_READ}
                ORDER BY
                    rec_id DESC
                LIMIT :limit OFFSET :offset
        """

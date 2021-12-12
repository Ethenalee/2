from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import List, Optional

from app.commons.database import DBSession


@dataclass(frozen=True)
class Rushing:
    rec_id: int
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
    def from_record(rec) -> Rushing:
        return Rushing(
            rec_id=rec.get("rec_id"),
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


@dataclass
class PageFilter:
    limit: int
    offset: int

    @property
    def page_query(self):
        return f" LIMIT {self.limit} OFFSET {self.offset}"


class SortField(str, Enum):
    total_rushing_yards = "total_rushing_yards"
    lng_rush = "lng_rush"
    total_rushing_touch_down = "total_rushing_touch_down"
    name = "name"


class SortDirection(str, Enum):
    ASC = "asc"
    DESC = "desc"


@dataclass
class SortFilter:
    field: SortField
    direction: Optional[SortDirection] = SortDirection.ASC

    @property
    def field_and_direction(self):
        return f"{self.field.name} {self.direction.name}"

    @staticmethod
    def create_from_params(sort_pair: str) -> "SortFilter":
        pair = sort_pair.split(",")
        field = SortField(pair[0])
        direction = SortDirection(pair[1]) if len(pair) == 2 \
            else SortDirection.ASC

        return SortFilter(field, direction)


@dataclass
class RushingFilters:
    name: Optional[str] = None
    page: Optional[PageFilter] = None
    sort: Optional[List[SortFilter]] = None

    @property
    def conditions_query(self):
        list_of_conditions = []
        if self.name is not None:
            list_of_conditions.append(
                "name = :name"
            )

        return " AND ".join(list_of_conditions)

    @property
    def sort_query(self):
        if self.sort:
            list_of_sort_filters = [s.field_and_direction for s in self.sort]
            return ", ".join(list_of_sort_filters)
        else:
            return "rec_id desc"


class RushingRepo:
    def __init__(self, db: DBSession):
        self._queries = _QueryBuilder()
        self._db = db

    async def get_with_filters(
        self, filters: RushingFilters
    ) -> List[Rushing]:
        sql = self._queries.get_with_filters(filters)
        values = {}
        if filters.name:
            values["name"] = filters.name

        recs = await self._db.exec_read(sql, values)
        return [Rushing.from_record(rec) for rec in recs]

    async def count_with_filters(self, filters: RushingFilters) -> int:
        sql = self._queries.count_with_filters(filters)
        values = {}
        if filters.name:
            values["name"] = filters.name
        rec = await self._db.exec_read_one(sql, values)
        count = rec.get("count")
        return count


class _QueryBuilder:
    TABLE = "rushingrecords"

    READ_PARAMS = """
                rec_id,
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

    def get_with_filters(self, filters: RushingFilters) -> str:

        query = f"""{self.BASE_READ} WHERE rec_id IN
                    (SELECT max(rec_id)
                    FROM rushingrecords GROUP BY rec_id)
        """

        if filters.conditions_query:
            query += f"AND {filters.conditions_query} "

        query += f"ORDER BY {filters.sort_query}"

        if filters.page:
            query += f"{filters.page.page_query}"

        return query

    def count_with_filters(cls, filters: RushingFilters) -> str:
        query = """ SELECT COUNT(*) FROM rushingrecords
                    WHERE rec_id IN (SELECT max(rec_id)
                    FROM rushingrecords GROUP BY rec_id)
        """
        if filters.conditions_query:
            query += f"AND {filters.conditions_query} "
        return query

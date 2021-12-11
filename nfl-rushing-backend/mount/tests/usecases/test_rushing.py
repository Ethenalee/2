import pytest

from app.commons.database import DBSession
from app.usecases.rushing import RushingUsecases
from tests.conftest import NUMBER_OF_SEED_DATA, PLAYER_NAME, \
                            SORT_TD_DESC, SORT_TD_ASC, HIGH_TD, LOW_TD


@pytest.mark.asyncio
async def test_get_all_without_filter(
    db_session: DBSession,
):
    rushing_usecase = RushingUsecases(db_session)
    _, count = await rushing_usecase.get_all()

    assert count == NUMBER_OF_SEED_DATA


@pytest.mark.asyncio
async def test_get_all_with_name_filter(
    db_session: DBSession,
):
    rushing_usecase = RushingUsecases(db_session)
    data, count = await rushing_usecase.get_all(name=PLAYER_NAME)

    assert count == 1
    assert data[0].name == PLAYER_NAME


@pytest.mark.asyncio
async def test_get_all_with_page_per_page_filter(
    db_session: DBSession,
):
    page = 1
    per_page = 10
    rushing_usecase = RushingUsecases(db_session)
    data, _ = await rushing_usecase.get_all(page=page, per_page=per_page)

    assert len(data) == per_page


@pytest.mark.asyncio
async def test_get_all_with_sort_filter(
    db_session: DBSession,
):

    rushing_usecase = RushingUsecases(db_session)
    asc_data, _ = await rushing_usecase.get_all(
                 sort=[SORT_TD_ASC])
    desc_data, _ = await rushing_usecase.get_all(
                 sort=[SORT_TD_DESC])

    assert asc_data[0].total_rushing_touch_down \
        == LOW_TD
    assert desc_data[0].total_rushing_touch_down \
        == HIGH_TD


@pytest.mark.asyncio
async def test_get_all_with_wrong_filter(
    db_session: DBSession,
):
    rushing_usecase = RushingUsecases(db_session)

    with pytest.raises(ValueError):
        await rushing_usecase.get_all(sort=["total_rushing_touch_dow,asc"])

from tests.conftest import NUMBER_OF_SEED_DATA, PLAYER_NAME, SORT_TD_ASC, \
                        LOW_TD


def test_get_all_returns_200(app_client):
    resp = app_client.get("/v1/rushingrecords")
    meta = resp.json()["meta"]
    assert resp.status_code == 200
    assert meta["total_pages"] == 1
    assert meta["total_results"] == NUMBER_OF_SEED_DATA


def test_get_all_return_with_name_filter_200(app_client):
    params = {"name": PLAYER_NAME}
    resp = app_client.get("/v1/rushingrecords", params=params)
    data = resp.json()["data"]
    meta = resp.json()["meta"]
    assert resp.status_code == 200
    assert data[0]["name"] == PLAYER_NAME
    assert meta["total_pages"] == 1
    assert meta["total_results"] == 1


def test_get_all_return_with_wrong_name_filter_200(app_client):
    params = {"name": "random"}
    resp = app_client.get("/v1/rushingrecords", params=params)
    data = resp.json()["data"]
    meta = resp.json()["meta"]
    assert resp.status_code == 200
    assert len(data) == 0
    assert meta["total_pages"] == 1
    assert meta["total_results"] == 0


def test_get_all_return_with_sort_filter_200(app_client):
    params = {"sort": SORT_TD_ASC}
    resp = app_client.get("/v1/rushingrecords", params=params)
    data = resp.json()["data"]
    meta = resp.json()["meta"]
    assert resp.status_code == 200
    assert data[0]["total_rushing_touch_down"] == LOW_TD
    assert meta["total_pages"] == 1
    assert meta["total_results"] == NUMBER_OF_SEED_DATA


def test_get_all_return_with_wrong_sort_filter_422(app_client):
    params = {"sort": "mistake"}
    resp = app_client.get("/v1/rushingrecords", params=params)
    assert resp.status_code == 422


def test_get_all_return_with_wrong_paginate_filter_422(app_client):
    params = {"page": "d", "per_page": "1"}
    resp = app_client.get("/v1/rushingrecords", params=params)
    assert resp.status_code == 422

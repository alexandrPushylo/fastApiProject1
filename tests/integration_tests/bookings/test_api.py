import pytest


@pytest.mark.parametrize(
    "room_id, date_from, date_to, status_code",
    [
        (1, "2026-01-01", "2026-01-10", 200),
        (1, "2026-01-01", "2026-01-11", 200),
        (1, "2026-01-01", "2026-01-12", 200),
        (1, "2026-01-01", "2026-01-13", 200),
        (1, "2026-01-01", "2026-01-14", 200),
        (1, "2026-01-01", "2026-01-15", 500),
        (1, "2026-01-11", "2026-01-25", 200),
    ])
async def test_add_booking(
        db,
        authenticated_ac,
        room_id,
        date_from,
        date_to,
        status_code,
):
    response = await authenticated_ac.post(
        "/bookings",
        json={
            "room_id": room_id,
            "date_from": date_from,
            "date_to": date_to,
        }
    )
    assert response.status_code == status_code
    if status_code == 200:
        res = response.json()
        assert isinstance(res, dict)
        assert res["status"] == "OK"
        assert 'data' in res


@pytest.fixture(scope="function")
async def delete_all_bookings(db):
    await db.bookings.delete()
    await db.commit()


@pytest.mark.parametrize(
    "room_id, date_from, date_to, count_bookings",
    [
        (1, "2026-01-01", "2026-01-10", 1),
        (1, "2026-01-02", "2026-01-10", 2),
        (1, "2026-01-03", "2026-01-10", 3),
    ]
)
async def test_add_and_get_my_bookings(
        room_id,
        date_from,
        date_to,
        count_bookings,
        delete_all_bookings,
        authenticated_ac,
):
    for i in range(count_bookings):
        response = await authenticated_ac.post(
            "/bookings",
            json={
                "room_id": room_id,
                "date_from": date_from,
                "date_to": date_to,
            }
        )
        assert response.status_code == 200

    response = await authenticated_ac.get(
        "/bookings/me",
    )
    assert response.status_code == 200
    res = response.json()
    assert len(res) == count_bookings

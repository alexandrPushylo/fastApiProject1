import pytest


@pytest.mark.parametrize(
    "email, password, status_code",
    [
        ("user1@user.com", "1234", 200),
        ("user1@user.com", "1234", 409),
    ])
async def test_auth_flow(
        email,
        password,
        status_code,
        db,
        ac,
        authenticated_ac,
):
    response_register = await ac.post(
        "/auth/register",
        json={
            "email": email,
            "password": password,
        }
    )
    assert response_register.status_code == status_code
    if status_code == 200:
        res = response_register.json()
        assert res["status"] == 'ok'

    response_login = await ac.post(
        "/auth/login",
        json={
            "email": email,
            "password": password,
        }
    )
    assert response_login.status_code == 200
    assert 'access_token' in ac.cookies


    response_get_me = await ac.get("/auth/me")
    assert response_get_me.status_code == 200
    if status_code == 200:
        res = response_get_me.json()
        assert 'id' in res
        assert 'email' in res
        assert email in res["email"]
        assert ac.cookies["access_token"]


    response_logout = await ac.post("/auth/logout")
    assert response_logout.status_code == 200
    assert 'access_token' not in ac.cookies
    if status_code == 200:
        res = response_logout.json()
        assert 'status' in res
        assert res["status"] == 'ok'

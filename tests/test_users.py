async def test_register(client):
    response = await client.post("/user/register", json={"username": "mariamissnf",
        "email": "mariamissnf@gmail.com", "name": "maria", "surname": "missnf",
        "university": "sinclarr", "degree": "nursing", "level": "2", "year": "1", "password": "myPass@343"})

    assert response.status_code == 200
    assert response.json()["username"] == "mariamissnf"
    assert "password" not in response.json()
    assert "password_hash" not in response.json()


async def test_register_duplicate_username(client):
    await client.post("/user/register", json={"username": "mariamissnf",
        "email": "mariamissnf@gmail.com", "name": "maria", "surname": "missnf",
        "university": "sinclarr", "degree": "nursing", "level": "2", "year": "1", "password": "myPass@343"})

    response = await client.post("/user/register", json={"username": "mariamissnf",
        "email": "mariamissnf55@gmail.com", "name": "maria", "surname": "mif",
        "university": "hahhah", "degree": "jdmmdmm", "level": "2", "year": "1", "password": "myPass@343"})

    assert response.status_code == 400
    assert response.json()["detail"] == "Username already exists."


async def test_register_duplicate_email(client):
    await client.post("/user/register", json={"username": "mariamissnf",
        "email": "mariamissnf@gmail.com", "name": "maria", "surname": "missnf",
        "university": "sinclarr", "degree": "nursing", "level": "2", "year": "1", "password": "myPass@343"})

    response = await client.post("/user/register", json={"username": "mariammar",
        "email": "mariamissnf@gmail.com", "name": "maria", "surname": "mif",
        "university": "havdkh", "degree": "jqaqdm", "level": "1", "year": "2", "password": "myPass@343"})

    assert response.status_code == 400
    assert response.json()["detail"] == "Email already exists."


async def test_login_successful(client):
    await client.post("/user/register", json={"username": "mariamissnf",
        "email": "mariamissnf@gmail.com", "name": "maria", "surname": "missnf",
        "university": "sinclarr", "degree": "nursing", "level": "2", "year": "1", "password": "myPass@343"})

    response = await client.post("/user/login", data={"username": "mariamissnf", "password": "myPass@343"})

    assert response.status_code == 200
    assert "access_token" in response.json()


async def test_login_wrong_password(client):
    await client.post("/user/register", json={"username": "mariamissnf",
            "email": "mariamissnf@gmail.com", "name": "maria", "surname": "missnf",
            "university": "sinclarr", "degree": "nursing", "level": "2", "year": "1", "password": "myPass@343"})
    
    response = await client.post("/user/login", data={"username": "mariamissnf", "password": "passGb#476"})

    assert response.status_code == 401


async def test_login_unknown_user(client):
    response = await client.post("/user/login", data={"username": "whoisThat", "password": "passGb#476"})
    assert response.status_code == 401


async def test_get_user_authenticated(client, auth_headers):
    response = await client.get("/user/me", headers=auth_headers)
    assert response.status_code == 200
    assert "password_hash" not in response.json()


async def test_get_user_no_token(client):
    response = await client.get("/user/me")
    assert response.status_code == 401


async def test_update_account(client, auth_headers):
    response = await client.put("/user/search/1", json={"name": "newww"}, headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["name"] == "newww"


async def test_update_no_token(client):
    repsonse = await client.put("/user/search/1", json={"name": "newww"})
    assert repsonse.status_code == 401


async def test_delete_account(client, auth_headers):
    response = await client.delete("/user/delete/", params={"user_id": 1}, headers=auth_headers)
    assert response.status_code in (200, 204)
    response = await client.post("/user/login", data={"username": "mariamissnf", "password": "myPass@343"})
    assert response.status_code == 401


async def test_delete_no_token(client):
    response = await client.delete("/user/delete/", params={"user_id": 1})
    assert response.status_code == 401


async def test_filter_users_degree(client):
    await client.post("/user/register", json={"username": "gabrielahwfh",
                        "email": "gabrielajsjs@gmail.com", "name": "gabi", "surname": "jsjs",
                        "university": "sinclarr", "degree": "nursing", "level": "2", "year": "1", "password": "myPass@6767"})

    await client.post("/user/register", json={"username": "tinamaarn",
                            "email": "tinamaarn@gmail.com", "name": "tina", "surname": "marn",
                            "university": "hohohoho", "degree": "nursing", "level": "2", "year": "2", "password": "myPass@6767"})

    response = await client.get("/user/filter/users", params={"degree": "nursing"})
    usernames = {u["username"] for u in response.json()}
    
    assert "gabrielahwfh" in usernames
    assert "tinamaarn" in usernames
    assert response.status_code == 200
    assert len(response.json()) >= 2

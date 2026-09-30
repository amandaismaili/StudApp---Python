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
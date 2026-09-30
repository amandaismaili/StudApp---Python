async def test_register(client):
    response = await client.post("/user/register", json={"username": "mariamissnf",
        "email": "mariamissnf@gmail.com", "name": "maria", "surname": "missnf",
        "university": "sinclarr", "degree": "nursing", "level": "2", "year": "1", "password": "myPass@343"})

    print(response.json())
    assert response.status_code == 200
    assert response.json()["username"] == "mariamissnf"
    assert "password" not in response.json()
    assert "password_hash" not in response.json()
async def test_section(client):
    response = await client.get("/section")
    assert response.status_code == 200
    assert response.json() == []


async def test_make_question(client, auth_headers):
    response = await client.post("/section/questions", json={"title": "y i have oo", "text": "rjfcurivrf87uhnvdc"}, headers=auth_headers)
    
    assert response.status_code == 201
    assert response.json()["title"] == "y i have oo"
    assert response.json()["author"]["username"] == "mariamissnf"


async def test_replying(client, auth_headers):
    ques_response = await client.post("/section/questions", json={"title": "y i have oo", "text": "rjfcurivrf87uhnvdc"}, headers=auth_headers)
    ques_id = ques_response.json()["id"]
    
    response = await client.post(f"/section/{ques_id}/reply", json={"text": "so idk but hey uoo yo"}, headers=auth_headers)

    assert response.status_code == 201
    assert response.json()["text"] == "so idk but hey uoo yo"
    assert response.json()["author"]["username"] == "mariamissnf"


async def test_reply_to_nonexistent_question(client, auth_headers):
    response = await client.post("/section/99999/reply", json={"text": "hi"}, headers=auth_headers)
    assert response.status_code == 404


async def test_search_question(client, auth_headers):
    ques_response = await client.post("/section/questions", json={"title": "y i have oo", "text": "rjfcurivrf87uhnvdc"}, headers=auth_headers)
    ques_id = ques_response.json()["id"]

    response = await client.get(f"/section/search/{ques_id}")

    assert response.status_code == 200
    assert response.json()["author"]["username"] == "mariamissnf"


async def test_search_nonexistent_question(client):
    response = await client.get("/section/search/6959")

    assert response.status_code == 404


async def test_delete_question(client, auth_headers):
    ques_response = await client.post("/section/questions", json={"title": "y i have oo", "text": "rjfcurivrf87uhnvdc"}, headers=auth_headers)
    ques_id = ques_response.json()["id"]

    response = await client.delete(f"/section/delete/question/{ques_id}", headers=auth_headers)
    assert response.status_code == 204

    search_response = await client.get(f"/section/search/{ques_id}")
    assert search_response.status_code == 404


async def test_delete_question_no_token(client):
    response = await client.delete("/section/delete/question/7777")
    assert response.status_code == 401


async def test_delete_someones_ques(client, auth_headers):
    ques_response = await client.post("/section/questions", json={"title": "y i have oo", "text": "rjfcurivrf87uhnvdc"}, headers=auth_headers)
    ques_id = ques_response.json()["id"]
    
    await client.post("/user/register", json={"username": "gabrielahwfh",
                "email": "gabrielajsjs@gmail.com", "name": "gabi", "surname": "jsjs",
                "university": "sinclarr", "degree": "nursing", "level": "2", "year": "1", "password": "myPass@6767"})
    login_response = await client.post(
        "/user/login",
        data={"username": "gabrielahwfh", "password": "myPass@6767"}
    )
    gabi_token = login_response.json()["access_token"]
    gabi_headers = {"Authorization": f"Bearer {gabi_token}"}
    
    response = await client.delete(f"/section/delete/question/{ques_id}", headers=gabi_headers)
    assert response.status_code == 403


async def test_delete_reply(client, auth_headers):
    ques_response = await client.post("/section/questions", json={"title": "y i have oo", "text": "rjfcurivrf87uhnvdc"}, headers=auth_headers)
    ques_id = ques_response.json()["id"]

    reply_response = await client.post(f"/section/{ques_id}/reply", json={"text": "so idk but hey uoo yo"}, headers=auth_headers)
    reply_id = reply_response.json()["id"]
    
    response = await client.delete(f"/section/delete/reply/{reply_id}", headers=auth_headers)
    assert response.status_code == 204

    
async def test_delete_reply_no_token(client):
    response = await client.delete("/section/delete/reply/9999")
    assert response.status_code == 401


async def test_delete_someones_reply(client, auth_headers):
    ques_response = await client.post("/section/questions", json={"title": "y i have oo", "text": "rjfcurivrf87uhnvdc"}, headers=auth_headers)
    ques_id = ques_response.json()["id"]
    
    reply_response = await client.post(f"/section/{ques_id}/reply", json={"text": "so idk but hey uoo yo"}, headers=auth_headers)
    reply_id = reply_response.json()["id"]

    await client.post("/user/register", json={"username": "gabrielahwfh",
                "email": "gabrielajsjs@gmail.com", "name": "gabi", "surname": "jsjs",
                "university": "sinclarr", "degree": "nursing", "level": "2", "year": "1", "password": "myPass@6767"})
    login_response = await client.post(
            "/user/login",
            data={"username": "gabrielahwfh", "password": "myPass@6767"}
        )
    gabi_token = login_response.json()["access_token"]
    gabi_headers = {"Authorization": f"Bearer {gabi_token}"}

    response = await client.delete(f"/section/delete/reply/{reply_id}", headers=gabi_headers)
    assert response.status_code == 403
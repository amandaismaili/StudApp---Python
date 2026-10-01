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



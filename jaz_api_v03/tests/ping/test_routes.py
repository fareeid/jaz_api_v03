import json

from fastapi.encoders import jsonable_encoder

from ...src.ping import routes as ping_routes


def test_pong_env(test_app):
    response = test_app.get("/ping/env")
    # print(response.json())
    assert response.status_code == 200
    # assert response.json() == {
    #   "ping_env": "pong_env",
    #   "POSTGRES_DB": "web_test",
    #   # "environment": "postgresql+asyncpg://postgres:changethis@db:5432/web_test",
    #   "environment": "postgresql+asyncpg://postgres:changethis@localhost:5432/web_test",
    # }


def test_create_person(test_app):
    person = ping_routes.test_data()
    person_json = json.dumps(jsonable_encoder(person.model_dump(exclude_unset=True)))
    response = test_app.post("/ping/create_person", content=person_json)
    # print(response)
    assert response.status_code == 200
    # assert response.json() == {"ping": "pong", "TESTING": 0}
    # assert True

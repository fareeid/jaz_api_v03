import json

from fastapi.encoders import jsonable_encoder

from ...src.quotes.sample_data import sample_quotes


def test_quote(test_app):
    quote = sample_quotes.create_quote()
    quote_json = json.dumps(jsonable_encoder(quote.model_dump(exclude_unset=True)))
    response = test_app.post("/quotes/quote", content=quote_json)
    # print(response)
    assert response.status_code == 200
    # assert response.json() == {"ping": "pong", "TESTING": 0}
    # assert True


def test_dyn_marine_payload(test_app):
    dyn_marine_payload = json.dumps(sample_quotes.create_dyn_marine_payload())
    response = test_app.post("/quotes/dyn_marine_payload", content=dyn_marine_payload)
    # print(response.status_code)
    assert response.status_code == 200
    # assert response.json() == {"ping": "pong", "TESTING": 0}s

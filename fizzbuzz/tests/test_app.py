import json
import pytest

from api.app import create_app
from api.database import add_instance
from api.models import FizzBuzz


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://"

    with app.test_client() as client:
        with app.app_context():
            add_instance(FizzBuzz, int1=5, int2=10, limit=20, str1="thanks", str2="gracias")
            add_instance(FizzBuzz, int1=4, int2=12, limit=30, str1="hello", str2="hola", nb_hit=2)
            yield client


def test_fizzbuzz_nominal(client):

    body = {
        "int1": 3,
        "int2": 15,
        "limit": 30,
        "str1": "test1",
        "str2": "test2"
    }
    headers = {'content-type': 'application/json'}
    response = client.get("/fizzbuzz", headers=headers, data=json.dumps(body))
    data = json.loads(response.get_data())

    expected = [1, 2, "test1", 4, 5, "test1", 7, 8, "test1", 10, 11, "test1", 13,
                14, "test1test2", 16, 17, "test1", 19, 20, "test1", 22, 23,
                "test1", 25, 26, "test1", 28, 29, "test1test2"]

    assert FizzBuzz.query.count() == 3
    assert data == expected
    assert response.status_code == 200


def test_fizzbuzz_new_hit(client):
    body = {
        "int1": 5,
        "int2": 10,
        "limit": 20,
        "str1": "thanks",
        "str2": "gracias"
    }
    headers = {'content-type': 'application/json'}
    response = client.get("/fizzbuzz", headers=headers, data=json.dumps(body))
    data = json.loads(response.get_data())

    print(FizzBuzz.query.first().nb_hit)

    expected = [1, 2, 3, 4, 'thanks', 6, 7, 8, 9, 'thanksgracias', 11, 12, 13,
                14, 'thanks', 16, 17, 18, 19, 'thanksgracias']

    fizzbuzz = FizzBuzz.query.filter_by(int1=5, int2=10, limit=20, str1="thanks",
                                        str2="gracias").first()

    assert fizzbuzz.nb_hit == 2
    assert data == expected
    assert response.status_code == 200


def test_fizzbuzz_missing_parameter(client):

    body = {
        "int2": 15,
        "limit": 30,
        "str1": "test1",
        "str2": "test2"
    }
    headers = {'content-type': 'application/json'}
    response = client.get("/fizzbuzz", headers=headers, data=json.dumps(body))

    data = json.loads(response.get_data())
    assert data == {"error": "Missing parameters for fizz buzz"}
    assert response.status_code == 400


def test_fizzbuzz_invalid_type_parameter(client):

    body = {
        "int1": "invalid type",
        "int2": 15,
        "limit": 30,
        "str1": "test1",
        "str2": "test2",
    }
    headers = {'content-type': 'application/json'}
    response = client.get("/fizzbuzz", headers=headers, data=json.dumps(body))

    data = json.loads(response.get_data())
    assert data == {"error": "Invalid type of parameters for fizz buzz"}
    assert response.status_code == 400


def test_statistics_nominal(client):

    response = client.get("/statistics")
    # data = json.loads(response.get_data())
    data = response.get_data()
    print("data", data)
    print(FizzBuzz.query.all())

    expected = {'int1': 4, 'int2': 12, 'limit': 30, 'str1': 'hello', 'str2': 'hola', 'nb_hit': 2}

    assert data == expected
    assert response.status_code == 200

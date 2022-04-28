
import json
from flask_testing import TestCase
from api.app import create_app
from api.database import add_instance, db
from api.models import FizzBuzz


class TestApi(TestCase):

    SQLALCHEMY_DATABASE_URI = "sqlite://"
    TESTING = True

    def create_app(self):
        return create_app()

    def setUp(self):
        with self.app.app_context():
            db.create_all()
            add_instance(FizzBuzz, int1=5, int2=10, limit=20, str1="thanks", str2="gracias")
            add_instance(FizzBuzz, int1=4, int2=12, limit=30, str1="hello", str2="hola", nb_hit=2)

    def tearDown(self):
        db.session.remove()
        with self.app.app_context():
            db.drop_all()

    def test_fizzbuzz_nominal(self):
        body = {
            "int1": 3,
            "int2": 15,
            "limit": 30,
            "str1": "test1",
            "str2": "test2"
        }
        headers = {'content-type': 'application/json'}
        response = self.client.get("/fizzbuzz", headers=headers, data=json.dumps(body))

        data = json.loads(response.get_data())
        expected = [1, 2, "test1", 4, 5, "test1", 7, 8, "test1", 10, 11, "test1", 13,
                    14, "test1test2", 16, 17, "test1", 19, 20, "test1", 22, 23,
                    "test1", 25, 26, "test1", 28, 29, "test1test2"]

        assert FizzBuzz.query.count() == 3
        assert data == expected
        assert response.status_code == 200

    def test_fizzbuzz_new_hit(self):
        body = {
            "int1": 5,
            "int2": 10,
            "limit": 20,
            "str1": "thanks",
            "str2": "gracias"
        }
        headers = {'content-type': 'application/json'}
        response = self.client.get("/fizzbuzz", headers=headers, data=json.dumps(body))
        data = json.loads(response.get_data())

        expected = [1, 2, 3, 4, 'thanks', 6, 7, 8, 9, 'thanksgracias', 11, 12, 13,
                    14, 'thanks', 16, 17, 18, 19, 'thanksgracias']

        fizzbuzz = FizzBuzz.query.filter_by(int1=5, int2=10, limit=20, str1="thanks",
                                            str2="gracias").first()

        assert fizzbuzz.nb_hit == 2
        assert data == expected
        assert response.status_code == 200

    def test_fizzbuzz_missing_parameter(self):

        body = {
            "int2": 15,
            "limit": 30,
            "str1": "test1",
            "str2": "test2"
        }
        headers = {'content-type': 'application/json'}
        response = self.client.get("/fizzbuzz", headers=headers, data=json.dumps(body))

        data = json.loads(response.get_data())
        assert data == {"error": "Missing parameters for fizz buzz"}
        assert response.status_code == 400

    def test_fizzbuzz_invalid_type_parameter(self):

        body = {
            "int1": "invalid type",
            "int2": 15,
            "limit": 30,
            "str1": "test1",
            "str2": "test2",
        }
        headers = {'content-type': 'application/json'}
        response = self.client.get("/fizzbuzz", headers=headers, data=json.dumps(body))

        data = json.loads(response.get_data())
        assert data == {"error": "Invalid type of parameters for fizz buzz"}
        assert response.status_code == 400

    def test_statistics_nominal(self):

        response = self.client.get("/statistics")
        data = json.loads(response.get_data())

        expected = {'int1': 4, 'int2': 12, 'limit': 30, 'str1': 'hello',
                    'str2': 'hola', 'nb_hit': 2}

        assert data == expected
        assert response.status_code == 200

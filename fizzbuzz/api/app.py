import json
import os
from typing import List

from flask import Flask, request

from database import add_instance, commit_changes, get_instance
from models import FizzBuzz, db
from utils import get_fizzbuzz


def create_app():
    flask_app = Flask(__name__)
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL", "sqlite://")
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    flask_app.app_context().push()
    db.init_app(flask_app)
    db.create_all()

    return flask_app


app = create_app()


@app.route("/fizz-buzz", methods=['GET'])
def fizzbuzz() -> List[str]:
    """Compute fizzbuzz with the given request parameters, then increment number
    of hits for the request or create instance in database if not created yet

    Returns
    -------
    List[str]
        List of numbers from 1 to limit, where some of them were replaced by str1, str2 or str1str2
    """
    data_request = request.get_json()

    # Check of the presence of all the parameters we need
    if not all(key in data_request for key in ('int1', 'int2', 'limit', 'str1', 'str2')):
        return "Missing parameters for fizz buzz", 400

    int1 = data_request["int1"]
    int2 = data_request["int2"]
    limit = data_request["limit"]
    str1 = data_request["str1"]
    str2 = data_request["str2"]

    # Check the type validity of the parameters
    if (not all(isinstance(i, int) for i in [int1, int2, limit])
       or not all(isinstance(i, str) for i in [str1, str2])):
        return "Invalid type of parameters for fizz buzz", 400

    fizzbuzz = get_fizzbuzz(int1, int2, limit, str1, str2)
    fizzbuzz_instance = get_instance(FizzBuzz, int1=int1, int2=int2, limit=limit,
                                     str1=str1, str2=str2)

    if not fizzbuzz_instance:
        add_instance(FizzBuzz, int1=int1, int2=int2, limit=limit, str1=str1, str2=str2)
    else:
        fizzbuzz_instance.nb_hit += 1
        commit_changes()

    return json.dumps(fizzbuzz), 200


@app.route("/statistics", methods=['GET'])
def get_stat_request():
    most_requested = FizzBuzz.query.order_by(FizzBuzz.nb_hit.desc()).first()

    if not most_requested:
        return "No fizz buzz registred", 404

    body = {
        "int1": most_requested.int1,
        "int2": most_requested.int2,
        "limit": most_requested.limit,
        "str1": most_requested.str1,
        "str2": most_requested.str2,
        "nb_hit": most_requested.nb_hit
    }

    return json.dumps(body), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)

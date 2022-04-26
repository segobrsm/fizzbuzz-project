import json
from typing import List

from flask import request
from sqlalchemy.sql import func

from models import FizzBuzz, db

from app import create_app

app = create_app()


@app.route('/')
def hello():
    return 'Coucou !'


@app.route("/fizz-buzz", methods=['GET'])
def fizz_buzz() -> List[str]:
    """Compute fizz buzz

    Returns
    -------
    List[str]
        _description_
    """
    data_request = request.get_json()

    if not all(key in data_request for key in ('int1', 'int2', 'limit', 'str1', 'str2')):
        return "Missing parameters for fizz buzz", 400

    int1 = data_request["int1"]
    int2 = data_request["int2"]
    limit = data_request["limit"]
    str1 = data_request["str1"]
    str2 = data_request["str2"]

    result = []
    for i in range(1, limit):
        if i % int1 == 0 and i % int2 == 0:
            result.append(str1 + str2)
        elif i % int1 == 0:
            result.append(str1)
        elif i % int2 == 0:
            result.append(str2)
        else:
            result.append(i)

    new_fizzbuzz = FizzBuzz.query.filter_by(int1=int1, int2=int2, limit=limit,
                                            str1=str1, str2=str2).first()
    if not new_fizzbuzz:
        # faire une fonction create_instance dans autre fichier
        new_fizzbuzz = FizzBuzz.query.filter_by(int1=int1, int2=int2, limit=limit,
                                                str1=str1, str2=str2).first()
        db.session.add(new_fizzbuzz)
        db.session.commit()

    else:
        new_fizzbuzz.nb_hit += 1
        db.session.commit()

    return json.dumps(result), 200


@app.route("/statistics", methods=['GET'])
def get_stat_request():
    most_requested = FizzBuzz.query.filter_by(func.max(FizzBuzz.nb_hit)).first()
    if not most_requested:
        return "No fizz buzz registred", 404

    return list(most_requested.int1, most_requested.int2, most_requested.limit,
                most_requested.str1, most_requested.str2, most_requested.nb_hit), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)

import json
from typing import Dict, List

from flask import Blueprint, request

from api.database import add_instance, commit_changes, get_instance
from api.models import FizzBuzz
from api.utils import get_fizzbuzz

bp = Blueprint("app", __name__)


@bp.route("/fizzbuzz", methods=['GET'])
def fizzbuzz() -> Dict[str, List[str]]:
    """Compute fizzbuzz with the given request parameters, then increment number
    of hits for the request or create instance in database if not created yet

    Returns
    -------
    Dict[str, List[str]]
        List of numbers from 1 to limit, where some of them were replaced by str1, str2 or str1str2
    """
    data_request = request.get_json()

    # Check of the presence of all the parameters we need
    if not all(key in data_request for key in ('int1', 'int2', 'limit', 'str1', 'str2')):
        return json.dumps({"error": "Missing parameters for fizz buzz"}), 400

    int1 = data_request["int1"]
    int2 = data_request["int2"]
    limit = data_request["limit"]
    str1 = data_request["str1"]
    str2 = data_request["str2"]

    # Check the type validity of the parameters
    if (not all(isinstance(i, int) for i in [int1, int2, limit])
       or not all(isinstance(i, str) for i in [str1, str2])):
        return json.dumps({"error": "Invalid type of parameters for fizz buzz"}), 400

    fizzbuzz = get_fizzbuzz(int1, int2, limit, str1, str2)
    fizzbuzz_instance = get_instance(FizzBuzz, int1=int1, int2=int2, limit=limit,
                                     str1=str1, str2=str2)

    if not fizzbuzz_instance:
        add_instance(FizzBuzz, int1=int1, int2=int2, limit=limit, str1=str1, str2=str2)
    else:
        fizzbuzz_instance.nb_hit += 1
        commit_changes()

    return json.dumps({"result": fizzbuzz}), 200


@bp.route("/statistics", methods=['GET'])
def get_stat_request() -> Dict[str, str]:
    """Find the fizzbuzz with the highest nb_hit in the database

    Returns
    -------
    Dict[str, str]
        The parameters of the most requested fizzbuzz
    """
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

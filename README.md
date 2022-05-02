# Fizz-buzz REST server

This is a Fizzbuzz web server that expose two endpoints. After starting the application you can access following URL's on the server:
 : 

| URL | Behavior | Call example |  |
|---|---|---|---|
| `http://<server>:<port>/fizzbuzz/` | returns the fizzbuzz string list with numbers from 1 to limit, where: all multiples of int1 are replaced by str1, all multiples of int2 are replaced by str2, all multiples of int1 and int2 are replaced by str1str2. | `curl -X GET -H "Content-Type: application/json" -d '{"int1": 3, "int2": 15, "limit": 50, "str1": "hello", "str2":"hola"}' http://127.0.0.1:5000/fizzbuzz` |  |
| `http:// <server> : <port> /statistics/` |  | `curl -X GET -H "Content-Type: application/json" http://127.0.0.1:5000/statistics` |  |
|  |  |  |  |

## How to run the application

You can run the application in 2 ways:

### With Docker

Requirements:
* [Docker](https://docs.docker.com/desktop/) installed
* [Docker Compose](https://docs.docker.com/compose/install/) installed

<ol>
    <li>
        Build the database and the app images with docker-compose
        - Development environment :  `docker-compose -f docker-compose.yml build`
        - Production environment : `docker-compose -f docker-compose.prod.yml build`
    </li>
    <li>
        Run the app with docker-compose
        - Development environment :  `docker-compose -f docker-compose.yml up`
        - Production environment : `docker-compose -f docker-compose.prod.yml up`
    </li>
    <li>
        Stop the running app:
        `docker-compose stop`
    </li>
</ol>


### From source

<ol>
    <li>
        Install requirements
        `pip install requirements.txt`       
    </li>
    <li>
        Launch app
        `cd fizzbuzz`
        `python manage.py`
    </li>
</ol>

## Development

### Virtual environment

For local development you can use a virtual environment.

Create a virtual environment:

```
# Linux example
python -m venv "venv"
source venv/bin/activate
```

With `deactivate` you can disable the virtual environment.

### Testing
To run tests : 
```
cd fizzbuzz
pip install pytest
pytest
```
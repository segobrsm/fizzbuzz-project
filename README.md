# Fizz-buzz REST server

This is a Fizzbuzz web server that expose two endpoints. After starting the application you can access following URL's on the server:
 : 

| URL | Response | Call example |
|---|---|---|
| `http://<server>:<port>/fizzbuzz/` | The fizzbuzz string list with numbers from 1 to limit, where: <br>- all multiples of int1 are replaced by str1<br>- all multiples of int2 are replaced by str2<br>- all multiples of int1 and int2 are replaced by str1str2 | `curl -X GET -H "Content-Type: application/json" -d '{"int1": 3, "int2": 15, "limit": 50, "str1": "hello", "str2":"hola"}' http://127.0.0.1:5000/fizzbuzz` |
| `http://<server>:<port>/statistics/` | The parameters corresponding to the most used request, as well as the number of hits for this request | `curl -X GET -H "Content-Type: application/json" http://127.0.0.1:5000/statistics` |
| `http://<server>:<port>/swagger/` | Documentation about Fizzbuzz web server | `curl -X GET -H "Content-Type: application/json" <br>http://127.0.0.1:5000/swagger` |


## How to run the application

You can run the application in 2 ways:

### With Docker

Requirements:
* [Docker](https://docs.docker.com/desktop/) installed
* [Docker Compose](https://docs.docker.com/compose/install/) installed

1. Build the database and the app images with docker-compose
- Development environment:  `docker-compose -f docker-compose.yml build`
- Production environment: `docker-compose -f docker-compose.prod.yml build`

 2. Run the app with docker-compose
- Development environment: `docker-compose -f docker-compose.yml up`
- Production environment: `docker-compose -f docker-compose.prod.yml up`

3. Stop the running app: `docker-compose stop`

### From source
1. Install requirements: `pip install requirements.txt`       
2. Launch app:
  ```
   cd fizzbuzz
   python manage.py
  ```

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
To run tests: 
```
cd fizzbuzz
pip install pytest
pytest
```

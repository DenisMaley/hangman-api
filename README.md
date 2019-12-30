# Hangman API

 > This is a simple hangman game API

## What is this project about?

This is the implementation of the API for the Hangman game.

The Stack: Python (Flask-RESTful), JWT (Flask-JWT-Extended), MongoDB (Mongoengine), Swagger (Flasgger)

## Requirements

To build this project you will need [Docker][Docker Install] and [Docker Compose][Docker Compose Install].

## Deploy and Run

After cloning this repository, type the following commands to start the app:

```sh
docker-compose build && docker-compose up
```
or run containers in the background:

```sh
docker-compose build && docker-compose up -d
```

Then visit [status endpoint][AppStatus] to check the status.
If you see 
 
 ```json
{
    "status": "OK"
}
```
 
it means that everything went well

To stop the app containers without removing them after you finished to work with the app:

```sh
docker-compose stop
```

To stop the app containers and removes containers, networks, volumes, and images:

```sh
docker-compose down
```

## Usage

Check Swagger UI [documentation][Swagger] to know how to use the API

E.g. to register a user run 

```sh
curl -d '{"username":"test", "password":"test"}' -H "Content-Type: application/json" -X POST http://localhost:5000/api/registration
```

or use Postman:

![Postman screenshot](https://i.gyazo.com/0d2b08ad60d9d7e992fc481f1133a2ec.png)

For the main endpoints use `access_token` as Bearer token for authorization:

![Postman screenshot](https://i.gyazo.com/98ab3dbe0cb2606934297a1aa60e363a.png)

## Tests
To run all tests
```bash
docker-compose run app python -W ignore:docker-compose run app python -W ignore:DeprecationWarning -m unittest discover -s tests -m unittest discover -s tests
```

## Client setup

> To set up client for the API check this [repo][Client].

## To do

The project is not completely finished.

Check for `# TODO` in you IDE

General ideas:

* Implement unit tests for the remaining classes
* Improve flow and catching exceptions, current implementation for ideal users
* Improve documentation, now it is not completed
* Implement request validation with [json-schema][JSONSchema] with [Fast JSON Schema][FastJSONSchema]

[Docker Install]:  https://docs.docker.com/install/
[Docker Compose Install]: https://docs.docker.com/compose/install/
[AppStatus]: http://localhost:5000/api/status
[Swagger]: http://localhost:5000/apidocs/
[JSONSchema]: https://json-schema.org/
[FastJSONSchema]: https://horejsek.github.io/python-fastjsonschema/
[Client]: https://github.com/DenisMaley/triplanner-vue-client
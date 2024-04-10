# toDoApp-fastAPI

This API is written with FastAPI and Python for a ToDo app.

## Prerequisites

Before to start, please note this app is built with Python 3.10 in mind. Please mind that using previous version might create issues on your development experience.

### Install the virtual environment

If it is the first time you start the application on your machine, remember to set up a virtual machine:

```shell
python3.exe -m venv venv
```

Then activate with the following for Windows:

```shell
venv\Scripts\activate
```

or Linux:

```shell
source venv/scripts/activate
```

Then install dependencies:

```shell
pip install -r requirements.txt
```

### Environment variables

Environment variables included in the `.env` file will be used inside the application. This file is excluded from source control, so you want to create it in the root folder (at the same level as `main.py`), with the same structure as `default.env`.

You can also locally use a `local.env` file, as an alternative to `.env`. It is also excluded from git.

The list of necessary environment variables is the following:

* **DEBUG**: whether FastAPI should start in debug mode or not
  * default: _false_
* **LOG_LEVEL**: from which level log will be printed out
  * default: _INFO_
  * possible values: _NOTSET_, _DEBUG_, _INFO_, _WARNING_, _ERROR_, _CRITICAL_
* **MONGO_URL** (_mandatory_): the path of the Mongo database to connect with, containing host and port;
* **DATABASE_NAME** (_mandatory_): the name of the MongoDB database;
* **HASH_KEY** (_mandatory_): this is a 32 letter hash that will be used to hash passwords (e.g. via Linux, you can generate it typing `openssl rand -hex 32` on a terminal)

## How to run

You can start the application with the following:

```shell
uvicorn main:app --reload
```

It will be exposed at `http://localhost:8000``

# How to test

Every test should be included in the `tests` folder. We use `Pytest` to run tests. Simply launch

```shell
pytest
```

to let the magic happen.

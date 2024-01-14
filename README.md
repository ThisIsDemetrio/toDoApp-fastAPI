# toDoApp-fastAPI

Backend written with FastAPI and Python for a To Do app.

## Prerequisites

### Install the virtual environment

If it is the first time you start the application on your machine, remember to set up a virtual machine:
```
python3.exe -m venv venv
```

Then activating with the following for Windows:
```
venv\Scripts\activate
```
or Linux:
```
source venv/scripts/activate
```

Then install dependencies:
```
pip install -r requirements.txt
```

### Environment variables

Environment variables included in the `.env` file will be used inside the application. This file is excluded from source control, so you want to create it at root folder (at the same level of `main.py`), with the same structure of `default.env`.

You can also locally use a `local.env` file, as an alternative of `.env`. It is also excluded from git.

The list of necessary environment variables are the following:
* **MONGO_URL** (_mandatory_): the path of the Mongo database to connect with, containing host and port;

## How to run

You can start the application with the following:
```
uvicorn main:app --reload
```

It will be exposed in `http://localhost:8000`

# How to test

Every test should be included inside the `tests` folder. We use `Pytest` to run tests. Simply launch
```
pytest
```

to let the magic happen.
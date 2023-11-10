## Setup
1. Install poetry:
```bash
curl -sSL https://install.python-poetry.org | python3 -
```
https://python-poetry.org/docs/

Remember to add poetry to your path

2. Install dependencies:
```bash
poetry install
```

3. Run the server:
```bash
poetry run flask run
```
If you want to run the server in debug mode, run:
```bash
poetry run flask run --debug
```

4. Initialize the database:
First time you run the server, you need to initialize the database. To do that, run:
```bash
poetry run flask shell
```
```python
>>> db.create_all()
```

If you want to drop all tables, run:
```bash
poetry run flask shell
```
```python
>>> db.drop_all()
```

5. Populate the database:
To populate the database, run:
```bash
poetry run python populate_db.py
```

This file can be modified to change the data that will be inserted in the database.

Also, you can send requests to the server to populate the database manually.
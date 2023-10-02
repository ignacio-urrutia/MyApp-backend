# MyApp
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

## Endpoints

### User Endpoints

#### 1. **GET** `/users`

- Returns a list of all users.
  
#### 2. **POST** `/users`

- Creates a new user.
- **Body Parameters:**
  - `name`: string (required)
  - `email`: string (required)
  - `last_latitude`: float (optional)
  - `last_longitude`: float (optional)

#### 3. **GET** `/users/<int:user_id>`

- Retrieves information about a specific user by user ID.
  
#### 4. **PATCH** `/users/<int:user_id>`

- Updates information for a specific user by user ID.
- **Body Parameters:**
  - `name`: string (optional)
  - `email`: string (optional)
  - `last_latitude`: float (optional)
  - `last_longitude`: float (optional)

#### 5. **DELETE** `/users/<int:user_id>`

- Deletes a specific user by user ID.

#### 6. **POST** `/users/login`

- Logs in a user.
- **Body Parameters:**
  - `email`: string (required)
  - `password`: string (required)

### Group Chat Endpoints

#### 1. **GET** `/groupchats`

- Returns a list of all group chats.
  
#### 2. **POST** `/groupchats`

- Creates a new group chat.
- **Body Parameters:**
  - `name`: string (required)
  - `north_boundary`: float (required)
  - `south_boundary`: float (required)
  - `east_boundary`: float (required)
  - `west_boundary`: float (required)
  - `description`: string (optional)
  - `owner_id`: integer (required)

#### 3. **GET** `/groupchats/<int:group_chat_id>`

- Retrieves information about a specific group chat by group chat ID.

#### 4. **PATCH** `/groupchats/<int:group_chat_id>/adduser`

- Adds a user to a specific group chat by group chat ID.
- **Body Parameters:**
  - `user_id`: integer (required)

## How it will work
1. User send its location
2. Server checks all groups where the user bellong and if the user is inside the group's area, return the information about the group

## Connect to the EC2 instance
1. Connect to the instance:
```bash
ssh -i BackendKeys/area-chat-keys.pem ec2-user@ec2-3-138-178-239.us-east-2.compute.amazonaws.com
``` 
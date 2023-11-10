# ChatterMap
This is the backend of the ChatterMap App. It provides a REST API for the frontend to consume. The instance is running a Flask server that is connected to a MySQL database. Also, the backend is connected to a S3 bucket to store multimedia files, mainly profile pictures.

The code is running in a EC2 instance in AWS in the following address: http://18.222.120.14:5000


## Setup
To setup the backend in local, follow the instructions in the [Setup.md](Setup.md) file.


## Endpoints

### Users

#### 1. **GET** `/all-users`
- Returns a list of all users. (For testing purposes only)
  
#### 2. **POST** `/signup`
- Creates a new user.
- **Body Parameters:**
  - `name`: string (required)
  - `email`: string (required)
  - `password`: string (required)

#### 3. **POST** `/users/login`
- Logs in a user.
- **Body Parameters:**
  - `email`: string (required)
  - `password`: string (required)

#### 4. **GET** `/users`
- Gets information about the current user. (Requires authentication)

#### 5. **PATCH** `/users`
- Updates information for the current user. (Requires authentication)
- **Body Parameters:**
  - `name`: string (optional)
  - `email`: string (optional)
  - `password`: string (optional)
  - `last_latitude`: float (optional)
  - `last_longitude`: float (optional)
  - `battery_level`: float (optional)

#### 6. **DELETE** `/users`
- Deletes the current user. (Requires authentication)

#### 7. **GET** `/users/chatrooms`
- Gets a list of all chatrooms the current user is in. (Requires authentication)

#### 8. **GET** `/friends`
- Gets a list of all friends of the current user. (Requires authentication)

#### 8. **DELETE** `/friends`
- Deletes a friend of the current user and removes the current user from the friend's friend list. (Requires authentication)
- **Body Parameters:**
  - `friend_id`: integer (required)

#### 9. **GET** `/users/update-chatrooms`
- Sends signal to update chatrooms of the current user based on their location. (Requires authentication)
- Returns a list of chatrooms available to the user.

#### 10. **GET** `/profile-picture/<int:user_id>`
- Retrieves the profile picture of a specific user by user ID. 

#### 11. **POST** `/update-profile-picture`
- Updates the profile picture of the current user. (Requires authentication)
- **Body Parameters:**
  - `file`: new profile picture (required)

  
### Friend Requests

#### 1. **GET** `/friend-requests`
- Gets a list of all friend requests of the current user. (Requires authentication)

#### 2. **POST** `/friend-requests`
- Sends a friend request to a user. (Requires authentication)
- **Body Parameters:**
  - `receiver_id`: integer (required)

#### 3. **PUT** `/friend-requests`
- Accepts or rejects a friend request. (Requires authentication)
- **Body Parameters:**
  - `request_id`: integer (required)
  - `status`: string (required) (must be either "accepted" or "declined")

### Group Chats (Chatrooms)

#### 1. **GET** `/groupchats/`
- Gets a list of all group chats. (For testing purposes only)

#### 2. **POST** `/groupchats/`

- Creates a new group chat. 
- **Body Parameters:**
  - `name`: string (required)
  - `owner_id`: integer (required)
  - `description`: string (required)
  - `latitude`: float (required)
  - `longitude`: float (required)
  - `radius`: float (required)

#### 3. **GET** `/groupchats/<int:chatroom_id>`
- Gets information about a specific group chat.

#### 4. **PATCH** `/groupchats/<int:chatroom_id>/adduser`
- Adds a user to a specific group chat. (Requires authentication)
- **Body Parameters:**
  - `user_id`: integer (required)

#### 5. **POST** `/groupchats/<int:chatroom_id>/messages`
- Sends a message to a specific group chat. (Requires authentication)
- **Body Parameters:**
  - `user_id`: integer (required, must be the same as the current user)
  - `content`: string (required)

#### 6. **GET** `/groupchats/<int:chatroom_id>/recent-messages`
- Gets the 20 most recent messages of a specific group chat. (Requires authentication)

#### 7. **GET** `/groupchats/<int:chatroom_id>/older-messages/<int:oldest_message_id>`
- Gets the 20 messages older than a specific message of a specific group chat. (Requires authentication)

from flask_restful import fields

message_fields = {
    'id': fields.Integer,
    'content': fields.String,
    'timestamp': fields.DateTime,
    'user_id': fields.Integer,
    'group_chat_id': fields.Integer
}

group_chat_fields = {
    "id": fields.Integer,
    "name": fields.String,
    "users": fields.List(fields.Nested(
        {
            "id": fields.Integer,
            "name": fields.String,
            "email": fields.String,
            "last_latitude": fields.Float,
            "last_longitude": fields.Float
        }
    )),
    "description": fields.String,
    "owner_id": fields.Integer,
    "last_messages": fields.List(fields.Nested(message_fields)),
    "latitude": fields.Float,
    "longitude": fields.Float,
    "radius": fields.Float
}

user_fields = {
    "id": fields.Integer,
    "name": fields.String,
    "email": fields.String,
    "last_latitude": fields.Float,
    "last_longitude": fields.Float,
    "group_chats": fields.List(fields.Nested(group_chat_fields)),
    "friends": fields.List(fields.Nested(
        {
            "id": fields.Integer,
            "name": fields.String,
            "email": fields.String,
            "last_latitude": fields.Float,
            "last_longitude": fields.Float
        }
    )),
    "profile_picture": fields.String
}

token_fields = {
    'token': fields.String,
    'duration': fields.Integer,
    'user_id': fields.Integer
}


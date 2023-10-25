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
    "north_boundary": fields.Float,
    "south_boundary": fields.Float,
    "east_boundary": fields.Float,
    "west_boundary": fields.Float,
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
    "last_messages": fields.List(fields.Nested(message_fields))
}

user_fields = {
    "id": fields.Integer,
    "name": fields.String,
    "email": fields.String,
    "last_latitude": fields.Float,
    "last_longitude": fields.Float,
    "group_chats": fields.List(fields.Nested(group_chat_fields))
}

token_fields = {
    'token': fields.String,
    'duration': fields.Integer,
    'user_id': fields.Integer
}


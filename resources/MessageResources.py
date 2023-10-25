from flask_restful import Resource, reqparse, fields, marshal_with
from models.MessageModel import Message
from application import db
from resourcesFields import message_fields

message_parser = reqparse.RequestParser()
message_parser.add_argument('content', type=str, required=True, help="Message content is required")
message_parser.add_argument('user_id', type=int, required=True, help="User ID is required")
message_parser.add_argument('group_chat_id', type=int, required=True, help="Group Chat ID is required")

class MessageResource(Resource):
    @marshal_with(message_fields)
    def post(self):
        args = message_parser.parse_args()
        message = Message(content=args['content'], user_id=args['user_id'], group_chat_id=args['group_chat_id'])
        db.session.add(message)
        db.session.commit()
        return message, 201

    # ... other methods for getting, updating, deleting messages


from functools import wraps

from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with, request
from flask import g
from flask_httpauth import HTTPBasicAuth
from models.GroupChatModel import GroupChat
from models.UserModel import User
from models.MessageModel import Message
from models.MultimediaModel import Multimedia
from application import db
from .UserResources import auth
from resourcesFields import group_chat_fields, message_fields

group_chat_post_args = reqparse.RequestParser()
group_chat_post_args.add_argument("name", type=str, help="Name required", required=True)
group_chat_post_args.add_argument("north_boundary", type=float, help="North boundary of the group chat required", required=True)
group_chat_post_args.add_argument("south_boundary", type=float, help="South boundary of the group chat required", required=True)
group_chat_post_args.add_argument("east_boundary", type=float, help="East boundary of the group chat required", required=True)
group_chat_post_args.add_argument("west_boundary", type=float, help="West boundary of the group chat required", required=True)
group_chat_post_args.add_argument("description", type=str, help="Description of the group chat required")
group_chat_post_args.add_argument("owner_id", type=int, help="Owner id of the group chat required", required=True)


user_update_args = reqparse.RequestParser()
user_update_args.add_argument("name", type=str, help="Name of the user")
user_update_args.add_argument("north_boundary", type=float, help="North boundary of the group chat")
user_update_args.add_argument("south_boundary", type=float, help="South boundary of the group chat")
user_update_args.add_argument("east_boundary", type=float, help="East boundary of the group chat")
user_update_args.add_argument("west_boundary", type=float, help="West boundary of the group chat")
user_update_args.add_argument("description", type=str, help="Description of the group chat")

add_user_args = reqparse.RequestParser()
add_user_args.add_argument("user_id", type=int, help="User id of the user to add to the group chat", required=True)

# Parser to validate incoming data
message_parser = reqparse.RequestParser()
message_parser.add_argument('content', type=str, required=True, help="Message content is required")
message_parser.add_argument('user_id', type=int, required=True, help="User ID is required")

def user_in_group(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        group_chat_id = kwargs.get('group_chat_id')  # Assumes the group_chat_id is a keyword argument
        group_chat = GroupChat.query.get(group_chat_id)
        if group_chat is None:
            return {"message": "Group chat not found"}, 404
        
        user = g.user
        if user not in group_chat.users:
            return {"message": "You are not a member of this group chat"}, 403

        return f(*args, **kwargs)
    return decorated_function

class GroupChatAll(Resource):
    @marshal_with(group_chat_fields)
    def get(self):
        result = GroupChat.query.all()
        return result
    
    @marshal_with(group_chat_fields)
    def post(self):
        args = group_chat_post_args.parse_args()
        
        owner = User.query.get(args["owner_id"])
        if not owner:
            abort(404, message="Owner user does not exist")

        north_boundary = args["north_boundary"]
        south_boundary = args["south_boundary"]
        east_boundary = args["east_boundary"]
        west_boundary = args["west_boundary"]

        if north_boundary <= south_boundary or east_boundary <= west_boundary:
            abort(400, message="Invalid boundary values")


        group_chat = GroupChat(name=args["name"], owner_id=args["owner_id"], north_boundary=north_boundary, south_boundary=south_boundary, east_boundary=east_boundary, west_boundary=west_boundary, description=args["description"])

        # group_chat.users.append(owner)

        db.session.add(group_chat)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            abort(500, message="Internal Server Error")

        return group_chat, 201

class GroupChatById(Resource):
    @auth.login_required
    @marshal_with(group_chat_fields)
    def get(self, group_chat_id):
        result = GroupChat.query.filter_by(id=group_chat_id).first()
        if not result:
            abort(404, message=f"No group chat with id {group_chat_id}")
        return result
    
    @marshal_with(group_chat_fields)
    def patch(self, group_chat_id): 
        args = add_user_args.parse_args()

        group_chat = GroupChat.query.get(group_chat_id)
        if not group_chat:
            abort(404, message="Group Chat does not exist")

        user = User.query.get(args["user_id"])
        if not user:
            abort(404, message="User does not exist")

        # Check if the user is already in the group chat
        if user in group_chat.users:
            abort(400, message="User is already in the Group Chat")

        group_chat.users.append(user)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            abort(500, message="Internal Server Error")


        return {"message": "User added to the Group Chat"}, 200
    
class GroupChatAddUser(Resource):
    @marshal_with(group_chat_fields)
    def patch(self, group_chat_id):
        args = add_user_args.parse_args()

        group_chat = GroupChat.query.get_or_404(group_chat_id, description="Group chat does not exist")
        user = User.query.get_or_404(args["user_id"], description="User does not exist")

        if user in group_chat.users:
            abort(400, message="User is already in the Group Chat")

        group_chat.users.append(user)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            abort(500, message="Internal Server Error")

        return group_chat, 204

class GroupChatMessages(Resource):
    @auth.login_required
    @marshal_with(message_fields)
    def post(self, group_chat_id):
        user = g.user
        args = message_parser.parse_args()

        # Check if user ID from args matches the logged-in user's ID
        if args['user_id'] != user.id:
            abort(403, message="You can only post messages with your own user ID")

        message = Message(content=args['content'], user_id=user.id, group_chat_id=group_chat_id)
        db.session.add(message)

        # Extract multimedia data from the request
        multimedia_data = request.json.get('multimedia', [])
        for item in multimedia_data:
            multimedia = Multimedia(type=item['type'], file_url=item['file_url'], message=message)
            db.session.add(multimedia)
        
        db.session.commit()
        return message, 201  # 201 status code signifies that a new resource has been created
    
class RecentMessagesResource(Resource):
    @auth.login_required
    @user_in_group
    def get(self, group_chat_id):
        group_chat = GroupChat.query.get(group_chat_id)
        if group_chat is None:
            return {"message": "Group chat not found"}, 404
        # Fetching the last 20 messages
        recent_messages = group_chat.messages[-20:]
        # Preparing a response list
        response = []
        for message in recent_messages:
            # Fetching multimedia items for the current message
            multimedia_items = Multimedia.query.filter_by(message_id=message.id).all()
            # Serializing the message and multimedia data
            message_data = message.serialize()
            message_data['multimedia'] = [item.serialize() for item in multimedia_items]
            response.append(message_data)
        return response, 200

class OlderMessagesResource(Resource):
    @auth.login_required
    @user_in_group
    def get(self, group_chat_id, earliest_message_id):
        earlier_messages = Message.query.filter(
            Message.group_chat_id == group_chat_id,
            Message.id < earliest_message_id
        ).order_by(Message.id.desc()).limit(20).all()
        
        response = []
        for message in earlier_messages:
            multimedia_items = Multimedia.query.filter_by(message_id=message.id).all()
            message_data = message.serialize()
            message_data['multimedia'] = [item.serialize() for item in multimedia_items]
            response.append(message_data)
            
        return response, 200

from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from models.GroupChatModel import GroupChat
from models.UserModel import User
from resources.UserResources import user_fields
from application import db
from .UserResources import auth

group_chat_fields = {
    "id": fields.Integer,
    "name": fields.String,
    "north_boundary": fields.Float,
    "south_boundary": fields.Float,
    "east_boundary": fields.Float,
    "west_boundary": fields.Float,
    "users": fields.List(fields.Nested(user_fields)),
    "description": fields.String,
    "owner_id": fields.Integer
}

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
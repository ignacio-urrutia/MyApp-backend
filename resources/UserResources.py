from flask_restful import Api, Resource, reqparse, abort, marshal_with
from flask import g, request
from flask_httpauth import HTTPBasicAuth

from application import db
from resourcesFields import user_fields, token_fields
from models.GroupChatModel import GroupChat
from models.UserModel import User

auth = HTTPBasicAuth()

user_put_args = reqparse.RequestParser()
user_put_args.add_argument("name", type=str, help="Name required", required=True)
user_put_args.add_argument("email", type=str, help="Email required", required=True)
user_put_args.add_argument("password", type=str, help="Password required", required=True)
user_put_args.add_argument("last_latitude", type=float, help="Last latitude of the user")
user_put_args.add_argument("last_longitude", type=float, help="Last longitude of the user")

user_update_args = reqparse.RequestParser()
user_update_args.add_argument("name", type=str, help="Name of the user")
user_update_args.add_argument("email", type=str, help="Email of the user")
user_update_args.add_argument("last_latitude", type=float, help="Last latitude of the user")
user_update_args.add_argument("last_longitude", type=float, help="Last longitude of the user")
user_update_args.add_argument("password", type=str, help="Password of the user")

user_login_args = reqparse.RequestParser()
user_login_args.add_argument("email", type=str, help="Email of the user", required=True)
user_login_args.add_argument("password", type=str, help="Password of the user", required=True)


class UserAll(Resource):
    @marshal_with(user_fields)
    def get(self):
        result = User.query.all()
        return result, 200

class SignUp(Resource):
    @marshal_with(user_fields)
    def post(self):
        args = user_put_args.parse_args()

        existing_user = User.query.filter_by(email=args['email']).first()
        if existing_user:
            abort(409, message="Whoa there, cowboy! That email already exists.")

        user = User(name=args["name"], email=args["email"])
        user.hash_password(args["password"])
        db.session.add(user)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            abort(500, message="Internal Server Error")

        return user, 201
    
class UserById(Resource):
    @marshal_with(user_fields)
    def get(self, user_id):
        result = User.query.filter_by(id=user_id).first()
        if not result:
            abort(404, message="Could not find user with that id...")
        return result, 200

    @marshal_with(user_fields)
    def patch(self, user_id):
        args = user_update_args.parse_args()
        result = User.query.filter_by(id=user_id).first()
        if not result:
            abort(404, message="User doesn't exist, cannot update...")
        if args["name"]:
            result.name = args["name"]
        if args["email"]:
            result.email = args["email"]
        if args["last_latitude"]:
            result.last_latitude = args["last_latitude"]
        if args["last_longitude"]:
            result.last_longitude = args["last_longitude"]

        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            abort(500, message="Internal Server Error")

        return result, 204
    
    @marshal_with(user_fields)
    def delete(self, user_id):
        result = User.query.filter_by(id=user_id).first()
        if not result:
            abort(404, message="Could not find user with that id...")
        db.session.delete(result)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            abort(500, message="Internal Server Error")

        return result, 204
    
class UserByToken(Resource):
    @marshal_with(user_fields)
    @auth.login_required
    def get(self):
        result = User.query.filter_by(id=g.user.id).first()
        if not result:
            abort(404, message="Could not find user with that id...")
        return result.serialize(), 200

    @marshal_with(user_fields)
    @auth.login_required
    def patch(self):
        args = user_update_args.parse_args()
        result = User.query.filter_by(id=g.user.id).first()
        if not result:
            abort(404, message="User doesn't exist, cannot update...")
        if args["name"]:
            result.name = args["name"]
        if args["email"]:
            result.email = args["email"]
        if args["last_latitude"]:
            result.last_latitude = args["last_latitude"]
        if args["last_longitude"]:
            result.last_longitude = args["last_longitude"]
        if args["password"]:
            result.hash_password(args["password"])

        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            abort(500, message="Internal Server Error")

        return result, 204
    
    @marshal_with(user_fields)
    @auth.login_required
    def delete(self):
        result = User.query.filter_by(id=g.user.id).first()
        if not result:
            abort(404, message="Could not find user with that id...")
        db.session.delete(result)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            abort(500, message="Internal Server Error")

        return result, 204
    
@auth.verify_password
def verify_password(username_or_token, password):
    # Attempt to extract the token from the Authorization header
    auth_header = request.headers.get('Authorization')
    if auth_header and auth_header.startswith('Bearer '):
        token = auth_header.split(" ")[1]
        user = User.verify_auth_token(token)
        if user:
            g.user = user
            return True
        return False

    # If no Authorization header or token verification failed,
    # fall back to username and password verification
    user = User.query.filter_by(email=username_or_token).first()
    if user and user.verify_password(password):
        g.user = user
        return True
    return False

class UserLogIn(Resource):
    @marshal_with(token_fields)
    def post(self):
        tokenDuration = 600
        args = user_login_args.parse_args()
        user = User.query.filter_by(email=args["email"]).first()
        if not user:
            abort(404, message="Could not find user with that email...")
        if not user.verify_password(args["password"]):
            abort(404, message="Incorrect password...")
        token = user.generate_auth_token(tokenDuration)
        return { 'token': token, 'duration': tokenDuration, 'user_id': user.id }, 200
    
class UserChatRooms(Resource):
    @auth.login_required
    def get(self):
        result = User.query.filter_by(id=g.user.id).first()
        if not result:
            abort(404, message="Could not find user with that id...")
        # Return the serialized version of the group chats
        return [group_chat.serialize() for group_chat in result.group_chats], 200

class FriendResource(Resource):
    @auth.login_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("friend_id", type=int, required=True, help="Friend ID is required")
        args = parser.parse_args()

        friend = User.query.filter_by(id=args["friend_id"]).first()

        if not friend:
            abort(404, message="Could not find the friend with that ID.")

        g.user.friends.append(friend)
        db.session.commit()

        return {"message": "Friend added successfully"}, 201

    @auth.login_required
    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument("friend_id", type=int, required=True, help="Friend ID is required")
        args = parser.parse_args()

        friend = User.query.filter_by(id=args["friend_id"]).first()

        if not friend:
            abort(404, message="Could not find the friend with that ID.")

        g.user.friends.remove(friend)
        friend.friends.remove(g.user)
        db.session.commit()

        return {"message": "Friend removed successfully"}, 200

    @auth.login_required
    def get(self):
        friend_list = [friend.serialize() for friend in g.user.friends]
        return {"friends": friend_list}, 200


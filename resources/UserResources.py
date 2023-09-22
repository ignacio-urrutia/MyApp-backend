from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from models.UserModel import User
from models.GroupChatModel import GroupChat
from main import db

user_fields = {
    "id": fields.Integer,
    "name": fields.String,
    "email": fields.String,
    "last_latitude": fields.Float,
    "last_longitude": fields.Float,
}

user_put_args = reqparse.RequestParser()
user_put_args.add_argument("name", type=str, help="Name required", required=True)
user_put_args.add_argument("email", type=str, help="Email required", required=True)
user_put_args.add_argument("last_latitude", type=float, help="Last latitude of the user")
user_put_args.add_argument("last_longitude", type=float, help="Last longitude of the user")

user_update_args = reqparse.RequestParser()
user_update_args.add_argument("name", type=str, help="Name of the user")
user_update_args.add_argument("email", type=str, help="Email of the user")
user_update_args.add_argument("last_latitude", type=float, help="Last latitude of the user")
user_update_args.add_argument("last_longitude", type=float, help="Last longitude of the user")


class UserAll(Resource):
    @marshal_with(user_fields)
    def get(self):
        result = User.query.all()
        return result
    
    @marshal_with(user_fields)
    def post(self):
        args = user_put_args.parse_args()

        user = User(name=args["name"], email=args["email"])
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

from flask import g
from flask_restful import Api, Resource, reqparse, abort, marshal_with

from application import db
from models.FriendRequestModel import FriendRequest
from models.UserModel import User
from .UserResources import auth

class FriendRequestResource(Resource):
    @auth.login_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("receiver_id", type=int, required=True, help="Receiver ID is required")
        args = parser.parse_args()

        receiver = User.query.filter_by(id=args["receiver_id"]).first()
        if not receiver:
            abort(404, message="Could not find the receiver with that ID.")

        # Check if the users are already friends
        if receiver in g.user.friends:
            abort(400, message="You are already friends with this user.")

        # Check if the users have a pending friend request
        friend_request = FriendRequest.query.filter_by(sender_id=g.user.id, receiver_id=receiver.id, status="pending").first()
        if friend_request:
            abort(400, message="You already have a pending friend request with this user.")
            
        friend_request = FriendRequest(sender_id=g.user.id, receiver_id=receiver.id)
        db.session.add(friend_request)
        db.session.commit()

        return {"message": "Friend request sent successfully"}, 201

    @auth.login_required
    @auth.login_required
    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument("request_id", type=int, required=True, help="Request ID is required")
        parser.add_argument("status", type=str, choices=("accepted", "declined"), required=True, help="Status must be 'accepted' or 'declined'")
        args = parser.parse_args()

        request_record = FriendRequest.query.filter_by(id=args["request_id"], receiver_id=g.user.id).first()
        if not request_record:
            abort(404, message="Could not find the request with that ID.")

        if args["status"] == "accepted":
            sender = User.query.get(request_record.sender_id)
            g.user.friends.append(sender)
            sender.friends.append(g.user)  # Mutual friendship
            db.session.commit()
            request_record.status = "accepted"

        else:
            request_record.status = "declined"

        db.session.commit()

        return {"message": f"Friend request {args['status']} successfully"}, 200
    
    @auth.login_required
    def get(self):
        pending_requests = FriendRequest.query.filter_by(receiver_id=g.user.id, status="pending").all()
        return {"pending_requests": [request.serialize() for request in pending_requests]}, 200
    

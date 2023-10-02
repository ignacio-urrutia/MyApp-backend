from flask import Flask, request, jsonify
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin


application = Flask(__name__)
cors = CORS(application)

# app.config['CORS_HEADERS'] = 'Content-Type'
api = Api(application)
application.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db = SQLAlchemy(application)

from resources.UserResources import UserAll, UserById, UserLogIn
from resources.GroupChatResources import GroupChatAll, GroupChatById, GroupChatAddUser

# Routes
# Users
api.add_resource(UserAll, "/users/")   
api.add_resource(UserById, "/users/<int:user_id>")
api.add_resource(UserLogIn, "/users/login")

# Group Chats
api.add_resource(GroupChatAll, "/groupchats/")
api.add_resource(GroupChatById, "/groupchats/<int:group_chat_id>")
api.add_resource(GroupChatAddUser, "/groupchats/<int:group_chat_id>/adduser")


if __name__ == '__main__':
    application.run(host = '0.0.0.0', debug=True)
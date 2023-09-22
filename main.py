from flask import Flask, request, jsonify
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db = SQLAlchemy(app)

from resources.UserResources import UserAll, UserById
from resources.GroupChatResources import GroupChatAll, GroupChatById, GroupChatAddUser

# Routes
# Users
api.add_resource(UserAll, "/users/")   
api.add_resource(UserById, "/users/<int:user_id>")

# Group Chats
api.add_resource(GroupChatAll, "/groupchats/")
api.add_resource(GroupChatById, "/groupchats/<int:group_chat_id>")
api.add_resource(GroupChatAddUser, "/groupchats/<int:group_chat_id>/adduser")


if __name__ == '__main__':
    app.run(debug=True)
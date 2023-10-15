from flask import Flask, request, jsonify
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS, cross_origin
from flask_httpauth import HTTPBasicAuth

application = Flask(__name__)
cors = CORS(application, resources={r"/*": {"origins": "*", "supports_credentials": True}})

# app.config['CORS_HEADERS'] = 'Content-Type'
api = Api(application)
application.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
application.config['SECRET_KEY'] = 'your_secret_key_here'
db = SQLAlchemy(application)
migrate = Migrate(application, db)

from resources.UserResources import UserAll, UserById, UserByToken, UserLogIn, UserChatRooms, SignUp
from resources.GroupChatResources import GroupChatAll, GroupChatById, GroupChatAddUser, GroupChatMessages, RecentMessagesResource, OlderMessagesResource
from resources.MessageResources import MessageResource
from resources.MultimediaResources import MultimediaResource

# Routes
# Users
api.add_resource(UserAll, "/all-users/")   
api.add_resource(SignUp, "/signup")
api.add_resource(UserByToken, "/users/")
api.add_resource(UserById, "/users/id/<int:user_id>")
api.add_resource(UserLogIn, "/users/login")
api.add_resource(UserChatRooms, "/users/chatrooms")

# Group Chats
api.add_resource(GroupChatAll, "/groupchats/")
api.add_resource(GroupChatById, "/groupchats/<int:group_chat_id>")
api.add_resource(GroupChatAddUser, "/groupchats/<int:group_chat_id>/adduser")
api.add_resource(GroupChatMessages, '/groupchats/<int:group_chat_id>/messages')
api.add_resource(RecentMessagesResource, '/groupchats/<int:group_chat_id>/recent-messages')
api.add_resource(OlderMessagesResource, '/groupchats/<int:group_chat_id>/older-messages/<int:earliest_message_id>')

# Messages
api.add_resource(MessageResource, '/messages/')

# Multimedia
api.add_resource(MultimediaResource, '/messages/<int:message_id>/multimedia')


if __name__ == '__main__':
    application.run(host = '0.0.0.0', debug=True)
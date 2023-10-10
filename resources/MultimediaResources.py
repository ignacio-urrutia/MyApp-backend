from flask_restful import Resource
from models.MessageModel import Message
from models.MultimediaModel import Multimedia  # Assuming this is your Multimedia model

class MultimediaResource(Resource):
    def get(self, message_id):
        message = Message.query.get(message_id)
        if message is None:
            return {"message": "Message not found"}, 404
        multimedia_items = message.multimedia
        return [item.serialize() for item in multimedia_items], 200
from flask_restful import Resource
from models.MessageModel import Message
from models.MultimediaModel import Multimedia, s3 # Assuming this is your Multimedia model
from application import db
from flask import request, send_file
from io import BytesIO
import os
import boto3

class MultimediaResource(Resource):
    def get(self, message_id):
        message = Message.query.get(message_id)
        if message is None:
            return {"message": "Message not found"}, 404
        multimedia_items = message.multimedia
        return [item.serialize() for item in multimedia_items], 200
    
    def post(self, message_id):
        message = Message.query.get(message_id)
        if message is None:
            return {"message": "Message not found"}, 404
        files = request.files.getlist("file")
        for file in files:
            filename = f"{message_id}_{file.filename}"
            multimedia = Multimedia.upload_file(message_id, file, filename)
            print(multimedia.serialize())         
        return {"message": "Multimedia uploaded successfully"}, 201

class MultimediaFile(Resource):
    def get(self, file_id):
        multimedia = Multimedia.query.get(file_id)
        if multimedia is None:
            return {"message": "Multimedia not found"}, 404
        bucket_name = 'area-chat'
        try:
            file = s3.get_object(Bucket=bucket_name, Key=multimedia.file_url)
            return send_file(
                BytesIO(file['Body'].read()),
                mimetype=file['ContentType'],
                as_attachment=True,
                download_name=multimedia.filename
            )
        except Exception as e:
            return {'message': str(e)}, 404
from flask_restful import Resource
from models.MessageModel import Message
from models.MultimediaModel import Multimedia  # Assuming this is your Multimedia model
from application import db
from flask import request

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
            file_name = f"{message_id}_{file.filename}"
            multimedia = Multimedia(type=file.content_type, message_id=message_id)
            multimedia.file_url = multimedia.upload_file(file, multimedia.id)
            multimedia.filename = file_name
            print("File name: ", file_name)
            print(multimedia.serialize())
            
            db.session.add(multimedia)
        db.session.commit()
        return {"message": "Multimedia uploaded successfully"}, 201

class MultimediaFile(Resource):
    def get(self, file_id):
        bucket_name = 'area-chat'
        try:
            file = s3.get_object(Bucket=bucket_name, Key=file_id)
            return send_file(
                BytesIO(file['Body'].read()),
                mimetype=file['ContentType'],
                as_attachment=True,
                attachment_filename=filename
            )
        except Exception as e:
            return {'message': str(e)}, 404
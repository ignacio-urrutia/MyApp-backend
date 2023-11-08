import os
import boto3
from sqlalchemy import UniqueConstraint

from application import db

aws_access_key = os.environ.get('AWS_ACCESS_KEY_ID')
aws_secret_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
aws_region = os.environ.get('AWS_REGION', 'us-east-2')

print(aws_access_key, aws_secret_key, aws_region)

s3 = boto3.client(
    "s3",
    aws_access_key_id=aws_access_key,
    aws_secret_access_key=aws_secret_key,
    region_name=aws_region
)

class Multimedia(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String, nullable=False)  # e.g., 'image', 'video', 'audio', 'pdf'
    file_url = db.Column(db.String, nullable=False)
    message_id = db.Column(db.Integer, db.ForeignKey('message.id'), nullable=False)
    filename = db.Column(db.String, nullable=True)

    def serialize(self):
        return {
            'id': self.id,
            'type': self.type,
            'file_url': self.file_url,
            'message_id': self.message_id,
            'filename': self.filename
        }
    
    def upload_file(message_id, file, filename):
        multimedia = Multimedia(type=file.content_type, message_id=message_id, filename=filename, file_url=f"files/{message_id}")
        db.session.add(multimedia)
        db.session.flush()  # This will assign an ID without committing the transaction
        try:
            s3.upload_fileobj(
                file,
                "area-chat",
                f"files/{message_id}/{multimedia.id}",  # Assuming you want to include the message_id in the path
                ExtraArgs={
                    "ContentType": file.content_type
                }
            )
            multimedia.file_url = f"files/{message_id}/{multimedia.id}"  # Update the file_url with the new path
            db.session.commit()
            return multimedia
        except Exception as e:
            db.session.rollback()  # Rollback the session in case of exception
            raise e

class ProfilePicture(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String, nullable=False)
    file_url = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    filename = db.Column(db.String, nullable=True)

    # Add a unique constraint to user_id to ensure one profile picture per user
    __table_args__ = (UniqueConstraint('user_id', name='unique_user_id'),)

    def serialize(self):
        return {
            'id': self.id,
            'type': self.type,
            'file_url': self.file_url,
            'user_id': self.user_id,
            'filename': self.filename
        }
    
    @staticmethod
    def upload_file(user_id, file, filename):
        # Check if a profile picture already exists for the user
        existing_profile_picture = ProfilePicture.query.filter_by(user_id=user_id).first()

        if existing_profile_picture:
            profile_picture = existing_profile_picture
            # Update the existing record with new file data
            profile_picture.type = file.content_type
            profile_picture.filename = filename
        else:
            # If not, create a new profile picture record
            profile_picture = ProfilePicture(type=file.content_type, user_id=user_id, filename=filename, file_url=f"profile_pictures/{user_id}")
            db.session.add(profile_picture)
        
        db.session.flush()

        try:
            # Generate the file path using the profile picture's ID
            file_path = f"profile_pictures/{user_id}"
            
            # Upload the file to S3
            s3.upload_fileobj(
                file,
                "area-chat",
                file_path,
                ExtraArgs={
                    "ContentType": file.content_type
                }
            )
            # Update the file_url after successful upload
            profile_picture.file_url = file_path
            db.session.commit()
            return profile_picture
        except Exception as e:
            db.session.rollback()
            raise e
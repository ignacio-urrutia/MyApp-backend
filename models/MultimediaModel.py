import os
import boto3

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
            'file_url': self.presigned_url(),
            'message_id': self.message_id,
            'filename': self.filename
        }
    
    def upload_file(self, file, file_id):
        try:
            s3.upload_fileobj(
                file,
                "area-chat",
                file_id,
                ExtraArgs={
                    "ContentType": file.content_type
                }
            )
            return f"https://area-chat.s3.us-east-2.amazonaws.com/{file_name}"
        except Exception as e:
            print("Something Happened: ", e)
            return e
    
    def presigned_url(self):
        print(self.filename)
        url = s3.generate_presigned_url(
            ClientMethod='get_object',
            Params={
                'Bucket': 'area-chat',
                'Key': self.filename
            }
        )
        return url


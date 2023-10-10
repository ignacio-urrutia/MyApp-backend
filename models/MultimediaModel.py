from application import db

class Multimedia(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String, nullable=False)  # e.g., 'image', 'video', 'audio', 'pdf'
    file_url = db.Column(db.String, nullable=False)
    message_id = db.Column(db.Integer, db.ForeignKey('message.id'), nullable=False)

    def serialize(self):
        return {
            'id': self.id,
            'type': self.type,
            'file_url': self.file_url,
            'message_id': self.message_id,
        }

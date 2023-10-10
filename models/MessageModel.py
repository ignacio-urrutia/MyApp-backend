from application import db
from datetime import datetime
from models.MultimediaModel import Multimedia

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(500), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    group_chat_id = db.Column(db.Integer, db.ForeignKey('group_chat.id'), nullable=False)
    multimedia = db.relationship('Multimedia', backref='message', lazy=True)

    def serialize(self):
        return {
            'id': self.id,
            'content': self.content,
            'timestamp': self.timestamp.isoformat(),  # Convert datetime to string
            'user_id': self.user_id,
            'group_chat_id': self.group_chat_id,
            'multimedia': [item.serialize() for item in self.multimedia]
        }


    def __repr__(self):
        return f"Message(id={self.id}, content={self.content}, timestamp={self.timestamp})"

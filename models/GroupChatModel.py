from application import db
from models.UserModel import usersGroupChats
from models.MessageModel import Message

class GroupChat(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    north_boundary = db.Column(db.Float, nullable=False)
    south_boundary = db.Column(db.Float, nullable=False)
    east_boundary = db.Column(db.Float, nullable=False)
    west_boundary = db.Column(db.Float, nullable=False)
    # users = db.relationship("User", secondary=usersGroupChats, lazy="subquery")
    description = db.Column(db.Text, nullable=True)
    owner_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    messages = db.relationship('Message', backref='group_chat', lazy=True)

    def serialize(self):
        return {
            'id': self.id,
            'content': self.name,
            'north_boundary': self.north_boundary,
            'south_boundary': self.south_boundary,
            'east_boundary': self.east_boundary,
            'west_boundary': self.west_boundary,
            'description': self.description,
            'owner_id': self.owner_id,
            'last_message': self.messages[-1].serialize() if len(self.messages) > 0 else None
        }

    def __repr__(self):
        return f"GroupChat(name={self.name}, north_boundary={self.north_boundary}, south_boundary={self.south_boundary}, east_boundary={self.east_boundary}, west_boundary={self.west_boundary})"

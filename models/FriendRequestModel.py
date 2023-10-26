from application import db
from models.UserModel import User

class FriendRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    receiver_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    status = db.Column(db.String(20), default="pending")  # pending, accepted, declined

    def serialize(self):
        sender = User.query.get(self.sender_id)
        receiver = User.query.get(self.receiver_id)
        return {
            'id': self.id,
            'sender': sender.serialize(include_group_chats=False, include_friends=False),
            'receiver': receiver.serialize(include_group_chats=False, include_friends=False),
            'status': self.status
        }
from application import db

class GroupChat(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    owner_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    messages = db.relationship('Message', backref='group_chat', lazy=True)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    radius = db.Column(db.Float, nullable=False)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'owner_id': self.owner_id,
            'last_message': self.messages[-1].serialize() if len(self.messages) > 0 else None,
            'users': [user.serialize(include_group_chats=False) for user in self.users],
            'latitude': self.latitude,
            'longitude': self.longitude,
            'radius': self.radius
        }

    def __repr__(self):
        return f"GroupChat(name={self.name}, description={self.description}, owner_id={self.owner_id})"

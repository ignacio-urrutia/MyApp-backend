from application import db
from models.UserModel import usersGroupChats

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

    def __repr__(self):
        return f"GroupChat(name={self.name}, north_boundary={self.north_boundary}, south_boundary={self.south_boundary}, east_boundary={self.east_boundary}, west_boundary={self.west_boundary})"

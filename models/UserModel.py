from main import db

usersGroupChats = db.Table("users_group_chats",
    db.Column("user_id", db.Integer, db.ForeignKey("user.id"), primary_key=True),
    db.Column("group_chat_id", db.Integer, db.ForeignKey("group_chat.id"), primary_key=True)
)

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    # password_hash = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    last_latitude = db.Column(db.Float, nullable=True)
    last_longitude = db.Column(db.Float, nullable=True)
    group_chats = db.relationship("GroupChat", secondary=usersGroupChats, lazy="subquery", backref=db.backref("users", lazy=True))

    def __repr__(self):
        return f"User(name={self.name}, email={self.email})"

from application import db
from application import application as app
from werkzeug.security import generate_password_hash, check_password_hash
import time
import jwt

usersGroupChats = db.Table("users_group_chats",
    db.Column("user_id", db.Integer, db.ForeignKey("user.id"), primary_key=True),
    db.Column("group_chat_id", db.Integer, db.ForeignKey("group_chat.id"), primary_key=True)
)

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password_hash = db.Column(db.String(100), nullable=False)
    # password = db.Column(db.String(100), nullable=False)
    last_latitude = db.Column(db.Float, nullable=True)
    last_longitude = db.Column(db.Float, nullable=True)
    group_chats = db.relationship("GroupChat", secondary=usersGroupChats, lazy="subquery", backref=db.backref("users", lazy=True))

    def hash_password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def generate_auth_token(self, expires_in = 600):
        return jwt.encode(
            { 'id': self.id, 'exp': time.time() + expires_in }, 
            app.config['SECRET_KEY'], algorithm='HS256')

    @staticmethod
    def verify_auth_token(token):
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])  # Notice the change here
        except Exception as e:
            return 
        return User.query.get(data['id'])

    def __repr__(self):
        return f"User(name={self.name}, email={self.email})"

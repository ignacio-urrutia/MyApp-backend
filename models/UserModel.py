from math import radians, cos, sin, asin, sqrt
from application import db
from application import application as app
from werkzeug.security import generate_password_hash, check_password_hash
import time
import jwt
from models.MultimediaModel import ProfilePicture
from models.GroupChatModel import GroupChat

def haversine(lon1, lat1, lon2, lat2):
    # Convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371000  # Radius of Earth in meters
    return c * r


usersGroupChats = db.Table("users_group_chats",
    db.Column("user_id", db.Integer, db.ForeignKey("user.id"), primary_key=True),
    db.Column("group_chat_id", db.Integer, db.ForeignKey("group_chat.id"), primary_key=True)
)

friendships = db.Table("friendships",
    db.Column("user_id", db.Integer, db.ForeignKey("user.id"), primary_key=True),
    db.Column("friend_id", db.Integer, db.ForeignKey("user.id"), primary_key=True)
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
    friends = db.relationship("User",
        secondary=friendships,
        primaryjoin=(friendships.c.user_id == id),
        secondaryjoin=(friendships.c.friend_id == id),
        backref=db.backref("friend_of", lazy="dynamic"),
        lazy="dynamic")
    profile_picture = db.relationship("ProfilePicture", uselist=False, backref="user", lazy=True)

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
    
    def update_chatrooms(self):
        # Ensure the user has valid last known coordinates
        if self.last_longitude is None or self.last_latitude is None:
            return  # Cannot update chatrooms without user's location

        # Create a user point from the last known user coordinates
        user_location = (self.last_longitude, self.last_latitude)

        # Get all the chatrooms
        chatrooms = GroupChat.query.all()

        # List to hold chatrooms within the user's radius
        chatrooms_within_radius = []

        # Iterate over the chatrooms and check the distance
        for chatroom in chatrooms:
            # Ensure the chatroom has valid coordinates
            if chatroom.longitude is None or chatroom.latitude is None:
                continue  # Cannot calculate distance for this chatroom

            # Calculate the distance to the user using the haversine formula
            distance = haversine(chatroom.longitude, chatroom.latitude, *user_location)

            # If the chatroom is within the user's radius, add it to the list
            if distance <= chatroom.radius:
                chatrooms_within_radius.append(chatroom)

        # Update the user's chatrooms in a way that SQLAlchemy expects
        # Clear the user's current chatrooms
        self.group_chats.clear()

        # Add the new chatrooms
        for chatroom in chatrooms_within_radius:
            self.group_chats.append(chatroom)

        # Commit the session to save changes
        db.session.commit()


    def __repr__(self):
        return f"User(name={self.name}, email={self.email})"
    
    def serialize(self, include_group_chats=True, include_friends=True):            
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'last_latitude': self.last_latitude,
            'last_longitude': self.last_longitude,
            'group_chats': [group_chat.serialize() for group_chat in self.group_chats] if include_group_chats else None,
            'friends': [friend.serialize(include_group_chats=False, include_friends=False) for friend in self.friends] if include_friends else None,
            'profile_picture': self.profile_picture.file_url if self.profile_picture else None
        }


from application import db, app
from models.UserModel import User
from models.GroupChatModel import GroupChat

def create_sample_users():
    # Create a list of sample users
    users = [
        User(name="John Doe", email="john.doe@example.com", password="password"),
        User(name="Jane Doe", email="jane.doe@example.com", password="password"),
        # Add more users as needed
    ]

    # Add users to the session and commit
    db.session.add_all(users)
    db.session.commit()

def create_sample_group_chats():
    # Assuming you have already created some sample users
    user1 = User.query.filter_by(name="John Doe").first()
    user2 = User.query.filter_by(name="Jane Doe").first()
    
    # Create a list of sample group chats
    group_chats = [
        GroupChat(name="Sample Group 1", owner_id=user1.id, 
                  north_boundary=1.0, south_boundary=-1.0, 
                  east_boundary=1.0, west_boundary=-1.0, 
                  description="This is a sample group chat."),
        GroupChat(name="Sample Group 2", owner_id=user2.id, 
                  north_boundary=2.0, south_boundary=-2.0, 
                  east_boundary=2.0, west_boundary=-2.0, 
                  description="This is another sample group chat."),
        # Add more group chats as needed
    ]

    group_chats[0].users.append(user1)
    group_chats[0].users.append(user2)
    group_chats[1].users.append(user1) 
    
    # Add group chats to the session and commit
    db.session.add_all(group_chats)
    db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        create_sample_users()
        create_sample_group_chats()



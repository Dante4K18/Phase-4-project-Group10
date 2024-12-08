from app import app, db
from models import User, Post, Follow # Import your models

def seed_data():
    # Drop all tables and recreate them
    db.drop_all()
    db.create_all()

    # Seed users
    users = [
        User(
            username="johndoe",
            email="johndoe@example.com",
            bio="Lover of technology and coffee.",
            avatar="https://via.placeholder.com/150"
        ),
        User(
            username="janedoe",
            email="janedoe@example.com",
            bio="Travel enthusiast and food blogger.",
            avatar="https://via.placeholder.com/150"
        ),
        User(
            username="techguru",
            email="techguru@example.com",
            bio="Coding is my superpower.",
            avatar="https://via.placeholder.com/150"
        ),
    ]

    for user in users:
        user.set_password("password123")  # Set a default password for all users
        db.session.add(user)

    db.session.commit()

    # Get user IDs
    johndoe = User.query.filter_by(username="johndoe").first()
    janedoe = User.query.filter_by(username="janedoe").first()
    techguru = User.query.filter_by(username="techguru").first()

    # Seed posts
    posts = [
        Post(
            user_id=johndoe.id,
            content="Just joined ConnectSphere! Excited to connect with everyone.",
        ),
        Post(
            user_id=janedoe.id,
            content="Exploring the beauty of Bali. Check out my latest blog!",
        ),
        Post(
            user_id=techguru.id,
            content="Learned a new trick in Flask today. Loving the journey of coding.",
        ),
    ]

    for post in posts:
        db.session.add(post)

    db.session.commit()

    print("Database successfully seeded!")

if __name__ == "__main__":
    with app.app_context():
        seed_data()

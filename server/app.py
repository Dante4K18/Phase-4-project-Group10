from flask import Flask,jsonify,request,session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from models import User,Post,Follow,Like
from werkzeug.security import check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/connectsphere'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
CORS(app)

## Signup
@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    try:
        user = User(username=data['username'], email=data['email'])
        user.set_password(data['password'])  # Assuming a method for password hashing
        db.session.add(user)
        db.session.commit()
        return jsonify({"message": "User created successfully!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

## Login
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    if user and check_password_hash(user.password_hash, data['password']):
        session['user_id'] = user.id
        return jsonify({"message": "Login successful!", "user": user.to_dict()}), 200
    return jsonify({"error": "Invalid email or password"}), 401

## Get All Posts(Read)
@app.route('/posts', methods=['GET'])
def get_posts():
    posts = Post.query.all()
    return jsonify([post.to_dict() for post in posts]), 200

## Get a Single Post (Read)
@app.route('/posts/<int:post_id>', methods=['GET'])
def get_post(post_id):
    post = Post.query.get(post_id)
    if post:
        return jsonify(post.to_dict()), 200
    return jsonify({"error": "Post not found"}), 404

## Create a Post (Create)
@app.route('/posts', methods=['POST'])
def create_post():
    data = request.get_json()
    post = Post(title=data['title'], content=data['content'], user_id=session.get('user_id'))
    db.session.add(post)
    db.session.commit()
    return jsonify(post.to_dict()), 201

## Update a Post (Patch)
@app.route('/posts/<int:post_id>', methods=['PATCH'])
def update_post(post_id):
    data = request.get_json()
    post = Post.query.get(post_id)
    if not post:
        return jsonify({"error": "Post not found"}), 404
    if 'title' in data:
        post.title = data['title']
    if 'content' in data:
        post.content = data['content']
    db.session.commit()
    return jsonify(post.to_dict()), 200

## Replace a Post (Put)
@app.route('/posts/<int:post_id>', methods=['PUT'])
def replace_post(post_id):
    data = request.get_json()
    post = Post.query.get(post_id)
    if not post:
        return jsonify({"error": "Post not found"}), 404
    post.title = data.get('title', post.title)
    post.content = data.get('content', post.content)
    db.session.commit()
    return jsonify(post.to_dict()), 200

## Delete a Post (Delete)
@app.route('/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    post = Post.query.get(post_id)
    if not post:
        return jsonify({"error": "Post not found"}), 404
    db.session.delete(post)
    db.session.commit()
    return '', 204

## User Follow
@app.route('/users/<int:user_id>/follow', methods=['POST'])
def follow_user(user_id):
    follower_id = session.get('user_id')
    if not follower_id:
        return jsonify({"error": "Unauthorized"}), 401
    user_to_follow = User.query.get(user_id)
    if not user_to_follow:
        return jsonify({"error": "User not found"}), 404
    user = User.query.get(follower_id)
    user.following.append(user_to_follow)
    db.session.commit()
    return jsonify({"message": f"You are now following {user_to_follow.username}"}), 200

## User Unfollow
@app.route('/users/<int:user_id>/unfollow', methods=['POST'])
def unfollow_user(user_id):
    follower_id = session.get('user_id')
    if not follower_id:
        return jsonify({"error": "Unauthorized"}), 401
    user_to_unfollow = User.query.get(user_id)
    if not user_to_unfollow:
        return jsonify({"error": "User not found"}), 404
    user = User.query.get(follower_id)
    user.following.remove(user_to_unfollow)
    db.session.commit()
    return jsonify({"message": f"You have unfollowed {user_to_unfollow.username}"}), 200

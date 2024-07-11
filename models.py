from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    # Increased length to 256
    password = db.Column(db.String(256), nullable=False)
    messages = db.relationship('Message', backref='author', lazy=True)


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(256), nullable=False)
    sentiment = db.Column(db.String(20))
    timestamp = db.Column(db.DateTime, index=True, default=db.func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

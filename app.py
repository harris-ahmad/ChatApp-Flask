from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash,
    jsonify
)
from flask_socketio import SocketIO, emit, join_room, leave_room
from werkzeug.security import generate_password_hash, check_password_hash
from config import Config
from models import db, User, Message
from flask_migrate import Migrate
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pandas as pd

nltk.download('vader_lexicon')

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
migrate = Migrate(app, db)
socketio = SocketIO(app)
app.secret_key = 'supersecretkey'

# Initialize sentiment analyzer
sid = SentimentIntensityAnalyzer()


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password)

        if User.query.filter_by(username=username).first():
            flash('Username already exists!')
            return redirect(url_for('register'))

        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful!')
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if not user or not check_password_hash(user.password, password):
            flash('Invalid username or password!')
            return redirect(url_for('login'))

        session['user_id'] = user.id
        session['username'] = user.username
        flash('Login successful!')
        return redirect(url_for('chat_room'))

    return render_template('login.html')


@app.route('/chat')
def chat_room():
    if 'username' not in session:
        return redirect(url_for('login'))

    messages = Message.query.order_by(Message.timestamp).all()
    return render_template('chat.html', messages=messages)


@socketio.on('join')
def handle_join(data):
    room = data['room']
    join_room(room)
    emit('message', {'username': 'System',
         'message': data['username'] + ' has joined the room.'}, room=room)


@socketio.on('leave')
def handle_leave(data):
    room = data['room']
    leave_room(room)
    emit('message', {'username': 'System',
         'message': data['username'] + ' has left the room.'}, room=room)


@socketio.on('message')
def handle_message(data):
    user = User.query.filter_by(username=data['username']).first()

    sentiment = sid.polarity_scores(data['message'])['compound']
    sentiment_label = 'positive' if sentiment >= 0.05 else 'negative' \
        if sentiment <= - 0.05 else 'neutral'

    message = Message(content=data['message'],
                      sentiment=sentiment_label, user_id=user.id)
    db.session.add(message)
    db.session.commit()

    room = data['room']
    emit('message', {'username': data['username'],
         'message': data['message'], 'sentiment': sentiment_label}, room=room)


@app.route('/api/messages', methods=['GET'])
def get_messages():
    messages = Message.query.all()
    return jsonify([{
        'username': m.author.username,
        'message': m.content,
        'sentiment': m.sentiment,
        'timestamp': m.timestamp
        } for m in messages])


@app.route('/api/analytics', methods=['GET'])
def get_analytics():
    messages = Message.query.all()
    df = pd.DataFrame([{'username': m.author.username,
                        'message': m.content,
                        'sentiment': m.sentiment,
                        'timestamp': m.timestamp
                        } for m in messages])
    sentiment_counts = df['sentiment'].value_counts().to_dict()
    return jsonify(sentiment_counts)


if __name__ == '__main__':
    socketio.run(app, debug=True)


# 📞 Real-time Chat Application with Analytics

Welcome to the Real-time Chat Application with Analytics! This application allows users to chat in real-time, analyze chat sentiment, and track user interactions.

## 🎯 Features

- **Real-time Messaging**: Communicate with others in real-time using WebSockets.
- **Sentiment Analysis**: Analyze the sentiment of chat messages using NLP.
- **User Analytics**: Track user behavior and interactions.
- **Database Management**: Store messages and user data in PostgreSQL.
- **API Endpoints**: Expose RESTful APIs for message retrieval and analytics data.

## 🛠️ Tech Stack

- **Backend**: Flask, SQLAlchemy
- **Database**: PostgreSQL
- **Real-time Communication**: WebSockets (Flask-SocketIO)
- **Sentiment Analysis**: NLTK
- **Data Analysis**: Pandas

## 🚀 Getting Started

Follow these steps to get the application up and running on your local machine.

### Prerequisites

- Python 3.6+
- PostgreSQL
- Node.js (for installing Socket.IO)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/chat-app.git
   cd chat-app
   ```

2. **Set up a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install the required packages:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up PostgreSQL:**
   - Ensure PostgreSQL is installed and running.
   - Create a new database and user:
     ```sql
     CREATE DATABASE chat_app_db;
     CREATE USER chat_app_user WITH ENCRYPTED PASSWORD 'your_password';
     GRANT ALL PRIVILEGES ON DATABASE chat_app_db TO chat_app_user;
     ```

5. **Configure the application:**
   - Update `config.py` with your database credentials.

6. **Run database migrations:**
   ```bash
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade
   ```

7. **Run the application:**
   ```bash
   python app.py
   ```

## 📝 Usage

1. **Register an account:**
   - Navigate to `http://localhost:5000/register`.
   - Fill in your username and password to register.

2. **Login to the chat:**
   - Navigate to `http://localhost:5000/login`.
   - Use your credentials to log in.

3. **Start chatting:**
   - After logging in, you'll be redirected to the chat room where you can start chatting in real-time.

## 📊 API Endpoints

- **GET /api/messages**: Retrieve all chat messages.
- **GET /api/analytics**: Retrieve sentiment analysis data.

## 🤖 Sentiment Analysis

The application uses NLTK's VADER sentiment analysis to determine the sentiment of each message as positive, negative, or neutral.

## 🧑‍💻 Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any enhancements or bug fixes.

## 📜 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- Special thanks to the creators of Flask, SQLAlchemy, Socket.IO, NLTK, and Pandas.
from flask import Flask, jsonify
from flask_cors import CORS
import psycopg2
from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
from flask_security import UserMixin, RoleMixin
from datetime import datetime
from sqlalchemy import text
import os
from dotenv import load_dotenv
from flask import Flask, render_template_string, request
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore, auth_required, hash_password, roles_required, current_user
from flask_security.models import fsqla_v3 as fsqla
from flask_socketio import SocketIO, join_room, leave_room, emit, rooms, disconnect
import random
import string
import functools

app = Flask(__name__)
app.config.from_object(__name__)

load_dotenv()

# Generate a nice key using secrets.token_urlsafe()
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
app.config['SECURITY_PASSWORD_SALT'] = os.getenv("SECURITY_PASSWORD_SALT")
# have session and remember cookie be samesite (flask/flask_login)
# app.config["REMEMBER_COOKIE_SAMESITE"] = "strict"
# app.config["SESSION_COOKIE_SAMESITE"] = "strict"
app.config["SECURITY_REGISTERABLE"] = True
# Disable all email functionality
app.config['SECURITY_SEND_REGISTER_EMAIL'] = False
app.config['SECURITY_SEND_PASSWORD_CHANGE_EMAIL'] = False
app.config['SECURITY_SEND_PASSWORD_RESET_NOTICE_EMAIL'] = False
app.config['SECURITY_SEND_PASSWORD_RESET_EMAIL'] = False
app.config['SECURITY_CONFIRMABLE'] = False

app.config["SECURITY_USERNAME_ENABLE"] = True
app.config["SECURITY_USERNAME_REQUIRED"] = True
app.config['SECURITY_TOKEN_AUTHENTICATION_HEADER'] = 'Authentication-Token'
# app.config['SECURITY_TOKEN_MAX_AGE'] = 3600
app.config['SECURITY_CSRF_PROTECT'] = False
app.config['WTF_CSRF_ENABLED'] = False



app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("SQLALCHEMY_DATABASE_URI")
# app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
#     "pool_pre_ping": True,
# }
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
fsqla.FsModels.set_db_info(db)


# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})
socketio = SocketIO(app, cors_allowed_origins="*")


# Association Tables
roles_users = db.Table('roles_users',
    db.Column('user_id', db.UUID, db.ForeignKey('users.id')),
    db.Column('role_id', db.Integer, db.ForeignKey('roles.id')),
    extend_existing=True 
)

# class Friendship(db.Model):
#     __tablename__ = 'friendships'
#     user_id = db.Column(db.UUID, db.ForeignKey('users.id'), primary_key=True)
#     friend_id = db.Column(db.UUID, db.ForeignKey('users.id'), primary_key=True)
#     status = db.Column(db.String(20), default='pending')
#     created_at = db.Column(db.DateTime, default=datetime.utcnow)

# class ClubMember(db.Model):
#     __tablename__ = 'club_members'
#     club_id = db.Column(db.UUID, db.ForeignKey('clubs.id'), primary_key=True)
#     user_id = db.Column(db.UUID, db.ForeignKey('users.id'), primary_key=True)
#     role = db.Column(db.String(20), default='member')
#     joined_at = db.Column(db.DateTime, default=datetime.utcnow)

# Core Models
class Role(db.Model, RoleMixin):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.UUID, primary_key=True, default=db.text('uuid_generate_v4()'))
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    rating = db.Column(db.Integer, default=1200)
    wins = db.Column(db.Integer, default=0)
    losses = db.Column(db.Integer, default=0)
    draws = db.Column(db.Integer, default=0)
    profile_pic = db.Column(db.Text)
    current_skin = db.Column(db.String(50), default='classic')
    current_theme = db.Column(db.String(50), default='default')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False)
    active = db.Column(db.Boolean(), default=True)

    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "username": self.username,
            "rating": self.rating,
            "wins": self.wins,
            "losses": self.losses,
            "draws": self.draws,
            "profile_pic": self.profile_pic,
            "current_skin": self.current_skin,
            "current_theme": self.current_theme,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "last_login": self.last_login.isoformat() if self.last_login else None,
            "active": self.active,
        }
    
    # Relationships
    roles = db.relationship('Role', secondary=roles_users,
                           backref=db.backref('users', lazy='dynamic'))
    # friends = db.relationship('User', secondary='friendships',
    #                         primaryjoin="User.id==Friendship.user_id",
    #                         secondaryjoin="User.id==Friendship.friend_id")
    # clubs = db.relationship('Club', secondary='club_members', backref='members')
    # puzzles = db.relationship('UserPuzzleProgress', backref='user', lazy=True)
    # tournaments = db.relationship('Tournament', secondary='tournament_participants', backref='participants')

# class Game(db.Model):
#     __tablename__ = 'games'
#     id = db.Column(db.UUID, primary_key=True, default=db.text('uuid_generate_v4()'))
#     pgn = db.Column(db.Text, nullable=False)
#     status = db.Column(db.String(20), default='ongoing')
#     created_at = db.Column(db.DateTime, default=datetime.utcnow)
#     ended_at = db.Column(db.DateTime)
#     result = db.Column(db.String(10))
#     zobrist_hash = db.Column(db.BigInteger)
    
#     # Relationships
#     white_id = db.Column(db.UUID, db.ForeignKey('users.id'))
#     black_id = db.Column(db.UUID, db.ForeignKey('users.id'))
#     white = db.relationship('User', foreign_keys=[white_id])
#     black = db.relationship('User', foreign_keys=[black_id])
#     moves = db.relationship('Move', backref='game', lazy=True)

# class Move(db.Model):
#     __tablename__ = 'moves'
#     id = db.Column(db.Integer, primary_key=True)
#     game_id = db.Column(db.UUID, db.ForeignKey('games.id'), nullable=False)
#     move_num = db.Column(db.Integer, nullable=False)
#     uci = db.Column(db.String(10), nullable=False)
#     fen = db.Column(db.String(100), nullable=False)
#     played_at = db.Column(db.DateTime, default=datetime.utcnow)

# class Club(db.Model):
#     __tablename__ = 'clubs'
#     id = db.Column(db.UUID, primary_key=True, default=db.text('uuid_generate_v4()'))
#     name = db.Column(db.String(100), nullable=False)
#     description = db.Column(db.Text)
#     created_at = db.Column(db.DateTime, default=datetime.utcnow)
#     owner_id = db.Column(db.UUID, db.ForeignKey('users.id'))

# class Puzzle(db.Model):
#     __tablename__ = 'puzzles'
#     id = db.Column(db.UUID, primary_key=True, default=db.text('uuid_generate_v4()'))
#     fen = db.Column(db.String(100), nullable=False)
#     solution = db.Column(db.JSON, nullable=False)
#     difficulty = db.Column(db.Integer, nullable=False)
#     themes = db.Column(db.JSON)
#     created_at = db.Column(db.DateTime, default=datetime.utcnow)

# class UserPuzzleProgress(db.Model):
#     __tablename__ = 'user_puzzle_progress'
#     user_id = db.Column(db.UUID, db.ForeignKey('users.id'), primary_key=True)
#     puzzle_id = db.Column(db.UUID, db.ForeignKey('puzzles.id'), primary_key=True)
#     solved = db.Column(db.Boolean, default=False)
#     attempts = db.Column(db.Integer, default=0)
#     last_attempted = db.Column(db.DateTime)

# class Tournament(db.Model):
#     __tablename__ = 'tournaments'
#     id = db.Column(db.UUID, primary_key=True, default=db.text('uuid_generate_v4()'))
#     name = db.Column(db.String(100), nullable=False)
#     format = db.Column(db.String(20), nullable=False)
#     status = db.Column(db.String(20), default='upcoming')
#     start_date = db.Column(db.DateTime)
#     end_date = db.Column(db.DateTime)

# class SkinUnlock(db.Model):
#     __tablename__ = 'skin_unlocks'
#     user_id = db.Column(db.UUID, db.ForeignKey('users.id'), primary_key=True)
#     skin_id = db.Column(db.String(50), primary_key=True)
#     unlocked_at = db.Column(db.DateTime, default=datetime.utcnow)

# def get_db_connection():
#     conn = psycopg2.connect(
#         host="localhost",
#         database="chessmate",
#         user="postgres",
#         password="starlord"
#     )
#     return conn

# @app.route('/')
# def index():
#     conn = get_db_connection()
#     cur = conn.cursor()
#     cur.execute('SELECT * FROM users;')
#     users = cur.fetchall()
#     cur.close()
#     conn.close()
#     return jsonify(users)

# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

# @app.route('/api/register', methods=['POST'])
# def register():
#     data = request.get_json()
#     user = user_datastore.create_user(
#         email=data['email'],
#         password=data['password'],
#         username=data['username']
#     )
#     db.session.commit()
#     return jsonify({"message": "User created"}), 201

@app.route('/user')
@auth_required()
def getUserDetails():
    return current_user.to_dict()
    


@app.route('/api/protected')
@auth_required()
def protected():
    return jsonify(message="This is protected")



# @socketio.on('join_game')
# def handle_join(data):
#     join_room(data['room_id'])
#     emit('player_joined', data, room=data['room_id'])

# @socketio.on('make_move')
# def handle_move(data):
#     # Broadcast the move to everyone else in the room
#     emit('opponent_move', data, room=data['room_id'], include_self=False)

# @socketio.on('leave_game')
# def handle_leave(data):
#     leave_room(data['room_id'])
#     emit('player_left', data, room=data['room_id'])





# Game state storage
games = {}
waiting_players = []

def generate_room_id():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

# Add these variables at the top level with other game state variables
connected_users = {}
user_rooms = {}

def authenticated_only(f):
    @functools.wraps(f)
    def wrapped(*args, **kwargs):
        if not request.sid in connected_users:
            disconnect()
        else:
            return f(*args, **kwargs)
    return wrapped

@socketio.on('connect')
def handle_connect():
    print(f"Client connected: {request.sid}")
    connected_users[request.sid] = None  # Will be set when they find_game

@socketio.on('disconnect')
def handle_disconnect():
    sid = request.sid
    print(f"Client disconnected: {sid}")
    username = connected_users.get(sid)
    
    if username:
        # Remove from waiting list if they were waiting
        if username in waiting_players:
            waiting_players.remove(username)
        
        # Handle active games
        room_id = user_rooms.get(username)
        if room_id and room_id in games:
            handle_leave({'room_id': room_id, 'username': username})
        
        # Cleanup
        if username in user_rooms:
            del user_rooms[username]
    
    if sid in connected_users:
        del connected_users[sid]

@socketio.on('find_game')
@authenticated_only
def handle_find_game(data):
    print(f"find_game event received from {data['username']}")
    username = data['username']
    connected_users[request.sid] = username
    
    # Join a personal room for this user
    join_room(username)
    
    print(f"Current waiting players: {waiting_players}")
    if waiting_players and waiting_players[0] != username:
        # Match with waiting player
        opponent = waiting_players.pop(0)
        room_id = generate_room_id()
        print(f"Matching {username} with {opponent} in room {room_id}")
        
        # Randomly assign colors
        players = [username, opponent]
        random.shuffle(players)
        white_player, black_player = players
        
        # Store room information
        user_rooms[white_player] = room_id
        user_rooms[black_player] = room_id
        
        games[room_id] = {
            'white': white_player,
            'black': black_player,
            'moves': [],
            'start_time': datetime.now().isoformat(),
            'status': 'active'
        }
        print(f"Game created in room {room_id}:")
        print(f"- White player: {white_player}")
        print(f"- Black player: {black_player}")
        
        # Send game_found event to white player
        white_data = {
            'room_id': room_id,
            'color': 'white',
            'opponent': black_player
        }
        emit('game_found', white_data, room=white_player)
        print(f"Sent to white player ({white_player}): {white_data}")
        
        # Send game_found event to black player
        black_data = {
            'room_id': room_id,
            'color': 'black',
            'opponent': white_player
        }
        emit('game_found', black_data, room=black_player)
        print(f"Sent to black player ({black_player}): {black_data}")
    else:
        if username not in waiting_players:
            waiting_players.append(username)
            print(f"Added {username} to waiting players. Current list: {waiting_players}")
        emit('waiting_for_opponent')
        print(f"Sent waiting_for_opponent to {username}")

@socketio.on('join_game')
@authenticated_only
def handle_join(data):
    room_id = data['room_id']
    username = data['username']
    print(f"join_game request from {username} for room {room_id}")
    
    if room_id in games:
        game = games[room_id]
        print(f"Game found: {game}")
        if username in [game['white'], game['black']]:
            join_room(room_id)
            print(f"{username} successfully joined room {room_id}")
            # Send current game state to the joining player
            emit('game_state', {
                'room_id': room_id,
                'white': game['white'],
                'black': game['black'],
                'moves': game['moves'],
                'status': game['status']
            })
            # Notify other player that opponent has joined
            emit('opponent_joined', {'username': username}, room=room_id, include_self=False)
        else:
            print(f"Unauthorized join attempt by {username} for room {room_id}")
            emit('error', {'message': 'Not authorized to join this game'})
    else:
        print(f"Room {room_id} not found for join request by {username}")
        emit('error', {'message': 'Game not found'})

@socketio.on('make_move')
@authenticated_only
def handle_move(data):
    room_id = data['room_id']
    username = data['username']
    print(f"Move received from {username} in room {room_id}")
    
    if room_id not in games:
        print(f"Room {room_id} not found for move by {username}")
        emit('error', {'message': 'Game not found'})
        return
        
    game = games[room_id]
    if username not in [game['white'], game['black']]:
        print(f"Unauthorized move attempt by {username} in room {room_id}")
        emit('error', {'message': 'Not authorized to make moves in this game'})
        return
        
    # Verify it's the player's turn
    is_white_turn = len(game['moves']) % 2 == 0
    is_white_player = username == game['white']
    if is_white_turn != is_white_player:
        print(f"Out of turn move attempt by {username} in room {room_id}")
        emit('error', {'message': 'Not your turn'})
        return
    
    move = {
        'from': data['from'],
        'to': data['to'],
        'fen': data['fen'],
        'timestamp': datetime.now().isoformat(),
        'player': username
    }
    
    game['moves'].append(move)
    print(f"Broadcasting move in room {room_id}: {move}")
    emit('opponent_move', move, room=room_id, include_self=False)
    # print(data)
    
    # Check for game end conditions
    # print(data['checkmate'])
    if data['checkmate']:
        game['status'] = 'completed'
        game['winner'] = username
        print(f"Game over in room {room_id} - {username} won by checkmate")
        emit('game_over', {
            'winner': username,
            'type': 'checkmate'
        }, room=room_id)

@socketio.on('resign')
def handle_resignation(data):
    room_id = data['room_id']
    username = data['username']
    
    if room_id in games:
        game = games[room_id]
        game['status'] = 'completed'
        game['winner'] = game['white'] if username == game['black'] else game['black']
        emit('game_over', {
            'winner': game['winner'],
            'type': 'resignation'
        }, room=room_id)

@socketio.on('leave_game')
def handle_leave(data):
    room_id = data['room_id']
    username = data['username']
    
    if room_id in games:
        game = games[room_id]
        leave_room(room_id)
        leave_room(username)
        
        if game['status'] == 'active':
            game['status'] = 'abandoned'
            game['winner'] = game['white'] if username == game['black'] else game['black']
            emit('game_over', {
                'winner': game['winner'],
                'type': 'abandonment'
            }, room=room_id)





# @app.route("/login", methods=['POST'])
# def login():
#         data = request.get_json()
#         user = User.query.filter_by(email=data['email']).first()
#         if user and user.verify_and_update_password(data['password']):
#             # Generate a session or token here
#             print("successful login")
#             return jsonify({"message": "Login successful"}), 200
#         return jsonify({"message": "Invalid credentials"}), 401



# # Views
# @app.route("/")
# @auth_required()
# def secure():
#     return current_user.to_dict()

# @app.route("/", methods=['GET', 'POST'])

# def home():
#     users = User.query.all()
#     users_list = [user.to_dict() for user in users]
#     return jsonify(users_list)


pgn = "1. e4 d5 2. exd5 e6 3. dxe6 fxe6 4. Qe2 Qd5 5. Qxe6+ Qxe6+ 6. Kd1 Qe1+"

@app.route("/load", methods=['GET'])
def load():
    return pgn




@app.route("/api/chess-news")
def chess_news():
    from openai import OpenAI

    YOUR_API_KEY = os.getenv('PERPLEXITY_API_KEY')

    from newsapi import NewsApiClient

    # Init
    newsapi = NewsApiClient(api_key=os.getenv('NEWSAPI'))

    # /v2/top-headlines
    top_headlines = newsapi.get_everything(q='chess', sort_by='publishedAt')

    # /v2/everything
    # all_articles = newsapi.get_everything(q='bitcoin',
    #                                     sources='bbc-news,the-verge',
    #                                     domains='bbc.co.uk,techcrunch.com',
    #                                     from_param='2017-12-01',
    #                                     to='2017-12-12',
    #                                     language='en',
    #                                     sort_by='relevancy',
    #                                     page=2)
    


    # /v2/top-headlines/sources
    # sources = newsapi.get_sources()

    return top_headlines


    # messages = [
    #     {
    #         "role": "system",
    #         "content": (
    #             "You have to collect the recent news about chess and output it into JSON format with summarized version of news in which each news contains a title, the summary, source of information and how old the information is"
    #         ),
    #     },
    #     {   
    #         "role": "user",
    #         "content": (
    #             "What are the recent news in the world of chess."
    #         ),
    #     },
    # ]

    # client = OpenAI(api_key=YOUR_API_KEY, base_url="https://api.perplexity.ai")

    # # chat completion without streaming
    # response = client.chat.completions.create(
    #     model="sonar-pro",
    #     messages=messages,
    # )
    # print(response)

    # # # chat completion with streaming
    # # response_stream = client.chat.completions.create(
    # #     model="sonar-pro",
    # #     messages=messages,
    # #     stream=True,
    # # )
    # # for response in response_stream:
    # #     print(response)
    


    # # after receiving the response
    # data = response.model_dump()   # or response.dict() in older versions
    # return jsonify(data)



if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)

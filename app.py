from boggle import Boggle
from flask import Flask, request, render_template, redirect, flash, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SECRET_KEY'] = "BogglesTheMind"
# app.debug = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

boggle_game = Boggle()

@app.route('/')
def show_homepage():
    """Display landing page and button to begin game"""
    
    if not session.get('high-score'):
        session['high-score'] = 0
        
    if not session.get('num-games'):
        session['num-games'] = 0

    return render_template('index.html')


@app.route('/game-board')
def handle_game_board():
    """Display game board, TODO"""
    
    board = boggle_game.make_board()
    session['game-board'] = board

    return render_template('game-board.html', board=board)


@app.route('/guess')
def check_guesses():
    """TODO"""
    
    guess = request.args.get('word')
    board = session.get('game-board')
    message = boggle_game.check_valid_word(board, guess)

    response = {"word": guess, "message": message}
    return jsonify(response)


@app.route('/play-again', methods=['POST'])
def play_again():
    """TODO"""
    
    score = request.json['score']
    session['high-score'] = score
    
    num_games = session.get('num-games', 0)
    num_games += 1
    session['num-games'] = num_games
    
    return jsonify(session['high-score']) 
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
    """Display landing page and button to begin game. Set session defaults."""
    
    session['high_score'] = session.get('high_score', 0)
    session['num_games'] = session.get('num_games', 0)

    return render_template('index.html')


@app.route('/game-board')
def handle_game_board():
    """Display game board"""
    
    board = boggle_game.make_board()
    session['game_board'] = board

    return render_template('game-board.html', board=board)


@app.route('/guess')
def check_guesses():
    """Check if a word is a valid word in the dictionary and/or the boggle board", and respond with a message accordingly."""
    
    word = request.args.get('word')
    board = session.get('game_board')
    message = boggle_game.check_valid_word(board, word)

    response = {"word": word, "message": message}
    return jsonify(response)


@app.route('/play-again', methods=['POST'])
def play_again():
    """
    Update session with the high score. Update session with number of games played.
    NB: JS is not using the return value. Return value could be anything.
    """
    
    current_high_score = session['high_score']
    score = request.json['score']

    session['high_score'] = current_high_score if current_high_score > score else score
    session['num_games'] = session.get('num_games', 0) + 1
    
    return jsonify(session['high_score']) 
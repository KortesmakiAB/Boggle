from boggle import Boggle
from flask import Flask, request, render_template, redirect, flash, session
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

    session['score'] = 0
    session['scored-words'] = []

    return render_template('index.html')

@app.route('/game-board')
def handle_game_board():
    """Display game board, TODO"""

    if not session['game-board']:
        board = boggle_game.make_board()
        session['game-board'] = board

        return render_template('game-board.html', board=board)
    else:
        board = session['game-board']

        return render_template('game-board.html', board=board)

@app.route('/guess', methods=['POST'])
def check_guesses():
    """TODO"""

    guess = request.form.get('word')
    board = session['game-board']
    message = boggle_game.check_valid_word(board, guess)
    flash(message)

    session['word'] = guess

    keeping_score(message, guess)

    return redirect('/game-board')

def keeping_score(message, guess):
    """TODO"""

    if message == 'ok':
        if guess not in session['scored-words']:
            session_scored_words(guess)

            score = session['score']
            score += len(guess)
            session['score'] = score
        else:
            flash(f"You already guessed {session['word']}")


def session_scored_words(guess):
    """TODO"""

    scored_words = session['scored-words']
    scored_words.append(guess)
    session['scored-words'] = scored_words

# def set_session(guess):
#     session['word'] = ''
#     word = session['word']
#     word.append(guess)
#     session['word'] = word
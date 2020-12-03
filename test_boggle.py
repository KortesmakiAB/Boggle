from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle

# Make Flask errors be real errors, not HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

class FlaskTests(TestCase):

    # '/'
    def test_index_template_and_base_html(self):
        with app.test_client() as client:
            resp =  client.get('/')
            html = resp.client.data(as_text, True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('<h3>The game I always lose because my wife always wins</h3>', html)
            self.assertIn('<script src="https://unpkg.com/axios/dist/axios.js"></script>', html)
            

    def test_begin_game_form(self):
        with app.test_client() as client:
            resp = client.post('/game-board', )
            html = resp.client.data(as_text, True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('<div id="play-again-div" class="hidden"></div>', html)

            
             



       
    def test_session_initial(self):
        with app.test_client() as client:

            self.assertEqual(session['high-score'], 1)
            self.assertEqual(session['num-games'], 1)

    def test_session_high(self):
        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session['high-score'] = 999
                change_session['num-games'] = 499

            self.assertEqual(session['high-score'], 1000)
            self.assertEqual(session['num-games'], 500)

    # '/game-board'
    def test_game_board_template(self):
        with app.test_client() as client:
            resp =  client.get('/game-board')
            html = resp.client.data(as_text, True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('<div id="play-again-div" class="hidden"></div>', html)
        
        "TODO"
        # are we making  a 5*5 board?
        # test the session
        

    # '/guess'
    def test_guess_route_response(self):
        with app.test_client() as client:
            resp =  client.get('/guess')
            json = resp.client.data(as_text, True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('TODO', json)

        "TODO"
       # check get request?
        # check_valid_word

    # '/play-again' (POST)
    def test_play_again_route_response(self):
        with app.test_client() as client:
            resp =  client.get('/play-again')
            json = resp.client.data(as_text, True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('TODO', json)
    
        "TODO"
        # test high-score with a high number and low number, set a default in the middle
        # test num-games, set a default value
        



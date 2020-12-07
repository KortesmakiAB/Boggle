from unittest import TestCase
from app import app, boggle_game
from flask import session
from boggle import Boggle


class FlaskTests(TestCase):

    # @classmethod
    # def tearDownClass(cls):
    #     session['board'] = None
    #     session['high-score'] = None
    #     session['num-games'] = None
    
    def setUp(self):
        """Before each test...
        Make Flask errors be real errors, not HTML pages with error info.
        Stop flask debug toolbar from running and interfering with tests (This is a bit of a hack)"""

        app.config['TESTING'] = True
        app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']


    def test_index_and_base_templates_html(self):
        """Test html for index.html and base.html. Also test status code"""

        with app.test_client() as client:
            resp =  client.get('/')
            html = resp.get_data(as_text=True)

            self.assertIn('<h3>The game I always lose because my wife always wins</h3>', html)
            self.assertIn('<script src="https://unpkg.com/axios/dist/axios.js"></script>', html)
            self.assertEqual(resp.status_code, 200)


    def test_session_initialize(self):
        """Test to make sure high score and number of games are initialized in session to zero"""

        with app.test_client() as client:
            client.get('/')

            self.assertEqual(session['high-score'], 0)
            self.assertEqual(session['num-games'], 0)


    def test_game_board_template(self):
        """Test html for game-board.html. Also test status code"""

        with app.test_client() as client:
            resp =  client.get('/game-board')
            html = resp.get_data(as_text=True)

            self.assertIn('<div id="play-again-div" class="hidden">', html)
            self.assertEqual(resp.status_code, 200)


    def test_valid_word(self):
        """Test is if a guess is valid by modifying board in the session. Also test response code.
        Assumes a 5 * 5 board"""

        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session['board'] = [['T','A','C','O','C'],
                                            ['A','T','T','A','C'],
                                            ['O','C','A','T','T'],
                                            ['A','C','O','C','A'],
                                            ['T','T','A','C','O']]
            
            resp = client.get('/guess?word=taco')
           
            self.assertEqual(resp.json['word'], 'taco')
            self.assertEqual(resp.json['message'], 'a valid response')
            self.assertEqual(resp.status_code, 200) 
    

    def test_word_not_on_board(self):
        """Test if a guess is a valid word but not on the board."""

        with app.test_client() as client:
            resp = client.get('/guess?word=developer')

            self.assertEqual(resp.json['word'], 'developer')
            self.assertEqual(resp.json['message'], 'not on the board')


    def test_not_a_word(self):
        """Test if a guess is not a valid word"""

        with app.test_client() as client:
            resp = client.get('/guess?word=tacocat')

            self.assertEqual(resp.json['word'], 'tacocat')
            self.assertEqual(resp.json['message'], 'not a word')


    def test_session_high_score_higher(self):
        """Test pay-again POST route, if high score in session is updated when a higher score is passed in. Also test status code."""

        with app.test_client() as client:
            resp =  client.post('/play-again', json={'score': '987'})
            # resp =  client.post('/play-again')

            self.assertEqual(resp.json['high-score'], '987' )
            self.assertEqual(resp.status_code, 200)
    

    def test_session_high_score_lower_and_num_games(self):
        """Test if high score in session remains the same when a lower score is passed in. 
        Also test if number of games is incremented"""        

        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session['high-score'] = 499
                change_session['num-games'] = 399

            resp = client.post('/play-again', {'score': 321})

            self.assertEqual(resp.json['high-score'], 499)
            self.assertEqual(session['num-games'], 400)



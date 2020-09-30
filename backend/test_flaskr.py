import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = f'postgresql://postgres:solidsnake208@localhost:5432/{self.database_name}'
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    # Testing getting all the categories
    def test_all_categories(self):
        res = self.client().get('/categories')
        res_data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res_data['categories'],
                    {'1': "Science", '2': "Art", '3': "Geography", '4': "History", '5': "Entertainment", '6': "Sports"})
        self.assertTrue(res_data['categories'])

    #--------------------------------------
    # Testing getting question
    #--------------------------------------
    # Success Case
    def test_all_questions(self):
        res = self.client().get('/questions')
        res_data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res_data['total_questions'], 19)
        self.assertTrue(res_data['categories'])
        self.assertTrue(res_data['questions'])

    # Error Case
    def test_404_all_questions(self):
        res = self.client().get('/questions?page=1000')
        res_data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(res_data['message'], "Not found")
        self.assertFalse(res_data['success'])
        self.assertTrue(res_data['error'])

    # --------------------------------------
    # Testing deleting a question
    # --------------------------------------
    # Success Case (Note it succeeded but now it fails because it has already been deleted)
    def test_delete_question(self):
        res = self.client().delete('/questions/15')
        res_data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res_data['total_questions'], 18)
        self.assertTrue(res_data['success'])
        self.assertTrue(res_data['deleted_question_id'])

    # Error Case
    def test_404_delete_question(self):
        res = self.client().delete('/questions/15')
        res_data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(res_data['message'], "Not found")
        self.assertFalse(res_data['success'])
        self.assertTrue(res_data['error'])

    # --------------------------------------
    # Testing posting a question
    # --------------------------------------
    # Success Case
    def test_post_question(self):
        data = {
            'question': "What is the movie that was released in 1999 and had Edward Norton and Brad Pitt?",
            'answer': "Fight Club",
            'category': 5,
            'difficulty': 2,
        }
        res = self.client().post('/questions', json=data)
        res_data = json.loads(res.data)

        self.assertEqual(res.status_code, 201)
        self.assertEqual(res_data['total_questions'], 19)
        self.assertTrue(res_data['success'])
        self.assertTrue(res_data['question_id'])

    # Error Case 1
    def test_422_post_question(self):
        res = self.client().post('/questions', json='foo bar baz')
        res_data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(res_data['message'], "please provide valid fields in your request body")
        self.assertFalse(res_data['success'])
        self.assertTrue(res_data['error'])

    # --------------------------------------
    # Testing searching a question
    # --------------------------------------
    # Success Case
    def test_search_question(self):
        data = {
            'searchTerm': "Norton"
        }
        res = self.client().post('/questions/search', json=data)
        res_data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res_data['total_questions'], 1)
        self.assertTrue(res_data['questions'])
        self.assertTrue(res_data['current_category'])

    # Error Case
    def test_422_search_question(self):
        res = self.client().post('/questions/search', json='foo bar baz')
        res_data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(res_data['message'], "please provide valid fields in your request body")
        self.assertFalse(res_data['success'])
        self.assertTrue(res_data['error'])

    # --------------------------------------
    # Testing getting questions in a category
    # --------------------------------------
    # Success Case
    def test_get_question_in_category(self):
        res = self.client().get('/categories/4/questions')
        res_data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(res_data['total_questions'])
        self.assertTrue(res_data['questions'])
        self.assertTrue(res_data['current_category'])

    # Error Case
    def test_404_get_question_in_category(self):
        res = self.client().get('/categories/22/questions')
        res_data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(res_data['message'], "Not found")
        self.assertFalse(res_data['success'])
        self.assertTrue(res_data['error'])

    # --------------------------------------
    # Testing playing the game
    # --------------------------------------
    # Success Case
    def test_play_game(self):
        data = {
            "quiz_category": {
                "id": 6,
                "type": "Sports"
            },
            "previous_questions": [1, 4, 5, 9]
        }
        res = self.client().post('/quizzes', json=data)
        res_data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(res_data['question'])

    # Error Case
    def test_422_play_game(self):
        data = {
            "quiz_category": {
                "id": 'foo',
                "type": "Sports"
            },
            "previous_questions": [1, 4, 5, 9]
        }
        res = self.client().post('/quizzes', json=data)
        res_data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(res_data['message'], "please provide valid fields in your request body")
        self.assertFalse(res_data['success'])
        self.assertTrue(res_data['error'])


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()

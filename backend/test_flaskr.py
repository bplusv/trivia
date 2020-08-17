import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""

        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}/{}".format('localhost:5432',
                                                         self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after each test"""
        pass

    def test_get_categories(self):
        res = self.client().get('/categories')
        body = res.get_json()
        self.assertTrue(body)
        self.assertEqual(res.status_code, 200)

    def test_get_questions(self):
        res = self.client().get('/questions?page=1')
        body = res.get_json()
        self.assertTrue(body['questions'])
        self.assertTrue(body['total_questions'])
        self.assertTrue(body['categories'])
        self.assertTrue(body['current_category'])
        self.assertEqual(res.status_code, 200)

    def test_get_questions_page_not_found(self):
        res = self.client().get('/questions?page=99')
        body = res.get_json()
        self.assertEqual(body['success'], False)
        self.assertEqual(body['error'], 404)
        self.assertEqual(body['message'], 'entity not found')
        self.assertEqual(res.status_code, 404)

    def test_delete_question(self):
        question_id = 5
        res = self.client().delete(f'/questions/{question_id}')
        body = res.get_json()
        self.assertTrue(body['success'])
        self.assertEqual(res.status_code, 200)
        self.assertIsNone(Question.query.get(question_id))

    def test_delete_question_not_found(self):
        question_id = 99
        res = self.client().delete(f'/questions/{question_id}')
        body = res.get_json()
        self.assertEqual(body['success'], False)
        self.assertEqual(body['error'], 404)
        self.assertEqual(body['message'], 'entity not found')
        self.assertEqual(res.status_code, 404)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()

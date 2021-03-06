import unittest

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
        self.assertTrue(body['categories'])
        self.assertEqual(res.status_code, 200)

    def test_get_questions(self):
        res = self.client().get('/questions?page=1')
        body = res.get_json()
        self.assertTrue(body['questions'])
        self.assertTrue(body['total_questions'])
        self.assertTrue(body['categories'])
        self.assertEqual(body['current_category'], 0)
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
        self.assertEqual(body['success'], True)
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

    def test_post_question(self):
        data = {
            'question': 'Who invented the Lambda calculus?',
            'answer': 'Alonzo Church',
            'difficulty': 3,
            'category': 1,
            'rating': 1
        }
        res = self.client().post('/questions', json=data)
        body = res.get_json()
        self.assertEqual(body['success'], True)
        self.assertTrue(body['question_id'])
        self.assertEqual(res.status_code, 200)
        question = Question.query.get(body['question_id'])
        self.assertTrue(question)
        self.assertEqual(question.question, data['question'])
        self.assertEqual(question.answer, data['answer'])
        self.assertEqual(question.difficulty, data['difficulty'])
        self.assertEqual(question.category, data['category'])

    def test_post_question_unprocessable(self):
        data = {
            'question': 'Who invented the Lambda calculus?',
            'answer': 'Alonzo Church',
            'difficulty': 'hard',
            'category': 'science',
            'rating': -1
        }
        res = self.client().post('/questions', json=data)
        body = res.get_json()
        self.assertEqual(body['success'], False)
        self.assertEqual(body['error'], 422)
        self.assertEqual(body['message'], 'unprocessable entity')
        self.assertEqual(res.status_code, 422)

    def test_search_questions(self):
        res = self.client().post('/questions', json={'searchTerm': 'cassius'})
        body = res.get_json()
        self.assertTrue(body['questions'])
        self.assertTrue(body['total_questions'])
        self.assertEqual(body['current_category'], 0)
        self.assertEqual(res.status_code, 200)

    def test_search_questions_no_results(self):
        res = self.client().post('/questions', json={'searchTerm': 'zzzzzzz'})
        body = res.get_json()
        self.assertFalse(body['questions'])
        self.assertTrue(body['total_questions'])
        self.assertEqual(body['current_category'], 0)
        self.assertEqual(res.status_code, 200)

    def test_get_questions_by_category(self):
        category_id = 1
        res = self.client().get(f'/categories/{category_id}/questions')
        body = res.get_json()
        self.assertTrue(body['questions'])
        self.assertTrue(body['total_questions'])
        self.assertEqual(body['current_category'], category_id)
        self.assertEqual(res.status_code, 200)

    def test_get_questions_by_category_no_results(self):
        category_id = 99
        res = self.client().get(f'/categories/{category_id}/questions')
        body = res.get_json()
        self.assertFalse(body['questions'])
        self.assertTrue(body['total_questions'])
        self.assertTrue(body['current_category'])
        self.assertEqual(res.status_code, 200)

    def test_get_quizzes_next_question_with_category(self):
        data = {
            'previous_questions': [10],
            'quiz_category': {'id': 6, 'type': 'Sports'}
        }
        res = self.client().post('/quizzes', json=data)
        body = res.get_json()
        self.assertTrue(body['question'])
        self.assertEqual(body['question']['id'], 11)
        self.assertEqual(res.status_code, 200)

    def test_get_quizzes_next_question_without_category(self):
        data = {
            'previous_questions': [],
            'quiz_category': {'id': 0, 'type': 'click'}
        }
        res = self.client().post('/quizzes', json=data)
        body = res.get_json()
        self.assertTrue(body['question'])
        self.assertEqual(res.status_code, 200)

    def test_get_quizzes_next_question_force_end(self):
        data = {
            'previous_questions': [10, 11],
            'quiz_category': {'id': 6, 'type': 'Sports'}
        }
        res = self.client().post('/quizzes', json=data)
        body = res.get_json()
        self.assertIsNone(body['question'])
        self.assertEqual(res.status_code, 200)

    def test_post_category(self):
        data = {
            'new_category': 'animation'
        }
        res = self.client().post('/categories', json=data)
        body = res.get_json()
        self.assertEqual(body['success'], True)
        self.assertTrue(body['category_id'])
        self.assertEqual(res.status_code, 200)
        category = Category.query.get(body['category_id'])
        self.assertEqual(category.type, data['new_category'])

    def test_post_category_unprocessable(self):
        data = {
            'new_category': None
        }
        res = self.client().post('/categories', json=data)
        body = res.get_json()
        self.assertEqual(body['success'], False)
        self.assertEqual(body['error'], 422)
        self.assertEqual(body['message'], 'unprocessable entity')
        self.assertEqual(res.status_code, 422)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()

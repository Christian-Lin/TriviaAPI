import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}/{}".format(
            'chris:admin@localhost:5432', self.database_name)
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

    # Test getting category endpoints and checks responses
    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        # In this case, we only have 6 categories. In case that more categories
        # are added, this has to be changed.
        self.assertEqual(len(data['categories']), 6)

    # Test paginated questions
    def test_get_pagination(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))
        self.assertTrue(len(data['categories']))

    # Test sending a 404 on a non-existing page (i.e. beyond range)
    def test_get_page_not_found_404(self):
        res = self.client().get('/questions?page=1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not found')

    # Create new question, then test its deletion
    def test_delete_question(self):
        # Create new question
        question = Question(
            question='delete question',
            answer='delete answer',
            category=1,
            difficulty=1
        )
        question.insert()
        question_id = question.id

        # Test its deletion
        res = self.client().delete(f'/questions/{question_id}')
        data = json.loads(res.data)

        question = Question.query.filter(
            Question.id == question.id).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        # self.assertEqual(data['deleted'], question_id)

    # Test error 404 (not found) on deleting an invalid question
    def test_delete_invalid_question_404(self):
        res = self.client().delete('/questions/asdasdasd@#!(&*$')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not found')

    # Test adding a new question
    def test_new_question(self):
        # Add new question as dict, default diff and cat as 1
        new_question = {
            'question': 'new question test',
            'answer': 'new answer test',
            'difficulty': 1,
            'category': 1
        }
        # Check all questions before, and after adding new question
        original_questions = len(Question.query.all())
        res = self.client().post('/questions', json=new_question)
        data = json.loads(res.data)
        modified_questions = len(Question.query.all())

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        # Assert that only one question was added, test +1 from original
        # questions
        self.assertEqual(modified_questions, original_questions + 1)

    # Test posting without an answer - should send a 422 (Unprocessable)
    def test_new_question_empty_answer(self):
        empty_answer = {
            'question': 'question without answer',
            'answer': '       ',
            'category': 1,
            'difficulty': 1
        }
        res = self.client().post('/questions', json=empty_answer)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable')

    # Test getting all the questions in a category
    def test_get_questions_from_category(self):
        res = self.client().get('/categories/2/questions')
        data = json.loads(res.data)

        self.assertEqual(data['success'], True)
        # Should return 4 questions for category 2 (Art) - as per original db
        self.assertEqual(data['total_questions'], 4)

    # Test error 404 (not found) for getting a question for a non-existent
    # category
    def test_get_questions_from_category_404(self):
        res = self.client().get('/categories/1000/questions')
        data = json.loads(res.data)

        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'Not found')

    # Test search for words in a question
    def test_search(self):
        search = {
            'searchTerm': 'boxer'
        }
        res = self.client().post('/questions/search', json=search)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['questions'][0]['id'], 9)

    # Test for the quiz, on category 'Art' (id of 2)
    def test_play_quiz(self):
        new_quiz = {
            'previous_questions': [],
            'quiz_category': {'type': 'Art', 'id': 2}
        }

        res = self.client().post('/quizzes', json=new_quiz)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    # Test error 422 (Unprocessable) for the quiz, on non-existent cat id
    def test_play_quiz_422(self):
        new_quiz = {
            'previous_questions': [0],
            'quiz_category': {"type": "Geography"}
        }
        res = self.client().post('/quizzes', json=new_quiz)
        data = json.loads(res.data)

        self.assertEqual(data['error'], 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Unprocessable")


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()

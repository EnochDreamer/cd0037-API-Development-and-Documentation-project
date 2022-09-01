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
        self.database_path = "postgresql://enoch:enoch@{}/{}".format('localhost:5432', self.database_name)
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
    def test_get_categories(self):
        response=self.client().get('/categories')
        data=json.loads(response.data)
        self.assertEqual(response.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(len(data['categories']))

    def test_404_if_wrong_endpoint(self):
        response=self.client().get('/cater')
        data=json.loads(response.data)
        self.assertEqual(response.status_code,404)
        self.assertEqual(data['message'] , "resource not found")
        self.assertEqual(data["success"], False)



    def test_get_questions(self):
        response=self.client().get('/questions')
        data=json.loads(response.data)
        self.assertEqual(response.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'])

    def test_404_if_invalid_page(self):
        response=self.client().get('/questions?page=50000')
        data=json.loads(response.data)
        self.assertEqual(response.status_code,404)
        self.assertEqual(data['message'] , "resource not found")
        self.assertEqual(data["success"], False)


    def test_create_questions(self):
        questions_count=len(Question.query.all())
        response=self.client().post('/questions', json={
            "question":"What's you favorite movie",
            "answer":"flash",
            "difficulty":2,
            "category":"2"
        })
        data=json.loads(response.data)
        self.assertEqual(response.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(len(data['questions']))
        self.assertTrue(data["created"])
        self.assertTrue(len(data["categories"]))
        self.assertEqual(data['total_questions'],(questions_count+1))

    def test_400_if_no_data_sent(self):
        response=self.client().post('/questions')
        data=json.loads(response.data)
        self.assertEqual(response.status_code,400)
        self.assertEqual(data['message'] , "Bad request")
        self.assertEqual(data["success"], False)



    def test_delete_question(self):
        question=Question.query.first()
        id=question.id
        response=self.client().delete(f'/questions/{id}')
        data=json.loads(response.data)
        deleted_question=Question.query.filter_by(id=id).one_or_none()
        self.assertEqual(response.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertEqual(data['deleted'],id)
        self.assertEqual(deleted_question,None)
        self.assertTrue(len(data['questions']))
        self.assertTrue(len(data['categories']))
        self.assertTrue(data['total_questions'])

    def test_422_if_question_id_does_not_exist(self):
        response=self.client().delete('/questions/2000')
        data=json.loads(response.data)
        self.assertEqual(response.status_code,422)
        self.assertEqual(data['message'] , "could not process recource")
        self.assertEqual(data["success"], False)



    def test_search_questions(self):
        response=self.client().post('/questions/search', json={"searchTerm":"what"})
        data=json.loads(response.data)
        self.assertEqual(response.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(len(data['questions']))
        self.assertTrue(data["searchTerm"])
        self.assertTrue(len(data["categories"]))

    def test_400_if_search_does_not_exist(self):
        response=self.client().post('/questions/search')
        data=json.loads(response.data)
        self.assertEqual(response.status_code,400)
        self.assertEqual(data['message'] , "Bad request")
        self.assertEqual(data["success"], False)


    def test_get_questions_per_category(self):
        category="2"
        response=self.client().get(f'categories/{category}/questions')
        data=json.loads(response.data)
        self.assertEqual(response.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'])
        self.assertEqual(data['current_category'],int(category))

    def test_404_if_category_does_not_exist(self):
        response=self.client().get('categories/3000/questions')
        data=json.loads(response.data)
        self.assertEqual(response.status_code,404)
        self.assertEqual(data['message'] , "resource not found")
        self.assertEqual(data["success"], False)


    def test_play_the_game(self):
        response=self.client().post('/quizzes', json={
            "previous_questions":[],
            "quiz_category":{"id":"2"}

        })
        data=json.loads(response.data)
        self.assertEqual(response.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['question'])
        self.assertEqual(len(data["previousQuestions"]),0)

    def test_500_if_previous_question_malfunctions(self):
        response=self.client().post('/quizzes' , json={
            "previous_questions":None,
            "quiz_category":{"id":"1000"}})
        data=json.loads(response.data)
        self.assertEqual(response.status_code,500)
        self.assertEqual(data['message'] , "internal server error")
        self.assertEqual(data["success"], False)

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
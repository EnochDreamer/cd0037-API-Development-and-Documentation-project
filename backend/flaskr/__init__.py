import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category
# a helper functions that pagination of questions and returns max. 10 questions per page
QUESTIONS_PER_PAGE = 10
def paginate_items(request , items):
  page=request.args.get('page' ,1 , type=int)
  start=(page-1)*QUESTIONS_PER_PAGE
  end=start + QUESTIONS_PER_PAGE
  items_list=[item.format() for item in items]
  result=items_list[start:end]
  return result

# a helper function for type formatting
def toDict(entries):
  result={}
  for entry in entries:
    result[entry.id]=entry.type
  return result


# Creates the app and database setup
def create_app(test_config=None):
  app = Flask(__name__)
  setup_db(app)
  # enables CORS for any origin with the specified URI 
  CORS(app , resources={r"\*/api/\*":{"origins":"*"}})
  # Access control setups
  @app.after_request
  def after_request(response):
      response.headers.add(
          "Access-Control-Allow-Headers", "Content-Type,Authorization, true"
      )
      response.headers.add(
          "Access-Control-Allow-Methods", "GET,POST,DELETE,OPTIONS"
      )
      return response

  # an endpoint to get all available categories
  @app.route('/categories')
  def get_categories(): 
    try:
      categories=Category.query.order_by(Category.id).all()
      return jsonify ({
        "success":True,
        "categories":toDict(categories)
      })
    except:
      abort(404)

  # an end point to get paginated question of max. 10 per page
  @app.route('/questions')
  def get_questions():
    questions=Question.query.order_by(Question.id).all()
    categories=Category.query.all()
    paginated_questions=paginate_items(request , questions)
    if len(paginated_questions)==0:
      abort(404)
    return jsonify({
      "success":True,
      "questions":paginated_questions,
      "total_questions":len(questions),
      "categories":toDict(categories),
      "current_category":None
    })
    
 # an endpoint to delete a specific question
  @app.route('/questions/<int:question_id>' , methods=['DELETE'])
  def delete_question(question_id):
    try:
      question=Question.query.filter_by(id=question_id).one_or_none()
      if question is None:
        abort(404)
      question.delete()
      questions=Question.query.order_by(Question.id).all()
      categories=Category.query.all()
      paginated_questions=paginate_items(request, questions)
      return jsonify({
        "success":True,
        "deleted":question_id,
        "questions":paginated_questions,
        "total_questions":len(questions),
        "categories":toDict(categories),
        "current_category":None
      })
    except:
      abort(422)
    
  # an endpoint to create a new question
  @app.route('/questions', methods=['POST'])
  def create_question():
    
      new_question=request.get_json()['question']
      new_answer=request.get_json()['answer']
      new_difficulty=request.get_json()['difficulty']
      new_category=request.get_json()['category']
      question=Question(question=new_question , answer=new_answer , difficulty=new_difficulty , category=new_category)
      #Ensure no null field
      if (new_answer and new_category and new_difficulty and new_question):
        try:
          question.insert()
          questions=Question.query.order_by(Question.id).all()
          categories=Category.query.all()
          paginated_questions=paginate_items(request, questions)
          if len(paginated_questions)==0:
            abort(404)
          return jsonify({
          "success":True,
          "created":question.id,
          "questions":paginated_questions,
          "total_questions":len(questions),
          "categories":toDict(categories),
          "current_category":None
          })
        except:
          #clear pending trnsactions
          question.rollback()
          abort(422)
        finally:
          # close session to free up system resources
          question.close()
       
      else:
        abort(400)
      
    
    
  @app.route('/questions/search' , methods=['POST'])
  def search_question():
    search_term= request.get_json().get('searchTerm')
    # make search input required
    if search_term:
      results=Question.query.filter(Question.question.ilike(f'%{(search_term)}%')).all()
      categories=Category.query.all()
      paginated_questions=paginate_items(request, results)
      if len(paginated_questions)==0:
        abort(404)
      return jsonify({
        "success":True,
        "searchTerm":search_term,
        "questions":paginated_questions,
        "total_questions":len(results),
        "categories":toDict(categories),
        "current_category":None
      })
    else:
      abort(400)
    
# an endpoint to get questions of a specific category paginated
  @app.route('/categories/<int:category_id>/questions')
  def Get_categories(category_id):
    questions=Question.query.filter_by(category=category_id).all()
    categories=Category.query.all()
    paginated_questions=paginate_items(request, questions)
    if len(paginated_questions)==0:
      abort(404)
    return jsonify({
      "success":True,
      "questions":paginated_questions,
      "total_questions":len(questions),
      "categories":toDict(categories) ,
      "current_category": category_id
    })

  # the endpoint to play the game
  @app.route('/quizzes', methods=['POST'])
  def quiz():
    #gets quiz category and previous questions
    category=request.get_json()['quiz_category']
    previous_questions=request.get_json()['previous_questions']
    if previous_questions is None:
      abort(500)
    if ('quiz_category' and 'previous_questions') not in request.get_json():
      abort(400)
    if category['id']==0:
      questions=Question.query.all()
    else:
      questions=Question.query.filter_by(category=category['id']).all()
      #creates a list of formated questions with id not in previous questions
    list_of_valid_questions=[question.format()   for question in questions if (question.id not in previous_questions)]
    if len(list_of_valid_questions)!=0:
      # generates a random index 
      next_question_index = random.randrange(0, len(list_of_valid_questions))
      # picks a next question
      next_question=list_of_valid_questions[next_question_index]
    elif len(list_of_valid_questions)==0:
      # Notifies the frontend to end quiz if no new question left
      next_question=None
    return jsonify({
      "success": True,
      "question":next_question,
      "previousQuestions":previous_questions
    })
    

# Error handlers
  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": "Bad request"
    }),400

  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "resource not found"
    }), 404

  @app.errorhandler(422)
  def not_processable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "could not process recource"
    }), 422

  @app.errorhandler(500)
  def server_error(error):
    return jsonify({
        "success": False,
        "error": 500,
        "message": "internal server error"
    }), 500




  return app

    
import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

# Pagination
def paginate(request, selection):
  page = request.args.get('page', 1, type=int) # Set page 1 as default
  start = (page - 1) * QUESTIONS_PER_PAGE
  end = start + QUESTIONS_PER_PAGE

  questions = [question.format() for question in selection[start:end]] # Perform slicing on selection
  return questions

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  '''
  @TODO(DONE): Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  CORS(app)
  '''
  @TODO(DONE): Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization, true')
    response.headers.add('Access-Control-Allow-Methods','GET,PATCH,POST,DELETE,OPTIONS')
    return response
  '''
  @TODO(DONE): 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/categories')
  def get_categories():
    categories = Category.query.order_by(Category.type).all()

    # Send a 404 not found if it doesn't exist
    if len(categories) == 0:
      abort(404)
    
    return jsonify({
      'success': True,
      'categories': {category.id: category.type for category in categories}
    })

  '''
  @TODO(DONE): 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''
  @app.route('/questions')
  def get_questions():
    questions = Question.query.order_by(Question.id).all() # Sort the questions by ID
    page_questions = paginate(request, questions) # Paginate the selected questions

    categories = Category.query.order_by(Category.type).all() # Sort by category type

    # Send a 404 not found if question doesn't exist
    if len(page_questions) == 0:
      abort(404)
    
    return jsonify({
      'success': True,
      'questions': page_questions,
      'total_questions': len(questions),
      'categories': {category.id: category.type for category in categories},
      'current_category': None
    })
  
  '''
  @TODO(DONE): 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route("/questions/<int:question_id>", methods=['DELETE'])
  def delete_question(question_id):
    # If question id does not exist
    if not question:
      abort(404)
    else:
      try:
        question = Question.query.get(question_id)
        question.delete()
        return jsonify({
          'success': True,
          'deleted:': question_id
        })
      except:
        abort(422) # Unable to process request

  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
  @app.route("/questions", methods=['POST'])
  def add_question():
    body = request.get_json()
    # If all required sections are not in the request response, send a 422 unable to process
    if not ('question' in body and 'answer' in body and 'difficulty' in body and 'category' in body):
      abort(422)

    # Add new question with required info
    new_question = body.get('question')
    new_answer = body.get('answer')
    new_difficulty = body.get('difficulty')
    new_category = body.get('category')

    # Populate new information into the database
    try:
      question = Question(question=new_question, answer=new_answer, difficulty=new_difficulty, category=new_category)
      question.insert()

      return jsonify({
        'success': True,
        'created': question.id,
      })
    # Abort if there is a problem creating new question - unable to process request
    except:
      abort(422)
  
  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''
  @app.route('/questions/search', methods=['POST'])
  def search_questions():
    body = request.get_json()
    search_term = body.get('searchTerm', None)
    # Filter search by insensitive to case (ilike)
    if search_term:
      search_results = Question.query.filter(Question.question.ilike(f'%{search_term}%')).all()

      return jsonify({
        'success': True,
        'questions': [question.format() for question in search_results], # Show all questions based on result
        'total_questions': len(search_results),
        'current_category': None
      })
    else:
      abort(404)
  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route('/categories/<int:category_id>/questions', methods=['GET'])
  def get_category_questions(category_id):
    questions = Question.query.filter(Question.category == str(category_id)).all()
    page = paginate(request, questions) # Paginate search, in case too many are found
    # If the page does not exist, send a 404 not found
    if len(page) == 0:
      abort(404)

    return jsonify({
      'success': True,
      'questions': page,
      'total_questions': len(questions),
      'current_category': category_id
    })


  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''
  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  
  return app

    
import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


# Pagination
def paginate(request, selection):
    # Set page 1 as default
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    # Perform slicing on selection
    questions = [question.format() for question in selection[start:end]]
    return questions


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    CORS(app)

    @app.after_request
    def after_request(response):
        response.headers.add(
            'Access-Control-Allow-Headers',
            'Content-Type, Authorization, true')
        response.headers.add(
            'Access-Control-Allow-Methods',
            'GET,PATCH,POST,DELETE,OPTIONS')
        return response

    @app.route('/categories')
    def get_categories():
        categories = Category.query.order_by(Category.type).all()

        # Send a 404 not found if it doesn't exist
        if len(categories) == 0:
            abort(404)

        return jsonify({'success': True, 'categories': {
                       category.id: category.type for category in categories}})

    @app.route('/questions')
    def get_questions():
        questions = Question.query.order_by(
            # Sort the questions by ID
            Question.id).all()
        # Paginate the selected questions
        page_questions = paginate(request, questions)

        # Sort by category type
        categories = Category.query.order_by(
            Category.type).all()

        # Send a 404 not found if question doesn't exist
        if len(page_questions) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'questions': page_questions,
            'total_questions': len(questions),
            'categories': {
                category.id: category.type for category in categories
            },
            'current_category': None
        })

    @app.route("/questions/<int:question_id>", methods=['DELETE'])
    def delete_question(question_id):
        question = Question.query.get(question_id)
        # If question id does not exist
        if not question:
            abort(404)
        else:
            try:
                question.delete()
                return jsonify({
                    'success': True,
                    'deleted:': question_id
                })
            # Unable to process request
            except BaseException:
                abort(422)

    @app.route("/questions", methods=['POST'])
    def add_question():
        body = request.get_json()
        # If all required sections are not in the request response, send a 422
        # unable to process
        if (body.get('question').strip() == "") or (
                body.get('answer').strip() == ""):
            abort(422)

        # Add new question with required info
        new_question = body.get('question')
        new_answer = body.get('answer')
        new_difficulty = body.get('difficulty')
        new_category = body.get('category')

        # Populate new information into the database
        try:
            question = Question(
                question=new_question,
                answer=new_answer,
                difficulty=new_difficulty,
                category=new_category)
            question.insert()

            return jsonify({
                'success': True,
                'created': question.id,
            })

        # Abort if there is a problem creating new question - unable to process
        # request
        except BaseException:
            abort(422)

    @app.route('/questions/search', methods=['POST'])
    def search_questions():
        body = request.get_json()
        search_term = body.get('searchTerm', None)
        # Filter search by case insensitive (ilike)
        if search_term:
            search_results = Question.query.filter(
                Question.question.ilike(f'%{search_term}%')).all()

            return jsonify({
                'success': True,
                # Show all questions based on result
                'questions': [question.format() for
                              question in search_results],
                'total_questions': len(search_results)
            })
        abort(404)

    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def get_category_questions(category_id):
        questions = Question.query.filter(
            Question.category == str(category_id)).all()
        # Paginate search, in case too many are found
        page = paginate(request, questions)
        # If the page does not exist, send a 404 not found
        if len(page) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'questions': page,
            'total_questions': len(questions),
            'current_category': category_id
        })

    @app.route('/quizzes', methods=['POST'])
    def play_quiz():

        body = request.get_json()

        try:
            category = body.get('quiz_category')
            # If category is "ALL" query all questions, else filter by category
            if category['type'] == 'click':
                questions = Question.query.all()
            else:
                questions = Question.query.filter_by(
                    category=str(category['id'])).all()
        # Category must exist, otherwise send a 422 unable to process
        except BaseException:
            abort(422)

        questions = [question.format() for question in questions]

        try:
            previous_question = body.get('previous_questions')
            # Filter a new list of questions to exclude previous ones
            new_questions = []
            for question in questions:
                if question['id'] not in previous_question:
                    new_questions.append(question)
            # End quiz if all questions are answered, else return a random
            # question from the new list
            if len(new_questions) == 0:
                return jsonify({
                    'success': True
                })
            question = random.choice(new_questions)
            return jsonify({
                'success': True,
                'question': question
            })
        except BaseException:
            abort(400)

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad request"
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "Unprocessable"
        }), 422

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "Internal server error"
        })

    return app

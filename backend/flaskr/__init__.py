import math
import os
import random

from flask import Flask, request, abort, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.exceptions import NotFound

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PATCH,POST,DELETE,OPTIONS')
        return response

    @app.route('/categories', methods=['GET'])
    def get_categories():
        try:
            categories = Category.query.order_by(Category.id.asc()).all()
            return jsonify([category.format() for category in categories])
        except Exception:
            abort(500)

    @app.route('/questions', methods=['GET'])
    def get_questions():
        try:
            page = request.args.get('page', 1, type=int)
            total_questions = Question.query.count()
            last_page = math.ceil(total_questions / QUESTIONS_PER_PAGE)
            if (page < 1) or (page > last_page):
                abort(404)
            offset = (page - 1) * QUESTIONS_PER_PAGE
            questions = Question.query.order_by(Question.id.asc())\
                .offset(offset).limit(QUESTIONS_PER_PAGE).all()
            categories = Category.query.order_by(Category.id.asc()).all()
            return jsonify({
                'questions': [question.format() for question in questions],
                'total_questions': total_questions,
                'categories': {category.id: category.type
                               for category in categories},
                'current_category': '<placeholder>'
            })
        except NotFound:
            abort(404)
        except Exception:
            abort(500)

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            question = Question.query.get(question_id)
            if not question:
                abort(404)
            question.delete()
            return jsonify({
                'success': True
            })
        except NotFound:
            abort(404)
        except Exception:
            abort(500)

    '''
    @TODO: 
    Create an endpoint to POST a new question, 
    which will require the question and answer text, 
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab, 
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.  
    '''
    @app.route('/questions', methods=['POST'])
    def post_question():
        try:
            data = request.get_json()
            question = Question(**data)
            question.insert()
            return jsonify({
                'success': True
            })
        except SQLAlchemyError:
            abort(422)
        except Exception:
            abort(500)


    '''
    @TODO: 
    Create a POST endpoint to get questions based on a search term. 
    It should return any questions for whom the search term 
    is a substring of the question. 

    TEST: Search by any phrase. The questions list will update to include 
    only question that include that string within their question. 
    Try using the word "title" to start. 
    '''

    '''
    @TODO: 
    Create a GET endpoint to get questions based on category. 

    TEST: In the "List" tab / main screen, clicking on one of the 
    categories in the left column will cause only questions of that 
    category to be shown. 
    '''


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

    @app.errorhandler(400)
    def bad_request(e):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'bad request'
        }), 400

    @app.errorhandler(404)
    def not_found(e):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'entity not found'
        }), 404

    @app.errorhandler(422)
    def unprocessable_entity(e):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'unprocessable entity'
        }), 422

    @app.errorhandler(500)
    def internal_server_error(e):
        return jsonify({
            'success': False,
            'error': 500,
            'message': 'internal server error'
        }), 500

    return app

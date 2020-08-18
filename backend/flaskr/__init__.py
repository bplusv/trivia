import math
import random

from flask import Flask, request, abort, jsonify
from flask_cors import CORS
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
            return jsonify({
                'categories': {
                    category.id: category.type for category in categories
                }
            })
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
                'current_category': 0
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

    @app.route('/questions', methods=['POST'])
    def post_question():
        try:
            data = request.get_json()
            if 'searchTerm' in data:
                searchTerm = data['searchTerm']
                questions = Question.query.filter(
                    Question.question.ilike(f'%{searchTerm}%')).all()
                total_questions = Question.query.count()
                return jsonify({
                    'questions': [question.format() for question in questions],
                    'total_questions': total_questions,
                    'current_category': 0
                })
            else:
                question = Question(**data)
                question.insert()
                return jsonify({
                    'success': True
                })
        except SQLAlchemyError:
            abort(422)
        except Exception:
            abort(500)

    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def get_questions_by_category(category_id):
        try:
            questions = Question.query.filter(
                Question.category == category_id).all()
            total_questions = Question.query.count()
            return jsonify({
                'questions': [question.format() for question in questions],
                'total_questions': total_questions,
                'current_category': category_id
            })
        except Exception:
            abort(500)

    @app.route('/quizzes', methods=['POST'])
    def get_quizzes_next_question():
        try:
            data = request.get_json()
            category_id = int(data['quiz_category']['id'])
            prev_questions = [int(question_id)
                              for question_id in data['previous_questions']]
            query = Question.query.filter(Question.id.notin_(prev_questions))
            if category_id > 0:
                query = query.filter(Question.category == category_id)
            questions = query.all()
            question = random.choice(questions) if questions else None
            return jsonify({
                'question': question.format() if question else None
            })
        except Exception as e:
            raise e
            abort(500)

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

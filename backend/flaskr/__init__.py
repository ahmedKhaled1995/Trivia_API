from flask import Flask, request, abort, jsonify
from flask_cors import CORS
import random

from models import setup_db, Question, Category
from helper import get_paginated_data, get_all_categories_map, get_next_question

QUESTIONS_PER_PAGE = 10
LENGTH_CATEGORIES = 6


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    # Setting up the cors
    CORS(app, resources={r"/*": {"origins": "*"}})

    
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,POST,DELETE,OPTIONS')
        return response

  
    @app.route('/categories', methods=['GET'])
    def get_categories():
        categories = None
        try:
            categories = Category.query.order_by('id').all()
        except():
            abort(500)
        if not categories:
            abort(404)
        categories_map = get_all_categories_map(categories)
        return jsonify({
            'categories': categories_map
        }), 200

    
    @app.route('/questions', methods=['GET'])
    def get_questions():
        # Getting the questions and the categories
        all_questions = None
        categories = None
        try:
            all_questions = Question.query.order_by('id').all()
            categories = Category.query.order_by('id').all()
        except():
            abort(500)
        # Serializing the questions and shuffling them
        serialized_questions = get_paginated_data(request, all_questions, QUESTIONS_PER_PAGE)
        if not serialized_questions or not categories:
            abort(404)
        random.shuffle(serialized_questions)
        categories_map = get_all_categories_map(categories)
        # Getting a random number that will represent the current category
        current_category = random.randrange(LENGTH_CATEGORIES) + 1
        return jsonify({
            'questions': serialized_questions,
            'total_questions': len(all_questions),
            'categories': categories_map,
            'current_category': current_category
        }), 200

    
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_book(question_id):
        # Getting the question to delete
        question_to_delete = None
        try:
            question_to_delete = Question.query.filter(Question.id == question_id).first()
        except():
            abort(500)
        # The user provided an invalid id
        if not question_to_delete:
            abort(404)
        # Deleting the question and returning the response
        delete_success = question_to_delete.delete()
        if not delete_success:
            abort(500)
        return jsonify({
            'success': True,
            'deleted_question_id': question_to_delete.id,
            'total_questions': len(Question.query.order_by('id').all())
        }), 200

    
    @app.route("/questions", methods=['POST'])
    def add_question():
        # Getting the request data as JSON
        req_body = request.get_json()
        if req_body is None:
            abort(400)
        # Checking if the user posted an invalid data
        allowed_fields_of_question = ['question', 'answer', 'category', 'difficulty']
        for field in req_body:
            if field not in allowed_fields_of_question:
                abort(422)
        # Checking if difficulty is a number
        difficulty = None
        try:
            difficulty = int(req_body['difficulty'])
        except():
            abort(422)
        # Adding the question to the database
        question = Question(req_body['question'], req_body['answer'], req_body['category'], difficulty)
        operation_success = question.insert()
        if not operation_success:
            abort(500)
        # Returning the response
        return jsonify({
            'success': True,
            'question_id': question.id,
            'total_questions': len(Question.query.order_by('id').all())
        }), 201

   
    @app.route('/questions/search', methods=['POST'])
    def search_questions():
        # Getting the request data as JSON
        req_body = request.get_json()
        if req_body is None:
            abort(400)
        search_term = None
        # Checking if the user has provided a valid body request
        if "searchTerm" in req_body:
            search_term = req_body['searchTerm']
        else:
            abort(422)
        if not search_term:
            abort(422)
        questions = None
        try:
            questions = Question.query.filter(Question.question.ilike(f'%{search_term}%')).all()
        except():
            abort(500)
        # Returning a response if no data is found
        if not questions:
            return jsonify(
                {
                    'questions': [],
                    'total_questions': 0,
                    'current_category': None
                }
            ), 404
        questions_serialized = [question.format() for question in questions]
        # Getting a random number that will represent the current category
        current_category = random.randrange(LENGTH_CATEGORIES) + 1
        return jsonify(
            {
                'questions': questions_serialized,
                'total_questions': len(questions_serialized),
                'current_category': current_category
            }
        ), 200

   
    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def get_questions_by_category(category_id):
        # Getting questions in the given category
        questions_in_category = None
        try:
            questions_in_category = Question.query.filter(Question.category == category_id).all()
        except():
            abort(500)
        if not questions_in_category:
            abort(404)
        # Serializing and shuffling the questions then returning them
        questions_in_category_serialized = [question.format() for question in questions_in_category]
        random.shuffle(questions_in_category_serialized)
        return jsonify({
            'questions': questions_in_category_serialized,
            'total_questions': len(questions_in_category_serialized),
            'current_category': category_id,
        }), 200

    
    @app.route('/quizzes', methods=['POST'])
    def play_game():
        # Getting the request data as JSON
        req_body = request.get_json()
        if req_body is None:
            abort(400)
        # Checking the validity of the request body
        allowed_fields = ['quiz_category', 'previous_questions']
        for field in req_body:
            if field not in allowed_fields:
                abort(422)
        # Parsing the request to make sure the request body is correctly formatted
        quiz_category = None
        previous_questions_ids = None
        try:
            quiz_category = int(req_body['quiz_category']['id'])
            previous_questions_ids = list(req_body['previous_questions'])
        except ValueError:
            abort(422)
        # Getting the next question to send, that question's id is not in the 'previous_questions_ids' list and its
        # category matches the 'quiz_category'
        questions_in_the_quiz_category = None
        try:
            if quiz_category == 0:
                questions_in_the_quiz_category = Question.query.all()
            else:
                questions_in_the_quiz_category = Question.query.filter(Question.category == quiz_category).all()
        except():
            abort(500)
        next_question_serialized = get_next_question(previous_questions_ids, questions_in_the_quiz_category)
        return jsonify({
            'total_questions': len(questions_in_the_quiz_category),
            'question': next_question_serialized
        }), 200
   
    # Error handler Routes:
    # -------------------
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': "Not found"
        }), 404

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': "bad request"
        }), 400

    @app.errorhandler(422)
    def illegal_request_body(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': "please provide valid fields in your request body"
        }), 422

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
            'success': False,
            'error': 500,
            'message': "server error"
        }), 500

    return app

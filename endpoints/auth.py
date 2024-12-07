from flask import request
from flask_restful import Resource
from utils.authentication import AuthValidator

class AuthenticationResource(Resource):
    def __init__(self):
        self.auth_validator = AuthValidator()

    def post(self):
        try:
            data = request.json
            if not data:
                return {'message': 'Bad Request: JSON body missing'}, 400
            
            username = data.get('username')
            password = data.get('password')

            if not username or not password:
                return {'message': 'Bad Request: Missing username or password'}, 400

            if self.auth_validator.validate(username, password):
                token = 'abcd12345'
                return {'token': token}, 200
            else:
                return {'message': 'Unauthorized'}, 401
        except Exception as e:
            return {'message': f'Internal Server Error: {str(e)}'}, 500

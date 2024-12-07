import os
from flask import request
from functools import wraps

class AuthValidator:
    """Clase para validar credenciales de usuario."""
    def __init__(self):
        self.username = os.getenv('AUTH_USERNAME', 'student')
        self.password = os.getenv('AUTH_PASSWORD', 'desingp')

    def validate(self, username, password):
        """Valida las credenciales ingresadas."""
        return username == self.username and password == self.password


class TokenValidator:
    """Clase para validar y manejar tokens."""
    def __init__(self):
        self.valid_token = os.getenv('AUTH_TOKEN', 'abcd1234')

    def is_valid_token(self, token):
        """Valida si un token es válido."""
        return token == self.valid_token

    def generate_token(self):
        """Genera un token."""
        return self.valid_token


# Decorador para validar tokens
def auth_required(func):
    """Decorador para validar tokens de autorización."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        token_validator = TokenValidator()
        token = request.headers.get('Authorization')
        if not token:
            return {'message': 'Unauthorized: Token not found'}, 401
        if not token_validator.is_valid_token(token):
            return {'message': 'Unauthorized: Invalid token'}, 401
        return func(*args, **kwargs)
    return wrapper

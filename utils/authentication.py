import os

class AuthValidator:
    """Clase para validar credenciales de usuario."""
    def __init__(self):
        self.username = os.getenv('AUTH_USERNAME', 'student')
        self.password = os.getenv('AUTH_PASSWORD', 'desingp')

    def validate(self, username, password):
        """Valida las credenciales ingresadas."""
        return username == self.username and password == self.password

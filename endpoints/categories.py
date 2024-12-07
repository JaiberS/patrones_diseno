from flask_restful import Resource, reqparse
from utils.database_connection import DatabaseConnection
from utils.authentication import auth_required

class CategoriesResource(Resource):
    def __init__(self):
        # Inicialización de la conexión a la base de datos y el analizador de argumentos
        self.db = DatabaseConnection('db.json')
        self.db.connect()
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('name', type=str, required=True, help='Name of the category')

    @auth_required
    def get(self, category_id=None):
        """
        Maneja las solicitudes GET para obtener categorías. Si se proporciona un ID, devuelve
        una categoría específica; de lo contrario, devuelve todas las categorías.
        """
        categories = self.db.get_categories()

        if category_id is not None:
            category = next((category for category in categories if category['id'] == category_id), None)
            if category:
                return category, 200
            return {'message': 'Category not found'}, 404

        return categories, 200

    @auth_required
    def post(self):
        """
        Maneja las solicitudes POST para agregar una nueva categoría.
        Requiere el nombre de la categoría en el cuerpo de la solicitud.
        """
        args = self.parser.parse_args()
        new_category_name = args['name']

        categories = self.db.get_categories()

        # Validación de categoría duplicada
        if any(category['name'] == new_category_name for category in categories):
            return {'message': 'Category already exists'}, 400

        # Crear y guardar nueva categoría
        new_category = {'id': len(categories) + 1, 'name': new_category_name}
        self.db.add_category(new_category)

        return {'message': 'Category added successfully'}, 201

    @auth_required
    def delete(self):
        """
        Maneja las solicitudes DELETE para eliminar una categoría existente.
        Requiere el nombre de la categoría en el cuerpo de la solicitud.
        """
        args = self.parser.parse_args()
        category_name = args['name']

        categories = self.db.get_categories()
        category_to_remove = next((category for category in categories if category['name'] == category_name), None)

        if not category_to_remove:
            return {'message': 'Category not found'}, 404

        # Eliminar la categoría
        self.db.remove_category(category_name)

        return {'message': 'Category removed successfully'}, 200

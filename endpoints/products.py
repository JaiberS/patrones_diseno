from flask_restful import Resource, reqparse
from flask import request
from utils.database_connection import DatabaseConnection
from utils.authentication import auth_required

class ProductsResource(Resource):
    def __init__(self):
        # Inicializar la conexión a la base de datos
        self.db = DatabaseConnection('db.json')
        self.db.connect()
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('name', type=str, required=True, help='Name of the product')
        self.parser.add_argument('category', type=str, required=True, help='Category of the product')
        self.parser.add_argument('price', type=float, required=True, help='Price of the product')

    @auth_required
    def get(self, product_id=None):
        """
        Maneja las solicitudes GET para obtener productos.
        Si se proporciona un ID, devuelve un producto específico.
        También filtra por categoría si se pasa un argumento de consulta.
        """
        products = self.db.get_products()
        category_filter = request.args.get('category')

        if category_filter:
            filtered_products = self._filter_by_category(products, category_filter)
            return filtered_products, 200

        if product_id is not None:
            product = next((product for product in products if product['id'] == product_id), None)
            if product:
                return product, 200
            return {'message': 'Product not found'}, 404

        return products, 200

    @auth_required
    def post(self):
        """
        Maneja las solicitudes POST para agregar un nuevo producto.
        """
        args = self.parser.parse_args()
        products = self.db.get_products()

        # Verificar si el producto ya existe
        if any(product['name'].lower() == args['name'].lower() for product in products):
            return {'message': 'Product already exists'}, 400

        # Crear y guardar el nuevo producto
        new_product = {
            'id': len(products) + 1,
            'name': args['name'],
            'category': args['category'],
            'price': args['price']
        }
        self.db.add_product(new_product)

        return {'message': 'Product added successfully', 'product': new_product}, 201

    def _filter_by_category(self, products, category):
        """
        Filtra productos por categoría.
        """
        return [product for product in products if product['category'].lower() == category.lower()]

from flask_restful import Resource, reqparse
from flask import request
from utils.database_connection import DatabaseConnection
from utils.authentication import auth_required

class FavoritesResource(Resource):
    def __init__(self):
        # Inicializar conexión a la base de datos
        self.db = DatabaseConnection('favorites.json')
        self.db.connect()
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('user_id', type=int, required=True, help='User ID is required')
        self.parser.add_argument('product_id', type=int, required=True, help='Product ID is required')

    @auth_required
    def get(self):
        """
        Devuelve todos los productos favoritos.
        """
        try:
            return self.db.get_favorites(), 200
        except Exception as e:
            return {'message': f'Error retrieving favorites: {str(e)}'}, 500

    @auth_required
    def post(self):
        """
        Agrega un nuevo producto a los favoritos.
        """
        args = self.parser.parse_args()
        favorites = self.db.get_favorites()

        # Verificar si el producto ya está en favoritos
        if any(fav['user_id'] == args['user_id'] and fav['product_id'] == args['product_id'] for fav in favorites):
            return {'message': 'Product already in favorites'}, 400

        # Agregar el nuevo favorito
        new_favorite = {
            'user_id': args['user_id'],
            'product_id': args['product_id']
        }
        self.db.add_favorite(new_favorite)
        return {'message': 'Product added to favorites', 'favorite': new_favorite}, 201

    @auth_required
    def delete(self):
        """
        Elimina un producto de los favoritos.
        """
        args = self.parser.parse_args()
        favorites = self.db.get_favorites()

        # Verificar si el favorito existe
        favorite_to_remove = next(
            (fav for fav in favorites if fav['user_id'] == args['user_id'] and fav['product_id'] == args['product_id']),
            None
        )
        if not favorite_to_remove:
            return {'message': 'Favorite not found'}, 404

        # Eliminar el favorito
        self.db.data['favorites'] = [
            fav for fav in favorites if fav != favorite_to_remove
        ]
        self.db._save_data()

        return {'message': 'Product removed from favorites'}, 200

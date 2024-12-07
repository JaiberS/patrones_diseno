from endpoints.products import ProductsResource
from endpoints.auth import AuthenticationResource
from endpoints.categories import CategoriesResource
from endpoints.favorites import FavoritesResource

def register_routes(api):
    api.add_resource(AuthenticationResource, '/auth')
    api.add_resource(ProductsResource, '/products', '/products/<int:product_id>')
    api.add_resource(CategoriesResource, '/categories', '/categories/<int:category_id>')
    api.add_resource(FavoritesResource, '/favorites')

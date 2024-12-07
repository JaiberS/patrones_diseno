from flask import Flask
from flask_restful import Api
from config import Config
from routes import register_routes
from data_loader import load_data

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Configurar la API
    api = Api(app)
    register_routes(api)
    
    # Cargar datos iniciales
    app.products = load_data('db.json')
    
    return app

if __name__ == '__main__':
    import os
    config_env = os.getenv('FLASK_ENV', 'development')
    app = create_app()
    app.run(debug=config_env == 'development')

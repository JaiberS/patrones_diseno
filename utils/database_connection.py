import json
import os

class DatabaseConnection:
    def __init__(self, json_file_path):
        self.json_file_path = json_file_path
        self.data = None 

    def connect(self):
        """Carga los datos desde el archivo JSON."""
        if os.path.exists(self.json_file_path):
            with open(self.json_file_path, 'r') as json_file:
                self.data = json.load(json_file)
        else:
            print("Warning: JSON file not found, initializing with empty data.")
            self.data = {"products": [], "categories": [], "favorites": []}

    def _save_data(self):
        """Guarda los datos actuales en el archivo JSON."""
        if self.data:
            with open(self.json_file_path, 'w') as json_file:
                json.dump(self.data, json_file, indent=4)
        else:
            print("Error: No data to save.")

    def _add_item(self, key, new_item, unique_key=None):
        """Agrega un elemento a la lista correspondiente en los datos."""
        if not self.data:
            print("Error: No data loaded. Call connect() first.")
            return
        if new_item not in self.data[key]:
            if unique_key and any(item[unique_key] == new_item[unique_key] for item in self.data[key]):
                print(f"Error: {unique_key} already exists in {key}.")
                return
            self.data[key].append(new_item)
            self._save_data()
        else:
            print(f"Error: Item already exists in {key}.")

    def get_items(self, key):
        """Obtiene los elementos de una lista específica."""
        if self.data:
            return self.data.get(key, [])
        else:
            print("Error: No data loaded. Call connect() first.")
            return []

    def add_product(self, new_product):
        self._add_item('products', new_product, unique_key="id")

    def add_category(self, new_category):
        self._add_item('categories', new_category, unique_key="name")

    def remove_category(self, category_name):
        """Elimina una categoría por nombre."""
        if not self.data:
            print("Error: No data loaded. Call connect() first.")
            return
        self.data['categories'] = [
            cat for cat in self.data['categories'] if cat["name"] != category_name
        ]
        self._save_data()

    def add_favorite(self, new_favorite):
        self._add_item('favorites', new_favorite, unique_key="product_id")

    def get_products(self):
        return self.get_items('products')

    def get_categories(self):
        return self.get_items('categories')

    def get_favorites(self):
        return self.get_items('favorites')

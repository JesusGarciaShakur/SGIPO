from .db import get_connection

mydb = get_connection()
#id_product, name_product, description_product, id_brand, price_product, stock_product
class Product:
    def __init__(self, id_product='', name_product='', description_product='', id_brand='', price_product='', stock_product='', image_product=''):
        self.id_product = id_product
        self.name_product = name_product
        self.description_product = description_product
        self.id_brand = id_brand
        self.price_product = price_product
        self.stock_product = stock_product
        self.image_product = image_product

    def save(self):
        with mydb.cursor() as cursor:
            sql = "INSERT INTO products_sgipo(name_product, description_product, id_brand, price_product, stock_product, image_product) VALUES (%s, %s, %s, %s, %s, %s)"
            values = (self.name_product, self.description_product, self.id_brand, self.price_product, self.stock_product, self.image_product)
            cursor.execute(sql, values)
        mydb.commit()

    def update(self):
        with mydb.cursor() as cursor:
            sql = "UPDATE products_sgipo SET name_product = %s, description_product = %s, id_brand = %s, price_product = %s, stock_product = %s, image_product = %s WHERE id_product = %s"
            values = (self.name_product, self.description_product, self.id_brand, self.price_product, self.stock_product, self.image_product, self.id_product)
            cursor.execute(sql, values)
            mydb.commit()
        return self.id_product
    
    def delete(self):
        with mydb.cursor() as cursor:
            sql = f"DELETE FROM products_sgipo WHERE id_product = {self.id_product}"
            cursor.execute(sql)
            mydb.commit()
        return self.id_product
    
    def to_dict(self):
        return {
            'id_product': self.id_product,
            'name_product': self.name_product,
            'description_product': self.description_product,
            'id_brand': self.id_brand,
            'price_product': self.price_product,
            'stock_product': self.stock_product,
            'image_product': self.image_product,
        }

    @staticmethod
    def get(id_product):
        with mydb.cursor(dictionary=True) as cursor:
            sql = f"SELECT * FROM products_sgipo WHERE id_product = {id_product}"
            cursor.execute(sql)
            product = cursor.fetchone()
            if  product:
                product = Product(id_product=product["id_product"],
                                name_product=product["name_product"],
                                description_product=product["description_product"],
                                id_brand=product["id_brand"],
                                price_product=product["price_product"],
                                stock_product=product["stock_product"],
                                image_product=product["image_product"])
                return product
            return None
        
    @staticmethod
    def get_all():
        products = []
        connection = get_connection()
        with connection.cursor(dictionary=True) as cursor:
            sql = "SELECT * FROM vista_productos"
            cursor.execute(sql)
            result = cursor.fetchall()
            for row in result:
                product = Product(id_product=row["id de producto"],
                                name_product=row["nombre del producto"],
                                description_product=row["descripcion producto"],
                                id_brand=row["nombre marca"],
                                price_product=row["precio producto"],
                                stock_product=row["cantidad en stock"],
                                image_product=row["imagen producto"])
                products.append(product)
        connection.close()
        return products
    

    @staticmethod
    def get_paginated_products(page, per_page):
        products = []
        offset = (page - 1) * per_page
        connection = get_connection()  # Obtén una conexión fresca
        with connection.cursor(dictionary=True) as cursor:
            cursor.execute("SELECT COUNT(*) FROM vista_productos")
            total = cursor.fetchone()['COUNT(*)']
            
            cursor.execute("SELECT * FROM vista_productos ORDER BY `id de producto` DESC LIMIT %s OFFSET %s", (per_page, offset))
            result = cursor.fetchall()
            for row in result:
                product = Product(id_product=row["id de producto"],
                                name_product=row["nombre del producto"],
                                description_product=row["descripcion producto"],
                                id_brand=row["nombre marca"],
                                price_product=row["precio producto"],
                                stock_product=row["cantidad en stock"],
                                image_product=row["imagen producto"])
                products.append(product)
        connection.close()  # Cierra la conexión después de usarla
        return products, total

    @staticmethod
    def search(query, page, per_page):
        offset = (page - 1) * per_page
        products = []
        search_query = f"%{query}%"

        with mydb.cursor(dictionary=True) as cursor:
            cursor.execute("""
                SELECT COUNT(*) FROM vista_productos
                WHERE `nombre del producto` LIKE %s OR `descripcion producto` LIKE %s OR `nombre marca` LIKE %s OR `precio producto` LIKE %s OR `cantidad en stock` LIKE %s
            """, (search_query, search_query, search_query, search_query, search_query))
            total = cursor.fetchone()['COUNT(*)']

            cursor.execute("""
                SELECT * FROM vista_productos
                WHERE `nombre del producto` LIKE %s OR `descripcion producto` LIKE %s OR `nombre marca` LIKE %s OR `precio producto` LIKE %s OR `cantidad en stock` LIKE %s
                ORDER BY `id de producto` DESC LIMIT %s OFFSET %s
            """, (search_query, search_query, search_query, search_query, search_query, per_page, offset))
            result = cursor.fetchall()

            for row in result:
                product = Product(id_product=row["id de producto"],
                                name_product=row["nombre del producto"],
                                description_product=row["descripcion producto"],
                                id_brand=row["nombre marca"],
                                price_product=row["precio producto"],
                                stock_product=row["cantidad en stock"],
                                image_product=row["imagen producto"])
                products.append(product)
        return products, total
    
class Brand:
    def __init__(self, id_brand='', name_brand='', description_brand='', id_supplier='', image_brand=''):
        self.id_brand = id_brand
        self.name_brand = name_brand
        self.description_brand = description_brand
        self.id_supplier = id_supplier
        self.image_brand = image_brand

    @staticmethod
    def get_all():
        brands = []
        connection = get_connection()
        with connection.cursor(dictionary=True) as cursor:
            sql = "SELECT * FROM vista_marcas"
            cursor.execute(sql)
            result = cursor.fetchall()
            for row in result:
                brand = Brand(id_brand=row["id de marca"],
                            name_brand=row["nombre de marca"],
                            description_brand=row["descripcion marca"],
                            id_supplier=row["nombre proveedor"],
                            image_brand=row["imagen marca"])
                brands.append(brand)
        connection.close()
        return brands

def count_products():
    with mydb.cursor(dictionary=True) as cursor:
        cursor.execute("SELECT COUNT(*) FROM products_sgipo")
        result = cursor.fetchone()
        return result['COUNT(*)']
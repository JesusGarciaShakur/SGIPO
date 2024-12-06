from .db import get_connection

mydb = get_connection()
#id_product, name_product, description_product, id_brand, price_product, stock_product
class Product:
    def __init__(self, id_product='', name_product='', description_product='', id_brand='', price_product='', stock_product=''):
        self.id_product = id_product
        self.name_product = name_product
        self.description_product = description_product
        self.id_brand = id_brand
        self.price_product = price_product
        self.stock_product = stock_product

    def save(self):
        with mydb.cursor() as cursor:
            sql = "INSERT INTO products_sgipo(name_product, description_product, id_brand, price_product, stock_product) VALUES (%s, %s, %s, %s, %s)"
            values = (self.name_product, self.description_product, self.id_brand, self.price_product, self.stock_product)
            print(f"SQL: {sql}")
            print(f"Values: {values}")
            cursor.execute(sql, values)
        mydb.commit()

    def update(self):
        with mydb.cursor() as cursor:
            sql = "UPDATE products_sgipo SET name_product = %s, description_product = %s, id_brand = %s, price_product = %s, stock_product = %s WHERE id_product = %s"
            values = (self.name_product, self.description_product, self.id_brand, self.price_product, self.stock_product, self.id_product)
            cursor.execute(sql, values)
            mydb.commit()
        return self.id_product
    
    def delete(self):
        with mydb.cursor() as cursor:
            sql = f"DELETE FROM products_sgipo WHERE id_product = {self.id_product}"
            cursor.execute(sql)
            mydb.commit()
        return self.id_product
    
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
                                stock_product=product["stock_product"])
                return product
            return None
        
    @staticmethod
    def __get__(id_product):
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
                                stock_product=product["stock_product"])
                return product
            return None
        
    @staticmethod
    def get_all():
        with mydb.cursor(dictionary=True) as cursor:
            sql = "SELECT * FROM vista_productos"
            cursor.execute(sql)
            result = cursor.fetchall()
            products = []
            for row in result:
                product = Product(id_product=row["id de producto"],
                                name_product=row["nombre del producto"],
                                description_product=row["descripcion producto"],
                                id_brand=row["nombre marca"],
                                price_product=row["precio producto"],
                                stock_product=row["cantidad en stock"])
                products.append(product)
        return products

    @staticmethod
    def get_paginated_products(page, per_page):
        offset = (page - 1) * per_page
        products = []
        with mydb.cursor(dictionary=True) as cursor:
            cursor.execute("SELECT COUNT(*) FROM vista_productos")
            total = cursor.fetchone()['COUNT(*)']
            
            cursor.execute("SELECT * FROM vista_productos ORDER BY 'id de producto'DESC LIMIT %s OFFSET %s", (per_page, offset))
            result = cursor.fetchall()
            for row in result:
                product = Product(id_product=row["id de producto"],
                                name_product=row["nombre del producto"],
                                description_product=row["descripcion producto"],
                                id_brand=row["nombre marca"],
                                price_product=row["precio producto"],
                                stock_product=row["cantidad en stock"])
                products.append(product)
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
                                stock_product=row["cantidad en stock"])
                products.append(product)
        return products, total
    
class Brand:
    def __init__(self, id_brand='', name_brand='', description_brand='', id_supplier=''):
        self.id_brand = id_brand
        self.name_brand = name_brand
        self.description_brand = description_brand
        self.id_supplier = id_supplier

    @staticmethod
    def get_all():
        brands = []
        with mydb.cursor(dictionary=True) as cursor:
            sql = "SELECT * FROM vista_marcas"
            cursor.execute(sql)
            result = cursor.fetchall()
            for row in result:
                brand = Brand(id_brand=row["id de marca"],
                            name_brand=row["nombre de marca"],
                            description_brand=row["descripcion marca"],
                            id_supplier=row["nombre proveedor"])
                brands.append(brand)
        return brands

def count_products():
    with mydb.cursor(dictionary=True) as cursor:
        cursor.execute("SELECT COUNT(*) FROM products_sgipo")
        result = cursor.fetchone()
        return result['COUNT(*)']
from .db import get_connection

mydb = get_connection()
#id_purchase,id_supplier,id_product,,quantity_ordered,date_ordered

class Purchase:
    def __init__(self, id_purchase='', id_supplier='', id_product='', quantity_ordered='', date_ordered=''):
        self.id_purchase = id_purchase
        self.id_supplier = id_supplier
        self.id_product = id_product
        self.quantity_ordered = quantity_ordered
        self.date_ordered = date_ordered

    def save(self):
        with mydb.cursor() as cursor:
            sql = "INSERT INTO purchase_orders_sgipo(id_supplier, id_product, quantity_ordered, date_ordered) VALUES(%s, %s, %s, %s)"
            values = (self.id_supplier, self.id_product, self.quantity_ordered, self.date_ordered)
            cursor.execute(sql, values)
        mydb.commit()

    def update(self):
        with mydb.cursor() as cursor:
            sql = "UPDATE purchase_orders_sgipo SET id_supplier = %s, id_product = %s, quantity_ordered = %s, date_ordered = %s WHERE id_purchase = %s"
            values = (self.id_supplier, self.id_product, self.quantity_ordered, self.date_ordered, self.id_purchase)
            cursor.execute(sql, values)
            mydb.commit()
        return self.id_purchase
    
    def delete(self):
        with mydb.cursor() as cursor:
            sql = f"DELETE FROM purchase_orders_sgipo WHERE id_purchase = {self.id_purchase}"
            cursor.execute(sql)
            mydb.commit()
        return self.id_purchase
    
    @staticmethod
    def get(id_purchase):
        with mydb.cursor(dictionary=True) as cursor:
            sql = f"SELECT * FROM purchase_orders_sgipo WHERE id_purchase = {id_purchase}"
            cursor.execute(sql)
            purchase = cursor.fetchone()
            if  purchase:
                purchase = Purchase(id_purchase=purchase["id_purchase"],
                                id_supplier=purchase["id_supplier"],
                                id_product=purchase["id_product"],
                                quantity_ordered=purchase["quantity_ordered"],
                                date_ordered=purchase["date_ordered"])
                return purchase
            return None
        
    @staticmethod
    def get_all():
        purchases = []
        connection = get_connection()
        with connection.cursor(dictionary=True) as cursor:
            sql = "SELECT * FROM vista_ordenes"
            cursor.execute(sql)
            result = cursor.fetchall()
            for row in result:
                purchase = Purchase(id_purchase=row["id de orden"],
                                id_supplier=row["nombre proveedor"],
                                id_product=row["nombre producto"],
                                quantity_ordered=row["cantidad ordenar"],
                                date_ordered=row["fecha de orden"])
                purchases.append(purchase)
        connection.close()
        return purchases
    
    @staticmethod
    def get_paginated_purchases(page, per_page):
        purchases = []
        offset = (page - 1) * per_page
        connection = get_connection()
        with connection.cursor(dictionary=True) as cursor:
            # Obtener el número total de registros
            cursor.execute("SELECT COUNT(*) FROM vista_ordenes")
            total = cursor.fetchone()['COUNT(*)']
            
            cursor.execute("SELECT * FROM vista_ordenes ORDER BY `id de orden` DESC LIMIT %s OFFSET %s", (per_page, offset))
            result = cursor.fetchall()
            for row in result:
                purchase = Purchase(id_purchase=row["id de orden"],
                                id_supplier=row["nombre proveedor"],
                                id_product=row["nombre producto"],
                                quantity_ordered=row["cantidad ordenar"],
                                date_ordered=row["fecha de orden"])
                purchases.append(purchase)
        connection.close()
        return purchases, total
    
    @staticmethod
    def search(query, page, per_page):
        offset = (page - 1) * per_page
        purchases = []
        search_query = f"%{query}%"

        with mydb.cursor(dictionary=True) as cursor:
            # Obtener el total de resultados
            cursor.execute("""SELECT COUNT(*) FROM vista_ordenes
                WHERE `nombre proveedor` LIKE %s OR `nombre producto` LIKE %s
                OR `cantidad ordenar` LIKE %s OR `fecha de orden` LIKE %s
            """, (search_query, search_query, search_query, search_query))
            total = cursor.fetchone()['COUNT(*)']

            # Obtener los resultados paginados
            cursor.execute("""SELECT * FROM vista_ordenes
                WHERE `nombre proveedor` LIKE %s OR `nombre producto` LIKE %s
                OR `cantidad ordenar` LIKE %s OR `fecha de orden` LIKE %s
                ORDER BY `id de orden` DESC LIMIT %s OFFSET %s
            """, (search_query, search_query, search_query, search_query, per_page, offset))
            result = cursor.fetchall()

            # Construir objetos Purchase
            for row in result:
                purchase = Purchase(id_purchase=row["id de orden"],
                                id_supplier=row["nombre proveedor"],
                                id_product=row["nombre producto"],
                                quantity_ordered=row["cantidad ordenar"],
                                date_ordered=row["fecha de orden"])
                purchases.append(purchase)
        return purchases, total
    
class Product:
    def __init__(self, id_product='', name_product='', description_product='', id_brand='', price_product='', stock_product=''):
        self.id_product = id_product
        self.name_product = name_product
        self.description_product = description_product
        self.id_brand = id_brand
        self.price_product = price_product
        self.stock_product = stock_product

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
                                stock_product=row["cantidad en stock"])
                products.append(product)
        connection.close()
        return products
    
class Supplier:
    def __init__(self, id_supplier='', name_supplier='', direction_supplier='', rfc_supplier='', contact_supplier=''):
        self.id_supplier = id_supplier
        self.name_supplier = name_supplier
        self.direction_supplier = direction_supplier
        self.rfc_supplier = rfc_supplier
        self.contact_supplier = contact_supplier

    @staticmethod
    def get_all():
        suppliers = []
        connection = get_connection()
        with connection.cursor(dictionary=True) as cursor:
            sql = "SELECT * FROM suppliers_sgipo"
            cursor.execute(sql)
            result = cursor.fetchall()
            for row in result:
                supplier = Supplier(id_supplier=row["id_supplier"],
                                    name_supplier=row["name_supplier"],
                                    direction_supplier=row["direction_supplier"],
                                    rfc_supplier=row["rfc_supplier"],
                                    contact_supplier=row["contact_supplier"])
                suppliers.append(supplier)
        connection.close()
        return suppliers
    
def count_purchases():
    with mydb.cursor(dictionary=True) as cursor:
        cursor.execute("SELECT COUNT(*) FROM purchase_orders_sgipo")
        result = cursor.fetchone()
        return result['COUNT(*)']
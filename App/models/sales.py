from .db import get_connection
from datetime import datetime
import mysql.connector

mydb = get_connection()
#id_sale,id_client,id_product,,quantity_sold,final_price,date_sold

class Sale:
    def __init__(self, id_sale='', id_client='', id_product='', quantity_sold='', final_price='', date_sold=''):
        self.id_sale = id_sale
        self.id_client = id_client
        self.id_product = id_product
        self.quantity_sold = quantity_sold
        self.final_price = final_price
        self.date_sold = date_sold

    def save(self):
        with mydb.cursor() as cursor:
            sql = "INSERT INTO sales_sgipo(id_client, id_product, quantity_sold, final_price, date_sold) VALUES(%s, %s, %s, %s, %s)"
            values = (self.id_client, self.id_product, self.quantity_sold, self.final_price, self.date_sold)
            cursor.execute(sql, values)
        mydb.commit()

    def update(self):
        with mydb.cursor() as cursor:
            sql = "UPDATE sales_sgipo SET id_client = %s, id_product = %s, quantity_sold = %s, final_price = %s, date_sold = %s WHERE id_sale = %s"
            values = (self.id_client, self.id_product, self.quantity_sold, self.final_price, self.date_sold, self.id_sale)
            cursor.execute(sql, values)
            mydb.commit()
        return self.id_sale
    
    def delete(self):
        with mydb.cursor() as cursor:
            sql = f"DELETE FROM sales_sgipo WHERE id_sale = {self.id_sale}"
            cursor.execute(sql)
            mydb.commit()
        return self.id_sale
    
    @staticmethod
    def get(id_sale):
        with mydb.cursor(dictionary=True) as cursor:
            sql = f"SELECT * FROM sales_sgipo WHERE id_sale = {id_sale}"
            cursor.execute(sql)
            sale = cursor.fetchone()
            if  sale:
                sale = Sale(id_sale=sale["id_sale"],
                                id_client=sale["id_client"],
                                id_product=sale["id_product"],
                                quantity_sold=sale["quantity_sold"],
                                final_price=sale["final_price"],
                                date_sold=sale["date_sold"])
                return sale
            return None
        
    @staticmethod
    def get_all():
        sales = []
        with mydb.cursor(dictionary=True) as cursor:
            sql = "SELECT * FROM vista_ventas"
            cursor.execute(sql)
            result = cursor.fetchall()
            for row in result:
                sale = Sale(id_sale=row["id de venta"],
                                id_client=row["nombre cliente"],
                                id_product=row["nombre producto"],
                                quantity_sold=row["articulos vendidos"],
                                final_price=row["precio final"],
                                date_sold=row["fecha venta"])
                sales.append(sale)
        return sales
    
    @staticmethod
    def get_paginated_sales(page, per_page):
        sales = []
        offset = (page - 1) * per_page
        connection = get_connection()
        with connection.cursor(dictionary=True) as cursor:
            # Obtener el número total de registros
            cursor.execute("SELECT COUNT(*) FROM vista_ventas")
            total = cursor.fetchone()['COUNT(*)']
            
            # Consulta para recuperar los datos, incluyendo el apellido
            cursor.execute("""
                SELECT 
                    `id de venta`,
                    `nombre cliente`,
                    `apellido cliente`,
                    `nombre producto`,
                    `articulos vendidos`,
                    `precio final`,
                    `fecha venta`
                FROM vista_ventas
                ORDER BY `id de venta` DESC
                LIMIT %s OFFSET %s
            """, (per_page, offset))
            result = cursor.fetchall()
            for row in result:
                sale = Sale(
                    id_sale=row["id de venta"],
                    id_client=f"{row['nombre cliente']} {row['apellido cliente']}",  # Combina nombre y apellido
                    id_product=row["nombre producto"],
                    quantity_sold=row["articulos vendidos"],
                    final_price=row["precio final"],
                    date_sold=row["fecha venta"]
                )
                sales.append(sale)
        connection.close()  # Cierra la conexión correctamente
        return sales, total


    
    @staticmethod
    def search(query, page, per_page):
        offset = (page - 1) * per_page
        sales = []
        search_query = f"%{query}%"

        with mydb.cursor(dictionary=True) as cursor:
            # Obtener el número total de registros
            cursor.execute("""SELECT COUNT(*) FROM vista_ventas
                WHERE `nombre cliente` LIKE %s OR `nombre producto` LIKE %s
                OR `articulos vendidos` LIKE %s OR `precio final` LIKE %s
                OR `fecha venta` LIKE %s
            """, (search_query, search_query, search_query, search_query, search_query))
            total = cursor.fetchone()['COUNT(*)']

            cursor.execute("""SELECT * FROM vista_ventas
                WHERE `nombre cliente` LIKE %s OR `nombre producto` LIKE %s
                OR `articulos vendidos` LIKE %s OR `precio final` LIKE %s
                OR `fecha venta` LIKE %s
                ORDER BY `id de venta` DESC LIMIT %s OFFSET %s
            """, (search_query, search_query, search_query, search_query, search_query, per_page, offset))
            result = cursor.fetchall()
            for row in result:
                sale = Sale(id_sale=row["id de venta"],
                                id_client=row["nombre cliente"],
                                id_product=row["nombre producto"],
                                quantity_sold=row["articulos vendidos"],
                                final_price=row["precio final"],
                                date_sold=row["fecha venta"])
                sales.append(sale)
        return sales, total


def generate_report(start_date, end_date):
    sales = []
    with mydb.cursor(dictionary=True) as cursor:
        sql = """
            SELECT 
                `id de venta`,
                `nombre cliente`,
                `apellido cliente`,
                `nombre producto`,
                `articulos vendidos`,
                `precio final`,
                `fecha venta`
            FROM vista_ventas
            WHERE `fecha venta` BETWEEN %s AND %s
            ORDER BY `fecha venta`
        """
        cursor.execute(sql, (start_date, end_date))
        sales = cursor.fetchall()

    # Aquí ya tienes acceso al apellido cliente, puedes agregarlo o manipularlo según sea necesario
    return sales



class Client:
    def __init__(self, id_client='', name_client='', lastName_client='', age_client='', numberPhone_client='', email_client='', direction_client='', id_disease='', time_disease='', is_controlled='', prescription_drugs='', oi_vision='', od_vision=''):
        self.id_client = id_client
        self.name_client = name_client
        self.lastName_client = lastName_client
        self.age_client = age_client
        self.numberPhone_client = numberPhone_client
        self.email_client = email_client
        self.direction_client = direction_client
        self.id_disease = id_disease
        self.time_disease = time_disease
        self.is_controlled = is_controlled
        self.prescription_drugs = prescription_drugs
        self.oi_vision = oi_vision
        self.od_vision = od_vision

    @staticmethod
    def get_all():
        clients = []
        connection = get_connection()
        with connection.cursor(dictionary=True) as cursor:
            sql = "SELECT * FROM vista_clientes"
            cursor.execute(sql)
            result = cursor.fetchall()
            for row in result:
                client = Client(id_client=row["id de cliente"],
                                name_client=row["nombre"],
                                lastName_client=row["apellido"],
                                age_client=row["edad"],
                                numberPhone_client=row["numero de telefono"],
                                email_client=row["correo electronico"],
                                direction_client=row["direccion"],
                                id_disease=row["nombre padecimiento"],
                                time_disease=row["tiempo"],
                                is_controlled=row["controlada"],
                                prescription_drugs=row["medicamentos"],
                                od_vision=row["ojo derecho"],
                                oi_vision=row["ojo izquierdo"])
                clients.append(client)
        connection.close()
        return clients

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
    
def count_sales():
    with mydb.cursor(dictionary=True) as cursor:
        cursor.execute("SELECT COUNT(*) FROM sales_sgipo")
        result = cursor.fetchone()
        return result['COUNT(*)']
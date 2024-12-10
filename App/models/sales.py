from .db import get_connection

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
        offset = (page - 1) * per_page
        sales = []

        with mydb.cursor(dictionary=True) as cursor:
            # Obtener el número total de registros
            cursor.execute("SELECT COUNT(*) FROM vista_ventas")
            total = cursor.fetchone()['COUNT(*)']
            
            # Ajuste en la consulta para ordenar correctamente
            cursor.execute("SELECT * FROM vista_ventas ORDER BY `id de venta` DESC LIMIT %s OFFSET %s", (per_page, offset))
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

    
    @staticmethod
    def search(query, page, per_page):
        offset = (page - 1) * per_page
        sales = []

        with mydb.cursor(dictionary=True) as cursor:
            # Obtener el número total de registros
            cursor.execute("""SELECT COUNT(*) FROM vista_ventas
                WHERE `nombre cliente` LIKE %s OR `nombre producto` LIKE %s
                OR `articulos vendidos` LIKE %s OR `precio final` LIKE %s
                OR `fecha venta` LIKE %s
            """, (query, query, query, query, query))
            total = cursor.fetchone()['COUNT(*)']

            cursor.execute("""SELECT * FROM vista_ventas
                WHERE `nombre cliente` LIKE %s OR `nombre producto` LIKE %s
                OR `articulos vendidos` LIKE %s OR `precio final` LIKE %s
                OR `fecha venta` LIKE %s
                ORDER BY `id de venta` DESC LIMIT %s OFFSET %s
            """, (query, query, query, query, query, per_page, offset))
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
    


from datetime import datetime
import mysql.connector

def generate_report(start_date_str, end_date_str):
    try:
        # Validar y convertir las fechas de string a objeto datetime
        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
        except ValueError:
            return {"error": "Invalid date format. Use YYYY-MM-DD."}

        # Verificar que la fecha de inicio no sea mayor a la fecha de fin
        if start_date > end_date:
            return {"error": "Start date must be earlier than or equal to end date."}

        # Establecer la conexión con la base de datos
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)  # Los resultados serán devueltos como diccionarios

        # Consulta SQL para obtener las ventas dentro del rango de fechas
        query = '''
            SELECT * FROM vista_ventas
            WHERE `fecha venta` >= %s AND `fecha venta` <= %s
        '''
        cursor.execute(query, (start_date, end_date))
        
        # Recuperar todos los resultados
        sales = cursor.fetchall()
        return sales

    except mysql.connector.Error as e:
        # Manejo de errores de la base de datos
        return {"error": f"Database error: {str(e)}"}
    
    except Exception as e:
        # Manejo de otros errores
        return {"error": f"Unexpected error: {str(e)}"}
    
    finally:
        # Asegurar que los recursos se cierren correctamente
        if 'cursor' in locals() and cursor:
            cursor.close()
        if 'conn' in locals() and conn:
            conn.close()



class Client:
    def __init__(self, id_client='', name_client='', lastName_client='', age_client='', numberPhone_client='', email_client='', direction_client='', id_disease=''):
        self.id_client = id_client
        self.name_client = name_client
        self.lastName_client = lastName_client
        self.age_client = age_client
        self.numberPhone_client = numberPhone_client
        self.email_client = email_client
        self.direction_client = direction_client
        self.id_disease = id_disease

    @staticmethod
    def get_all():
        clients = []
        with mydb.cursor(dictionary=True) as cursor:
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
                                id_disease=row["nombre padecimiento"])
                clients.append(client)
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
        with mydb.cursor(dictionary=True) as cursor:
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
        return products
    
def count_sales():
    with mydb.cursor(dictionary=True) as cursor:
        cursor.execute("SELECT COUNT(*) FROM sales_sgipo")
        result = cursor.fetchone()
        return result['COUNT(*)']
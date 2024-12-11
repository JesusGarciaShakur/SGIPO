from .db import get_connection

mydb = get_connection()
#id_return,id_sale,reason,date_return

class Return:
    def __init__(self, id_return='', id_sale='', reason='', date_return=''):
        self.id_return = id_return
        self.id_sale = id_sale
        self.reason = reason
        self.date_return = date_return

    def save(self):
        with mydb.cursor() as cursor:
            sql = "INSERT INTO returns_sgipo(id_sale, reason, date_return) VALUES(%s, %s, %s)"
            values = (self.id_sale, self.reason, self.date_return)
            cursor.execute(sql, values)
        mydb.commit()

    def update(self):
        with mydb.cursor() as cursor:
            sql = "UPDATE returns_sgipo SET id_sale=%s, reason=%s, date_return=%s WHERE id_return=%s"
            values = (self.id_sale, self.reason, self.date_return, self.id_return)
            cursor.execute(sql, values)
            mydb.commit()
        return self.id_return
    
    def delete(self):
        with mydb.cursor() as cursor:
            sql = f"DELETE FROM returns_sgipo WHERE id_return = {self.id_return}"
            cursor.execute(sql)
            mydb.commit()
        return self.id_return
    
    @staticmethod
    def get(id_return):
        with mydb.cursor(dictionary=True) as cursor:
            sql = f"SELECT * FROM returns_sgipo WHERE id_return = {id_return}"
            cursor.execute(sql)
            return_ = cursor.fetchone()
            if return_:
                return_ = Return(id_return=return_["id_return"],
                                id_sale=return_["id_sale"],
                                reason=return_["reason"],
                                date_return=return_["date_return"])
                return return_
            return None
        
    @staticmethod
    def get_all():
        returns = []
        connection = get_connection()
        with connection.cursor(dictionary=True) as cursor:
            sql = "SELECT * FROM returns_sgipo"
            cursor.execute(sql)
            result = cursor.fetchall()
            for row in result:
                return_ = Return(id_return=row["id_return"],
                                id_sale=row["id_sale"],
                                reason=row["reason"],
                                date_return=row["date_return"])
                returns.append(return_)
        connection.close()
        return returns
    
    @staticmethod
    def get_paginated_returns(page, per_page):
        returns = []
        offset = (page - 1) * per_page
        connection = get_connection()
        with connection.cursor(dictionary=True) as cursor:
            # Obtener el número total de registros
            cursor.execute("SELECT COUNT(*) FROM returns_sgipo")
            total = cursor.fetchone()['COUNT(*)']
            
            cursor.execute("SELECT * FROM returns_sgipo ORDER BY 'id_return'DESC LIMIT %s OFFSET %s", (per_page, offset))
            result = cursor.fetchall()
            for row in result:
                return_ = Return(id_return=row["id_return"],
                                id_sale=row["id_sale"],
                                reason=row["reason"],
                                date_return=row["date_return"])
                returns.append(return_)
        connection.close()
        return returns, total
    
    @staticmethod
    def search(query, page, per_page):
        offset = (page - 1) * per_page
        returns = []

        with mydb.cursor(dictionary=True) as cursor:
            cursor.execute("""SELECT COUNT(*) FROM vista_devoluciones
                WHERE `fecha venta` LIKE %s OR `razon` LIKE %s
                OR `fecha devolucion` LIKE %s
            """, (query, query, query))
            total = cursor.fetchone()['COUNT(*)']

            cursor.execute("""SELECT * FROM vista_devoluciones
                WHERE `fecha venta` LIKE %s OR `razon` LIKE %s
                OR `fecha devolucion` LIKE %s
                ORDER BY `id devolucion` DESC LIMIT %s OFFSET %s
            """, (query, query, query, per_page, offset))
            result = cursor.fetchall()
            for row in result:
                return_ = Return(id_return=row["id devolucion"],
                                id_sale=row["fecha venta"],
                                reason=row["razon"],
                                date_return=row["fecha devolucion"])
                returns.append(return_)
        return returns, total
    
class Sale:
    def __init__(self, id_sale='', id_client='', id_product='', quantity_sold='', final_price='', date_sold=''):
        self.id_sale = id_sale
        self.id_client = id_client
        self.id_product = id_product
        self.quantity_sold = quantity_sold
        self.final_price = final_price
        self.date_sold = date_sold

    @staticmethod
    def get_all():
        sales = []
        connection = get_connection()
        with connection.cursor(dictionary=True) as cursor:
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
        connection.close()
        return sales
    
def count_returns():
    with mydb.cursor(dictionary=True) as cursor:
        cursor.execute("SELECT COUNT(*) FROM returns_sgipo")
        result = cursor.fetchone()
        return result['COUNT(*)']
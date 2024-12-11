from .db import get_connection

mydb = get_connection()
#id_repair, objectName_repair, quantity_repaired, cost_repair, date_repair

class Repair:
    def __init__(self, id_repair='', objectName_repair='', quantity_repaired='', cost_repair='', date_repair=''):
        self.id_repair = id_repair
        self.objectName_repair = objectName_repair
        self.quantity_repaired = quantity_repaired
        self.cost_repair = cost_repair
        self.date_repair = date_repair

    def save(self):
        with mydb.cursor() as cursor:
            sql = "INSERT INTO repairs_sgipo (objectName_repair, quantity_repaired, cost_repair, date_repair) VALUES (%s, %s, %s, %s)"
            values = (self.objectName_repair, self.quantity_repaired, self.cost_repair, self.date_repair)
            cursor.execute(sql, values)
        mydb.commit()

    def update(self):
        with mydb.cursor() as cursor:
            sql = "UPDATE repairs_sgipo SET objectName_repair=%s, quantity_repaired=%s, cost_repair=%s, date_repair=%s WHERE id_repair=%s"
            values = (self.objectName_repair, self.quantity_repaired, self.cost_repair, self.date_repair, self.id_repair)
            #revisar errores
            print(f"SQL: {sql}")
            print(f"Values: {values}")
            cursor.execute(sql, values)
            mydb.commit()
        return self.id_repair
    
    def delete(self):
        with mydb.cursor() as cursor:
            sql = f"DELETE FROM repairs_sgipo WHERE id_repair = {self.id_repair}"
            cursor.execute(sql)
            mydb.commit()
        return self.id_repair
    
    @staticmethod
    def get(id_repair):
        with mydb.cursor(dictionary=True) as cursor:
            sql = f"SELECT * FROM repairs_sgipo WHERE id_repair = {id_repair}"
            cursor.execute(sql)
            repair = cursor.fetchone()
            if  repair:
                repair = Repair(id_repair=repair["id_repair"],
                                objectName_repair=repair["objectName_repair"],
                                quantity_repaired=repair["quantity_repaired"],
                                cost_repair=repair["cost_repair"],
                                date_repair=repair["date_repair"])
                return repair
            return None
        
    @staticmethod
    def get_all():
        repairs = []
        connection = get_connection()
        with connection.cursor(dictionary=True) as cursor:
            sql = "SELECT * FROM repairs_sgipo"
            cursor.execute(sql)
            result = cursor.fetchall()
            for row in result:
                repair = Repair(id_repair=row["id_repair"],
                                objectName_repair=row["objectName_repair"],
                                quantity_repaired=row["quantity_repaired"],
                                cost_repair=row["cost_repair"],
                                date_repair=row["date_repair"])
                repairs.append(repair)
        connection.close()
        return repairs
    
    @staticmethod
    def get_paginated_repairs(page, per_page):
        repairs = []
        offset = (page - 1) * per_page
        connection = get_connection()
        with connection.cursor(dictionary=True) as cursor:
            cursor.execute("SELECT COUNT(*) FROM repairs_sgipo")
            total = cursor.fetchone()['COUNT(*)']
            
            cursor.execute("SELECT * FROM repairs_sgipo ORDER BY 'id_repair'DESC LIMIT %s OFFSET %s", (per_page, offset))
            result = cursor.fetchall()
            for row in result:
                repair = Repair(id_repair=row["id_repair"],
                                objectName_repair=row["objectName_repair"],
                                quantity_repaired=row["quantity_repaired"],
                                cost_repair=row["cost_repair"],
                                date_repair=row["date_repair"])
                repairs.append(repair)
        connection.close()
        return repairs, total
    
    @staticmethod
    def search(query, page, per_page):
        offset = (page - 1) * per_page
        repairs = []
        search_query = f"%{query}%"

        with mydb.cursor(dictionary=True) as cursor:
            cursor.execute("""SELECT COUNT(*) FROM repairs_sgipo
                WHERE `objectName_repair` LIKE %s OR `quantity_repaired` LIKE %s
                OR `cost_repair` LIKE %s OR `date_repair` LIKE %s
            """, (search_query, search_query, search_query, search_query))
            total = cursor.fetchone()['COUNT(*)']

            cursor.execute("""SELECT * FROM repairs_sgipo
                WHERE `objectName_repair` LIKE %s OR `quantity_repaired` LIKE %s
                OR `cost_repair` LIKE %s OR `date_repair` LIKE %s
                ORDER BY `id_repair` DESC LIMIT %s OFFSET %s
            """, (search_query, search_query, search_query, search_query, per_page, offset))
            result = cursor.fetchall()

            for row in result:
                repair = Repair(id_repair=row["id_repair"],
                                objectName_repair=row["objectName_repair"],
                                quantity_repaired=row["quantity_repaired"],
                                cost_repair=row["cost_repair"],
                                date_repair=row["date_repair"])
                repairs.append(repair)
        return repairs, total
    
def count_repairs():
    with mydb.cursor(dictionary=True) as cursor:
        cursor.execute("SELECT COUNT(*) FROM repairs_sgipo")
        result = cursor.fetchone()
        return result['COUNT(*)']
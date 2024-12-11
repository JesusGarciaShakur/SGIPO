from .db import get_connection

mydb = get_connection()
#id_supplier, name_supplier, direction_supplier ,rfc_supplier ,contact_supplier
class Supplier:
    def __init__(self, id_supplier='', name_supplier='', direction_supplier='', rfc_supplier='', contact_supplier=''):
        self.id_supplier = id_supplier
        self.name_supplier = name_supplier
        self.direction_supplier = direction_supplier
        self.rfc_supplier = rfc_supplier
        self.contact_supplier = contact_supplier

    def save(self):
        with mydb.cursor() as cursor:
            sql = "INSERT INTO suppliers_sgipo(name_supplier, direction_supplier, rfc_supplier, contact_supplier) VALUES (%s, %s, %s, %s)"
            values = (self.name_supplier, self.direction_supplier, self.rfc_supplier, self.contact_supplier)
            cursor.execute(sql, values)
        mydb.commit()

    
    def update(self):
        with mydb.cursor() as cursor:
            sql = "UPDATE suppliers_sgipo SET name_supplier = %s, direction_supplier = %s, rfc_supplier = %s, contact_supplier = %s WHERE id_supplier = %s"
            values = (self.name_supplier, self.direction_supplier, self.rfc_supplier, self.contact_supplier, self.id_supplier)
            #revisar errores
            print(f"SQL: {sql}")
            print(f"Values: {values}")
            cursor.execute(sql, values)
            mydb.commit()
        return self.id_supplier
    
    def delete(self):
        with mydb.cursor() as cursor:
            sql = f"DELETE FROM suppliers_sgipo WHERE id_supplier = {self.id_supplier}"
            cursor.execute(sql)
            mydb.commit()
        return self.id_supplier
    
    @staticmethod
    def get(id_supplier):
        with mydb.cursor(dictionary=True) as cursor:
            sql = f"SELECT * FROM suppliers_sgipo WHERE id_supplier = {id_supplier}"
            cursor.execute(sql)
            supplier = cursor.fetchone()
            if supplier:
                supplier = Supplier(id_supplier=supplier["id_supplier"],
                                    name_supplier=supplier["name_supplier"],
                                    direction_supplier=supplier["direction_supplier"],
                                    rfc_supplier=supplier["rfc_supplier"],
                                    contact_supplier=supplier["contact_supplier"])
                return supplier
            return None
        
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
    
    @staticmethod
    def get_paginated_suppliers(page, per_page):
        suppliers = []
        offset = (page - 1) * per_page
        connection = get_connection()
        with connection.cursor(dictionary=True) as cursor:
            cursor.execute("SELECT COUNT(*) FROM suppliers_sgipo")
            total = cursor.fetchone()['COUNT(*)']

            cursor.execute("""SELECT * FROM suppliers_sgipo ORDER BY `id_supplier` DESC LIMIT %s OFFSET %s""", (per_page, offset))
            result = cursor.fetchall()
            for row in result:
                supplier = Supplier(id_supplier=row["id_supplier"],
                                    name_supplier=row["name_supplier"],
                                    direction_supplier=row["direction_supplier"],
                                    rfc_supplier=row["rfc_supplier"],
                                    contact_supplier=row["contact_supplier"])
                suppliers.append(supplier)
        connection.close()
        return suppliers, total

    @staticmethod
    def search(query, page, per_page):
        offset = (page - 1) * per_page
        suppliers = []
        search_query = f"%{query}%"

        with mydb.cursor(dictionary=True) as cursor:
            cursor.execute("""SELECT COUNT(*) FROM suppliers_sgipo
                WHERE `name_supplier` LIKE %s OR `direction_supplier` LIKE %s
                OR `rfc_supplier` LIKE %s OR `contact_supplier` LIKE %s""",
                (search_query, search_query, search_query, search_query))
            total = cursor.fetchone()['COUNT(*)']

            cursor.execute("""SELECT * FROM suppliers_sgipo
                WHERE `name_supplier` LIKE %s OR `direction_supplier` LIKE %s
                OR `rfc_supplier` LIKE %s OR `contact_supplier` LIKE %s
                ORDER BY `id_supplier` DESC LIMIT %s OFFSET %s""",
                (search_query, search_query, search_query, search_query, per_page, offset))
            result = cursor.fetchall()

            for row in result:
                supplier = Supplier(id_supplier=row["id_supplier"],
                                    name_supplier=row["name_supplier"],
                                    direction_supplier=row["direction_supplier"],
                                    rfc_supplier=row["rfc_supplier"],
                                    contact_supplier=row["contact_supplier"])
                suppliers.append(supplier)
        return suppliers, total

def count_suppliers():
    with mydb.cursor(dictionary=True) as cursor:
        cursor.execute("SELECT COUNT(*) FROM suppliers_sgipo")
        result = cursor.fetchone()
        return result['COUNT(*)']
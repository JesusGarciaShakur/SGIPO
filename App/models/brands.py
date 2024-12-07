from .db import get_connection

mydb = get_connection()
#id_brand,name_brand ,description_brand ,id_supplier

class Brand:
    def __init__(self, id_brand='', name_brand='', description_brand='', id_supplier='', image_brand=''):
        self.id_brand = id_brand
        self.name_brand = name_brand
        self.description_brand = description_brand
        self.id_supplier = id_supplier
        self.image_brand = image_brand

    def save(self):
        with mydb.cursor() as cursor:
            sql = "INSERT INTO brands_sgipo (name_brand, description_brand, id_supplier, image_brand) VALUES (%s, %s, %s, %s)"
            values = (self.name_brand, self.description_brand, self.id_supplier, self.image_brand)
            cursor.execute(sql, values)
        mydb.commit()

    def update(self):
        with mydb.cursor() as cursor:
            sql = "UPDATE brands_sgipo SET name_brand = %s, description_brand = %s, id_supplier = %s, image_brand = %s WHERE id_brand = %s"
            values = (self.name_brand, self.description_brand, self.id_supplier, self.image_brand, self.id_brand )
            cursor.execute(sql, values)
            mydb.commit()
        return self.id_brand

    def delete(self):
        with mydb.cursor() as cursor:
            sql = f"DELETE FROM brands_sgipo WHERE id_brand = {self.id_brand}"
            cursor.execute(sql)
            mydb.commit()
        return self.id_brand
    
    @staticmethod
    def get(id_brand):
        with mydb.cursor(dictionary=True) as cursor:
            sql = f"SELECT * FROM brands_sgipo WHERE id_brand = {id_brand}"
            cursor.execute(sql)
            brand = cursor.fetchone()
            if brand:
                brand = Brand(id_brand=brand["id_brand"],
                            name_brand=brand["name_brand"],
                            description_brand=brand["description_brand"],
                            id_supplier=brand["id_supplier"],
                            image_brand=brand["image_brand"])
                return brand
            return None
    
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
                            id_supplier=row["nombre proveedor"],
                            image_brand=row["imagen marca"])
                brands.append(brand)
        return brands

    @staticmethod
    def get_paginated_brands(page, per_page):
        offset = (page - 1) * per_page
        brands = []
        with mydb.cursor(dictionary=True) as cursor:
            cursor.execute("SELECT COUNT(*) FROM vista_marcas")
            total = cursor.fetchone()['COUNT(*)']

            cursor.execute("SELECT * FROM vista_marcas LIMIT %s OFFSET %s", (per_page, offset))
            result = cursor.fetchall()
            for row in result:
                brand = Brand(id_brand=row["id de marca"],
                            name_brand=row["nombre de marca"],
                            description_brand=row["descripcion marca"],
                            id_supplier=row["nombre proveedor"],
                            image_brand=row["imagen marca"])
                brands.append(brand)
        return brands, total

    @staticmethod
    def search(query, page, per_page):
        offset = (page - 1) * per_page
        brands = []
        search_query = f"%{query}%"

        with mydb.cursor(dictionary=True) as cursor:
            cursor.execute("""SELECT COUNT(*) FROM vista_marcas
                            WHERE `nombre de marca` LIKE %s OR `descripcion marca` LIKE %s OR `nombre proveedor` LIKE %s""", (search_query, search_query, search_query))
            total = cursor.fetchone()['COUNT(*)']

            cursor.execute("""SELECT * FROM vista_marcas
                            WHERE `nombre de marca` LIKE %s OR `descripcion marca` LIKE %s OR `nombre proveedor` LIKE %s
                            LIMIT %s OFFSET %s""", (search_query, search_query, search_query, per_page, offset))
            result = cursor.fetchall()

            for row in result:
                brand = Brand(id_brand=row["id de marca"],
                            name_brand=row["nombre de marca"],
                            description_brand=row["descripcion marca"],
                            id_supplier=row["nombre proveedor"],
                            image_brand=row["imagen marca"])
                brands.append(brand)
        return brands, total

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
        with mydb.cursor(dictionary=True) as cursor:
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
        return suppliers

def count_brands():
    with mydb.cursor(dictionary=True) as cursor:
        cursor.execute("SELECT COUNT(*) FROM brands_sgipo")
        result = cursor.fetchone()
        return result['COUNT(*)']
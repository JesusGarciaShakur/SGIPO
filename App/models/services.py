from .db import get_connection

mydb = get_connection()

#id_service, name_service, description_service
class Service:
    def __init__(self, id_service='', name_service='', description_service=''):
        self.id_service = id_service
        self.name_service = name_service
        self.description_service = description_service

    def save(self):
        with mydb.cursor() as cursor:
            sql = "INSERT INTO services_sgipo (name_service, description_service) VALUES (%s, %s)"
            values = (self.name_service, self.description_service)
            cursor.execute(sql, values)
        mydb.commit()

    def update(self):
        with mydb.cursor() as cursor:
            sql = "UPDATE services_sgipo SET name_service=%s, description_service=%s WHERE id_service=%s"
            values = (self.name_service, self.description_service, self.id_service)
            cursor.execute(sql, values)
            mydb.commit()
        return self.id_service
    
    def delete(self):
        with mydb.cursor() as cursor:
            sql = f"DELETE FROM services_sgipo WHERE id_service = {self.id_service}"
            cursor.execute(sql)
            mydb.commit()
        return self.id_service
    
    @staticmethod
    def get(id_service):
        with mydb.cursor(dictionary=True) as cursor:
            sql = f"SELECT * FROM services_sgipo WHERE id_service = {id_service}"
            cursor.execute(sql)
            service = cursor.fetchone()
            if  service:
                service = Service(id_service=service["id_service"],
                                name_service=service["name_service"],
                                description_service=service["description_service"])
                return service
            return None
        
    @staticmethod
    def __get__(id_service):
        with mydb.cursor(dictionary=True) as cursor:
            sql = f"SELECT * FROM services_sgipo WHERE id_service = {id_service}"
            cursor.execute(sql)
            service = cursor.fetchone()
            if  service:
                service = Service(id_service=service["id_service"],
                                name_service=service["name_service"],
                                description_service=service["description_service"])
                return service
            return None
        
    @staticmethod
    def get_all():
        with mydb.cursor(dictionary=True) as cursor:
            sql = "SELECT * FROM services_sgipo"
            cursor.execute(sql)
            result = cursor.fetchall()
            services = []
            for row in result:
                service = Service(id_service=row["id_service"],
                                name_service=row["name_service"],
                                description_service=row["description_service"])
                services.append(service)
        return services
    
    @staticmethod
    def get_paginated_services(page, per_page):
            offset = (page - 1) * per_page
            with mydb.cursor(dictionary=True) as cursor:
                cursor.execute("SELECT COUNT(*) FROM services_sgipo")
                total = cursor.fetchone()['COUNT(*)']
                
                cursor.execute("SELECT * FROM services_sgipo ORDER BY 'id_service'DESC LIMIT %s OFFSET %s", (per_page, offset))
                result = cursor.fetchall()
                services = []
                for row in result:
                    service = Service(id_service=row["id_service"],
                                    name_service=row["name_service"],
                                    description_service=row["description_service"])
                    services.append(service)
            return services, total
    @staticmethod
    def search(query, page, per_page):
            offset = (page - 1) * per_page
            services = []
            search_query = f"%{query}%"

            with mydb.cursor(dictionary=True) as cursor:
                cursor.execute("""SELECT COUNT(*) FROM services_sgipo
                    WHERE `name_service` LIKE %s OR `description_service` LIKE %s
                """, (search_query, search_query))
                total = cursor.fetchone()['COUNT(*)']

                cursor.execute("""SELECT * FROM services_sgipo
                    WHERE `name_service` LIKE %s OR `description_service` LIKE %s
                    ORDER BY `id_service` DESC LIMIT %s OFFSET %s
                """, (search_query, search_query, per_page, offset))
                result = cursor.fetchall()

                for row in result:
                    service = Service(id_service=row["id_service"],
                                    name_service=row["name_service"],
                                    description_service=row["description_service"])
                    services.append(service)
            return services, total

def count_services():
        with mydb.cursor(dictionary=True) as cursor:
            cursor.execute("SELECT COUNT(*) FROM services_sgipo")
            result = cursor.fetchone()
            return result['COUNT(*)']
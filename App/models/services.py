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
        services = []
        connection = get_connection()
        with connection.cursor(dictionary=True) as cursor:
            sql = "SELECT * FROM services_sgipo"
            cursor.execute(sql)
            result = cursor.fetchall()
            for row in result:
                service = Service(id_service=row["id_service"],
                                name_service=row["name_service"],
                                description_service=row["description_service"])
                services.append(service)
        connection.close()
        return services
    
    @staticmethod
    def get_paginated_services(page, per_page):
            services = []
            offset = (page - 1) * per_page
            connection = get_connection()
            with connection.cursor(dictionary=True) as cursor:
                cursor.execute("SELECT COUNT(*) FROM services_sgipo")
                total = cursor.fetchone()['COUNT(*)']
                
                cursor.execute("SELECT * FROM services_sgipo ORDER BY 'id_service'DESC LIMIT %s OFFSET %s", (per_page, offset))
                result = cursor.fetchall()
                for row in result:
                    service = Service(id_service=row["id_service"],
                                    name_service=row["name_service"],
                                    description_service=row["description_service"])
                    services.append(service)
            connection.close()
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
        
#id_request, id_service, id_client, date_request, price_request
class ServiceRequest:
    def __init__(self, id_request='', id_service='', id_client='', date_request='', price_request=''):
        self.id_request = id_request
        self.id_service = id_service
        self.id_client = id_client
        self.date_request = date_request
        self.price_request = price_request

    def save(self):
        with mydb.cursor() as cursor:
            sql = "INSERT INTO servicerequests_sgipo (id_service, id_client, date_request, price_request) VALUES (%s, %s, %s, %s)"
            values = (self.id_service, self.id_client, self.date_request, self.price_request)
            cursor.execute(sql, values)
        mydb.commit()

    def update(self):
        with mydb.cursor() as cursor:
            sql = "UPDATE servicerequests_sgipo SET id_service=%s, id_client=%s, date_request=%s, price_request=%s WHERE id_request=%s"
            values = (self.id_service, self.id_client, self.date_request, self.price_request, self.id_request)
            cursor.execute(sql, values)
            mydb.commit()
        return self.id_request
    
    def delete(self):
        with mydb.cursor() as cursor:
            sql = f"DELETE FROM servicerequests_sgipo WHERE id_request = {self.id_request}"
            cursor.execute(sql)
            mydb.commit()
        return self.id_request
    
    @staticmethod
    def get(id_request):
        with mydb.cursor(dictionary=True) as cursor:
            sql = f"SELECT * FROM servicerequests_sgipo WHERE id_request = {id_request}"
            cursor.execute(sql)
            service_request = cursor.fetchone()
            if  service_request:
                service_request = ServiceRequest(id_request=service_request["id_request"],
                                id_service=service_request["id_service"],
                                id_client=service_request["id_client"],
                                date_request=service_request["date_request"],
                                price_request=service_request["price_request"])
                return service_request
            return None
    
    def get_all():
        service_requests = []
        connection = get_connection()
        with connection.cursor(dictionary=True) as cursor:
            sql = "SELECT * FROM vista_solicitudservicios"
            cursor.execute(sql)
            result = cursor.fetchall()
            for row in result:
                service_request = ServiceRequest(id_request=row["id de solicitud"],
                                id_service=row["nombre de servicio"],
                                id_client=row["nombre de cliente"],
                                date_request=row["fecha de solicitud"],
                                price_request=row["precio a cobrar"])
                service_requests.append(service_request)
        connection.close()
        return service_requests
    
    @staticmethod
    def get_paginated_service_requests(page, per_page):
        service_requests = []
        offset = (page - 1) * per_page
        connection = get_connection()
        with connection.cursor(dictionary=True) as cursor:
            # Obtener el número total de registros
            cursor.execute("SELECT COUNT(*) FROM vista_solicitudservicios")
            total = cursor.fetchone()['COUNT(*)']

            # Consulta para recuperar los datos, incluyendo el apellido
            cursor.execute("""
                SELECT 
                    `id de solicitud`,
                    `nombre de servicio`,
                    `nombre de cliente`,
                    `apellido cliente`,
                    `fecha de solicitud`,
                    `precio a cobrar`
                FROM vista_solicitudservicios
                ORDER BY `id de solicitud` DESC
                LIMIT %s OFFSET %s
            """, (per_page, offset))
            result = cursor.fetchall()
            # Construir la lista de `service_requests`
            for row in result:
                service_request = ServiceRequest(
                    id_request=row["id de solicitud"],
                    id_service=row["nombre de servicio"],
                    id_client=f"{row['nombre de cliente']} {row['apellido cliente']}",  # Combina nombre y apellido
                    date_request=row["fecha de solicitud"],
                    price_request=row["precio a cobrar"]
                )
                service_requests.append(service_request)
        connection.close()
        return service_requests, total

    
    @staticmethod
    def search(query, page, per_page):
        offset = (page - 1) * per_page
        service_requests = []
        search_query = f"%{query}%"

        with mydb.cursor(dictionary=True) as cursor:
            # Obtener el total de resultados
            cursor.execute("""
                SELECT COUNT(*) FROM vista_solicitudservicios
                WHERE `nombre de servicio` LIKE %s OR `nombre de cliente` LIKE %s
                OR `fecha de solicitud` LIKE %s OR `precio a cobrar` LIKE %s
            """, (search_query, search_query, search_query, search_query))
            total = cursor.fetchone()['COUNT(*)']

            # Obtener los resultados paginados
            cursor.execute("""
                SELECT * FROM vista_solicitudservicios
                WHERE `nombre de servicio` LIKE %s OR `nombre de cliente` LIKE %s
                OR `fecha de solicitud` LIKE %s OR `precio a cobrar` LIKE %s
                ORDER BY `id de solicitud` DESC LIMIT %s OFFSET %s
            """, (search_query, search_query, search_query, search_query, per_page, offset))
            result = cursor.fetchall()

            # Construir objetos ServiceRequest
            for row in result:
                service_request = ServiceRequest(
                    id_request=row["id de solicitud"],
                    id_service=row["nombre de servicio"],
                    id_client=row["nombre de cliente"],
                    date_request=row["fecha de solicitud"],
                    price_request=row["precio a cobrar"]
                )
                service_requests.append(service_request)  # Mover esta línea dentro del bucle

        return service_requests, total

    


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
                                id_disease=row["nombre padecimiento"])
                clients.append(client)
        connection.close()
        return clients
    
def count_service_requests():
    with mydb.cursor(dictionary=True) as cursor:
        cursor.execute("SELECT COUNT(*) FROM servicerequests_sgipo")
        result = cursor.fetchone()
        return result['COUNT(*)']
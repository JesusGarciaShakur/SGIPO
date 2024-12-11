from .db import get_connection

mydb = get_connection()
# id_client, name_client, lastName_client, age_client, numberPhone_client, email_client, direction_client, id_disease
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

    def save(self):
        with mydb.cursor() as cursor:
            sql = "INSERT INTO clients_sgipo (name_client, lastName_client, age_client, numberPhone_client, email_client, direction_client, id_disease) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            values = (self.name_client, self.lastName_client, self.age_client, self.numberPhone_client, self.email_client, self.direction_client, self.id_disease)
            cursor.execute(sql, values)
        mydb.commit()

    def update(self):
        with mydb.cursor() as cursor:
            sql = "UPDATE clients_sgipo SET name_client=%s, lastName_client=%s, age_client=%s, numberPhone_client=%s, email_client=%s, direction_client=%s, id_disease=%s WHERE id_client=%s"
            values = (self.name_client, self.lastName_client, self.age_client, self.numberPhone_client, self.email_client, self.direction_client, self.id_disease, self.id_client)
            cursor.execute(sql, values)
            mydb.commit()
        return self.id_client
    
    def delete(self):
        with mydb.cursor() as cursor:
            sql = f"DELETE FROM clients_sgipo WHERE id_client = {self.id_client}"
            cursor.execute(sql)
            mydb.commit()
        return self.id_client
    
    @staticmethod
    def get(id_client):
        with mydb.cursor(dictionary=True) as cursor:
            sql = f"SELECT * FROM clients_sgipo WHERE id_client = {id_client}"
            cursor.execute(sql)
            client = cursor.fetchone()
            if  client:
                client = Client(id_client=client["id_client"],
                                name_client=client["name_client"],
                                lastName_client=client["lastName_client"],
                                age_client=client["age_client"],
                                numberPhone_client=client["numberPhone_client"],
                                email_client=client["email_client"],
                                direction_client=client["direction_client"],
                                id_disease=client["id_disease"])
                return client
            return None
    
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
    
    @staticmethod
    def get_paginated_clients(page, per_page):
        clients = []
        offset = (page - 1) * per_page
        connection = get_connection()
        with connection.cursor(dictionary=True) as cursor:
            cursor.execute("SELECT COUNT(*) FROM vista_clientes")
            total = cursor.fetchone()['COUNT(*)']
            
            cursor.execute("SELECT * FROM vista_clientes ORDER BY `id de cliente` DESC LIMIT %s OFFSET %s", (per_page, offset))
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
        return clients, total
    
    @staticmethod
    def search(query, page, per_page):
        offset = (page - 1) * per_page
        clients = []
        search_query = f"%{query}%"

        with mydb.cursor(dictionary=True) as cursor:
            cursor.execute("""
                SELECT COUNT(*) FROM vista_clientes
                WHERE `nombre` LIKE %s  OR `apellido` LIKE %s
                OR `edad` LIKE %s OR `numero de telefono` LIKE %s
                OR `correo electronico` LIKE %s OR `direccion` LIKE %s
                OR `nombre padecimiento` LIKE %s
            """, (search_query, search_query, search_query, search_query, search_query, search_query, search_query))
            total = cursor.fetchone()['COUNT(*)']

            cursor.execute("""
                SELECT * FROM vista_clientes
                WHERE `nombre` LIKE %s  OR `apellido` LIKE %s
                OR `edad` LIKE %s OR `numero de telefono` LIKE %s
                OR `correo electronico` LIKE %s OR `direccion` LIKE %s
                OR `nombre padecimiento` LIKE %s
                ORDER BY `id de cliente` DESC LIMIT %s OFFSET %s
            """, (search_query, search_query, search_query, search_query, search_query, search_query, search_query, per_page, offset))
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
        return clients, total

class Disease:
    def __init__(self, id_disease='', name_disease='', description_disease=''):
        self.id_disease = id_disease
        self.name_disease = name_disease
        self.description_disease = description_disease

    @staticmethod
    def get_all():
        diseases = []
        connection = get_connection()
        with connection.cursor(dictionary=True) as cursor:
            sql = "SELECT * FROM chronic_diseases_sgipo"
            cursor.execute(sql)
            result = cursor.fetchall()
            for row in result:
                disease = Disease(id_disease=row["id_disease"], name_disease=row["name_disease"])
                diseases.append(disease)
        connection.close()
        return diseases
    
def count_clients():
    with mydb.cursor(dictionary=True) as cursor:
        cursor.execute("SELECT COUNT(*) FROM clients_sgipo")
        result = cursor.fetchone()
        return result['COUNT(*)']
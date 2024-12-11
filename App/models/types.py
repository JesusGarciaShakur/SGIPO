from .db import get_connection

mydb = get_connection()

class Type:
    def __init__(self, id_rol='', name_rol=''):
        self.id_rol = id_rol
        self.name_rol = name_rol

    @staticmethod
    def get(id_rol):
        with mydb.cursor(dictionary=True) as cursor:
            sql = f"SELECT * FROM roles_sgipo WHERE id_rol = { id_rol }"
            cursor.execute(sql)
            type = cursor.fetchone()
            if type:
                type = Type(id_rol=type["id_rol"],
                            name_rol=type["name_rol"])
                return type
            return None
    
    @staticmethod
    def __get__(id_rol):
        with mydb.cursor(dictionary=True) as cursor:
            sql = f"SELECT * FROM roles_sgipo WHERE id_rol = { id_rol }"
            cursor.execute(sql)
            type = cursor.fetchone()
            if type:
                type = Type(id_rol=type["id_rol"],
                            name_rol=type["name_rol"])
                return type
            return None

    @staticmethod
    def get_all():
        types = []
        connection = get_connection()
        with connection.cursor(dictionary=True) as cursor:
            sql = "SELECT * FROM roles_sgipo"
            cursor.execute(sql)
            result = cursor.fetchall()
            for row in result:
                type = Type(id_rol=row["id_rol"],
                            name_rol=row["name_rol"])
                types.append(type)
        connection.close()
        return types
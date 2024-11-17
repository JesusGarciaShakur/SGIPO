#models/users.py
from .db import get_connection
from werkzeug.security import generate_password_hash, check_password_hash

mydb = get_connection()

class User:
    def __init__(self, id_user='', userName_user = '', password_user='', id_rol='', name_user='', lastName_user='', numberPhone_user='', image_user=''):
        self.id_user = id_user
        self.userName_user = userName_user
        self.password_user = password_user
        self.id_rol = id_rol
        self.name_user = name_user
        self.lastName_user = lastName_user
        self.numberPhone_user = numberPhone_user
        self.image_user = image_user


    def save(self):
        with mydb.cursor() as cursor:
            self.password_user = generate_password_hash(self.password_user)
            sql = "INSERT INTO users_sgipo (userName_user, password_user, id_rol, name_user, lastName_user, numberPhone_user, image_user) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            values = (self.userName_user, self.password_user, self.id_rol, self.name_user, self.lastName_user, self.numberPhone_user, self.image_user)
            cursor.execute(sql, values)
        mydb.commit() 

    def update(self):
        with mydb.cursor() as cursor:
            self.password_user = generate_password_hash(self.password_user)
            sql = "INSERT users_sgipo SET userName_user=%s, password_user=%s, id_rol=%s, name_user=%s, lastName_user=%s, numberPhone_user=%s, image_user WHERE id_user=%s)"
            values = (self.userName_user, self.password_user, self.id_rol, self.name_user, self.lastName_user, self.numberPhone_user, self.image_user, self.id_user)
            #revisar errores
            #print(f"SQL: {sql}")
            #print(f"Values: {values}")
            cursor.execute(sql, values)
            mydb.commit()
        return self.id_user 

    def delete(self):
        with mydb.cursor() as cursor:
            sql = f"DELETE FROM users_sgipo WHERE id_user = { self.id_user }"
            cursor.execute(sql)
            mydb.commit()
        return self.id_user

    @staticmethod
    def get(id_user):
        with mydb.cursor(dictionary=True) as cursor:
            sql = f"SELECT * FROM users_sgipo WHERE id_user = { id_user }"
            cursor.execute(sql)
            user = cursor.fetchone()
            if user:
                user = User(id_user=user["id_user"],
                            userName_user=user["userName_user"],
                            password_user=user["password_user"],
                            id_rol=user["id_rol"],
                            name_user=user["name_user"],
                            lastName_user=user["lastName_user"],
                            numberPhone_user=user["numberPhone_user"],
                            image_user=user["image_user"])
                return user
            return None

    @staticmethod
    def __get__(id_user):
        with mydb.cursor(dictionary=True) as cursor:
            sql = f"SELECT * FROM users_sgipo WHERE id_user = { id_user }"
            cursor.execute(sql)
            user = cursor.fetchone()
            if user:
                user = User(id_user=user["id_user"],
                            userName_user=user["userName_user"],
                            password_user=user["password_user"],
                            id_rol=user["id_rol"],
                            name_user=user["name_user"],
                            lastName_user=user["lastName_user"],
                            numberPhone_user=user["numberPhone_user"],
                            image_user=user["image_user"])
                return user
            return None

#id_user, userName_user, password_user, id_rol, name_user, lastName_user, numberPhone_user, image_user
    @staticmethod
    def check_username(userName_user):
        with mydb.cursor(dictionary=True) as cursor:
            sql = "SELECT id_user FROM users_sgipo WHERE userName_user = %s"
            cursor.execute(sql, (userName_user,))
            result = cursor.fetchone()
            return result is not None

    @staticmethod
    def check_password(password_user):
        with mydb.cursor(dictionary=True) as cursor:
            sql = "SELECT id_user FROM users_sgipo WHERE password_user = %s"
            cursor.execute(sql, (password_user,))
            result = cursor.fetchone()
            return result is not None

    @staticmethod
    def check_password_hash(password_user):
        return check_password_hash(self.password_user, password_user) # type: ignore

    @staticmethod
    def get_by_password(userName_user, password_user):
        with mydb.cursor(dictionary=True) as cursor:
            sql = "SELECT id_user, userName_user, password_user FROM users_sgipo WHERE userName_user = %s"
            val = (userName_user,)
            cursor.execute(sql, val)
            user = cursor.fetchone()
            print(user)
            if user != None:
                if check_password_hash(user["password_user"], password_user):
                    return User.__get__(user["id_user"])
            return None

class Type:
    def __init__(self, id_rol='', name_rol=''):
        self.id_rol = id_rol
        self.name_rol = name_rol
    
    @staticmethod
    def get_all():
        types = []
        with mydb.cursor(dictionary=True) as cursor:
            sql = "SELECT * FROM roles_sgipo"
            cursor.execute(sql)
            result = cursor.fetchall()
            print(result)
            for row in result:
                type= Type(id_rol=row["id_rol"], name_rol=row["name_rol"])
                types.append(type)
        return types
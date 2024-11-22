from .db import get_connection
from werkzeug.security import generate_password_hash, check_password_hash

mydb = get_connection()

class Disease:
    def __init__(self, id_disease='', name_disease='', description_disease=''):
        self.id_disease = id_disease
        self.name_disease = name_disease
        self.description_disease = description_disease

    @staticmethod
    def get(id_disease):
        with mydb.cursor(dictionary=True) as cursor:
            sql = f"SELECT * FROM chronic_diseases_sgipo WHERE id_disease = {id_disease}"
            cursor.execute(sql)
            disease = cursor.fetchone()
            if disease:
                disease = Disease(id_disease=disease["id_disease"],
                                name_disease=disease["name_disease"],
                                description_disease=disease["description_disease"])
                return disease
            return None
        
    @staticmethod
    def __get__(id_disease):
        with mydb.cursor(dictionary=True) as cursor:
            sql = f"SELECT * FROM chronic_diseases_sgipo WHERE id_disease = {id_disease}"
            cursor.execute(sql)
            disease = cursor.fetchone()
            if disease:
                disease = Disease(id_disease=disease["id_disease"],
                                name_disease=disease["name_disease"],
                                description_disease=disease["description_disease"])
                return disease
            return None

    @staticmethod
    def get_all():
        diseases = []
        with mydb.cursor(dictionary=True) as cursor:
            sql = "SELECT * FROM chronic_diseases_sgipo"
            cursor.execute(sql)
            result = cursor.fetchall()
            for row in result:
                disease = Disease(id_disease=row["id_disease"],
                                name_disease=row["name_disease"],
                                description_disease=row["description_disease"])
                diseases.append(disease)
        return diseases
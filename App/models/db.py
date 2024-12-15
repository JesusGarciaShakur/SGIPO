
import mysql.connector

def get_connection():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="sgipo1"
    )
    return mydb


import mysql.connector

def get_connection():
    mydb = mysql.connector.connect(
        host="localhost",
        user="shakur",
        password="shaaragy970",
        database="sgipo1"
    )
    return mydb

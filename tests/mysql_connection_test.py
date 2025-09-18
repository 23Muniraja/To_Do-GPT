import mysql.connector
from jupyter_server.auth import passwd

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="muni",
    database="db_to_do-gpt"
)

mycursor = mydb.cursor()

mycursor.execute("SELECT * FROM To_Do ;")
output = mycursor.fetchall()
print(output)
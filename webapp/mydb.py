
import mysql.connector

try:
  database = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = 'kishor@2233#'
  )
  print("Connection Successful!")
  
  cursorObj = database.cursor()
  
  cursorObj.execute("DROP DATABASE IF EXISTS DCRM")
  cursorObj.execute("CREATE DATABASE DCRM")
  
except mysql.connector.Error as error:
  print(f"Error : {error}")

finally:
  if 'database' in locals() and database.is_connected():
    database.close()
    print("MYSQL connected closed")
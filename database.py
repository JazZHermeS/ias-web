import sqlite3

connection = sqlite3.connect("db.sqlite3")

cursor = connection.cursor()

cursor.execute("""CREATE TABLE 
		""")
		
connection.commit()
connection.close()

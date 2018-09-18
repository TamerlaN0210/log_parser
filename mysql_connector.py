import mysql.connector


mydb = mysql.connector.connect(host="localhost", user="root", password="", database="logs_data")
# mycursor = mydb.cursor()
# mycursor.execute("SELECT * FROM books WHERE `author_id` = (SELECT `id` from authors WHERE `full_name` = 'Федор Михайлович Достоевский')")
# for item in mycursor:
#     print(item)

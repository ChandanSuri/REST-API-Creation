import sqlite3

connection = sqlite3.connect('my_data.db')
cursor = connection.cursor()

# INTEGER PRIMARY KEY -> for auto-incrementing it...
create_users_table = "CREATE TABLE IF NOT EXISTS Users (id INTEGER PRIMARY KEY, username text, password text)"
cursor.execute(create_users_table)

create_items_table = "CREATE TABLE IF NOT EXISTS Items (name text, price real)"
cursor.execute(create_items_table)

connection.commit()

connection.close()

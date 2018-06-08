import sqlite3

connection = sqlite3.connect('data.db')
# for selecting some data items from the database and for execution purposes.
# used also for storing the results of any executed query
cursor = connection.cursor()

create_table = "CREATE TABLE Users (id int, username text, password text)"
cursor.execute(create_table)

new_user = (1, "Chandan", "HelloThere")
insert_query = "INSERT INTO Users VALUES (?, ?, ?)"
cursor.execute(insert_query, new_user) # By itself it replaces the ? with data

# how to insert multiple data sets (here users)...
users = [
    (2, "Gaurav Sinha", "GSinha"),
    (3, "Arpita Singh", "ASingh"),
    (4, "Shraddha Singh", "HeheHehe")
]
cursor.executemany(insert_query, users)

# retrieve data
select_query = "SELECT * FROM Users"
for row in cursor.execute(select_query):
    print(row)

# to save all the changes...
connection.commit()

connection.close()

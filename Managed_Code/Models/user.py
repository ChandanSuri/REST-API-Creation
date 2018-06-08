import sqlite3

db_name = "my_data.db"

# this is not a resource and is a helper, an internal representation of this entity

class User:
    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password
    # changes made for sqlite...
    # in case we want to change the name of the class in future, so, that we can reuse the code below
    @classmethod
    def find_by_username(cls, name):
        connection = sqlite3.connect(db_name)
        cursor = connection.cursor()

        select_acc_to_name_query = "SELECT * FROM Users WHERE username=?"
        result = cursor.execute(select_acc_to_name_query, (name, )) # this second argument is a tuple

        row = result.fetchone() # it fetches the first one in the list of rows that may be returned

        if row: # is not None
            # reusability
            # to get the number of arguments acc to the position and not stating them explicitly...
            user = cls(*row)
            #user = cls(row[0], row[1], row[2])
        else:
            user = None
        connection.close()
        return user

    @classmethod
    def find_by_id(cls, _id):
        connection = sqlite3.connect(db_name)
        cursor = connection.cursor()

        select_acc_to_id_query = "SELECT * FROM Users WHERE id=?"
        result = cursor.execute(select_acc_to_id_query, (_id, )) # this second argument is a tuple

        row = result.fetchone() # it fetches the first one in the list of rows that may be returned

        if row: # is not None
            # reusability
            # to get the number of arguments acc to the position and not stating them explicitly...
            user = cls(*row)
            #user = cls(row[0], row[1], row[2])
        else:
            user = None
        connection.close()
        return user

    # changes made for sqlite ends here...

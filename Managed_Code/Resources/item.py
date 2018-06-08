import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

db_name = "my_data.db"

class Item(Resource):

    # Advanced Request Parsing -> for getting some particular arguments from the request, restricting the changes
    parser = reqparse.RequestParser()
    parser.add_argument("price", type = float, required = True, help = "This field cannot be left blank!!!")

    # whenever you need JWT token for authorization use the decorator below...
    @jwt_required()
    def get(self, name):
        item = self.find_by_name(name)
        if item:
            return item
        return {"message" : "Item Not Found..."}, 404

    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect(db_name)
        cursor = connection.cursor()

        select_query = "SELECT * FROM Items WHERE name=?"
        result = cursor.execute(select_query, (name,))
        row = result.fetchone()

        connection.close()

        if row:
            return {"item": {"name": row[0], "price": row[1]}}

    def post(self, name):
        if self.find_by_name(name):
            return {"message": "An item with the name '{}' already exists.".format(name)}, 400 # Bad Request Code

        # Error first approach...
        data = Item.parser.parse_args()
        item = {"name": name, "price": data["price"]}

        try:
            self.insert(item)
        except:
            return {"message": "An error occurred while inserting the item..."}, 500 # Internal Server Error

        return item, 201 # Created Status Code

    @classmethod
    def insert(cls, item):
        connection = sqlite3.connect(db_name)
        cursor = connection.cursor()

        insert_query = "INSERT INTO Items VALUES (?, ?)"
        cursor.execute(insert_query, (item["name"], item["price"]))

        connection.commit()
        connection.close()

    def delete(self, name):
        connection = sqlite3.connect(db_name)
        cursor = connection.cursor()

        delete_query = "DELETE FROM Items WHERE name=?"
        cursor.execute(delete_query, (name,))

        connection.commit()
        connection.close()

        return {"message": "Item is deleted..."}

    def put(self, name):
        data = Item.parser.parse_args()

        item = self.find_by_name(name)
        updated_item = {"name": name, "price": data["price"]}

        if item is None:
            try:
                self.insert(updated_item)
            except:
                return {"message": "An error occurred while inserting the item..."}, 500
        else:
            try:
                self.update(updated_item)
            except:
                return {"message": "An error occurred while updating the item..."}, 500
        return updated_item

    @classmethod
    def update(cls, item):
        connection = sqlite3.connect(db_name)
        cursor = connection.cursor()

        update_query = "UPDATE Items SET price=? WHERE name=?"
        cursor.execute(update_query, (item["price"], item["name"]))

        connection.commit()
        connection.close()

class ItemList(Resource):
    def get(self):
        connection = sqlite3.connect(db_name)
        cursor = connection.cursor()

        select_all_query = "SELECT * FROM Items"
        result = cursor.execute(select_all_query)
        items = []
        for row in result:
            items.append({"name": row[0], "price": row[1]})

        connection.close()

        return {"items": items}

# 200 -> OK Status Code

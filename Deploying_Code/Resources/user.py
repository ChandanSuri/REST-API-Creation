import sqlite3
from flask_restful import Resource, reqparse
from Models.user import User

# clients interact with these resources (entities)...

class UserRegister(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument("username",
        type = str,
        required = True,
        help = "This field cannot be blank..."
    )
    parser.add_argument("password",
        type = str,
        required = True,
        help = "This field cannot be blank..."
    )

    @classmethod
    def post(cls):

        data = cls.parser.parse_args()

        # no duplicate users with user names
        if User.find_by_username(data["username"]):
            return {"message": "A user with that username already exists..."}, 400

        connection = sqlite3.connect(db_name)
        cursor = connection.cursor()

        insert_query = "INSERT INTO Users VALUES (NULL, ?, ?)"
        cursor.execute(insert_query, (data["username"], data["password"]))

        connection.commit()
        connection.close()

        return {"message" : "User Created Succesfully"}, 201 # create response Code

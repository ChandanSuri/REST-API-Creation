from flask import Flask, request
from flask_restful import Resource, Api, reqparse # for request parsing -> reqparse
# if an api returns item, then item is an resource and so on...
# resources can also be mapped to database tables for various purposes...
# resource has to be a class...
from flask_jwt import JWT, jwt_required
from security import authenticate, identity

from user import UserRegister

app = Flask(__name__)
app.secret_key = "Chandan21"
api = Api(app)

jwt = JWT(app, authenticate, identity) # /auth

items = []

class Item(Resource):

    # Advanced Request Parsing -> for getting some particular arguments from the request, restricting the changes
    parser = reqparse.RequestParser()
    parser.add_argument("price", type = float, required = True, help = "This field cannot be left blank!!!")

    # whenever you need JWT token for authorization use the decorator below...
    @jwt_required()
    def get(self, name):
        # next gives us the first item that filter returns according to the condition specified.
        # if nothing is found by filter, we get None in the item and thus, the program is prevented from crashing.
        item = next(filter(lambda x: x["name"] == name, items), None)
        return {"item": item}, 200 if item else 404 # Not Found Status Code

    def post(self, name):
        if next(filter(lambda x: x["name"] == name, items), None):
            return {"message": "An item with the name '{}' already exists.".format(name)}, 400 # Bad Request Code

        # Error first approach...
        data = Item.parser.parse_args()
        # data = request.get_json(force= True) This is used to force this to work even if the content type is not set to JSON.
        # data = request.get_json(silent=True) In case it fails, rather than giving an error, it just returns None.
        # These options can be used, though the first one is not preferred...
        # If an item already exists with the same name then the program below can fail.
        # Thus, we have added the if condition above for bad requests.
        # data = request.get_json()
        item = {"name": name, "price": data["price"]}
        items.append(item)
        return item, 201 # Created Status Code

    def delete(self, name):
        # this global is needed else python will think that items is a local variable
        # and would throw an error saying that the variable is being used before initialised.
        # to overcome that situation we have to use global to explicitly state it
        global items
        items = list(filter(lambda x: x["name"] != name, items))
        return {"message": "Item is deleted..."}

    def put(self, name):
        data = Item.parser.parse_args()

        # Shown below is directly getting the request without any control over it.
        # data = request.get_json()
        item = next(filter(lambda x: x["name"] == name, items), None)

        if item is None:
            item = {"name": name, "price": data["price"]}
            items.append(item)
        else:
            item.update(data)
        return item

class ItemList(Resource):
    def get(self):
        return {"items": items}

# 200 -> OK Status Code
# you don't need to use the decorator now...
api.add_resource(Item, "/item/<string:name>")
api.add_resource(ItemList, "/items")
api.add_resource(UserRegister, "/register")

app.run(port=5000, debug= True)

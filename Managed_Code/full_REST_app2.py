from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity

from user import UserRegister
from item import Item, ItemList

app = Flask(__name__)
app.secret_key = "Chandan21"
api = Api(app)

jwt = JWT(app, authenticate, identity) # /auth

# you don't need to use the decorator now...
api.add_resource(Item, "/item/<string:name>")
api.add_resource(ItemList, "/items")
api.add_resource(UserRegister, "/register")

# In case we inport this file, then this app should not run...
# this is ensured as if it is being used by some other file, then the executed fie is called the __main__
# Thus, this file when imported will not be called __main__ and thus, will not run...
if __name__ == "__main__":
    app.run(port=5000, debug= True)

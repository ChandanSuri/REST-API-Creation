# from server's perspective, here as we see it
# POST - used to receive data
# GET - used to send data back only.

from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

stores = [
    {
        'name': 'My Wonderful Store',
        'items':[
            {
                'name': 'My Item',
                'price': 22.97
            }
        ]
    }
]

# we create various requests here

# Flask automatically looks into the template folder for the file specified...
@app.route('/')
def home():
    return render_template('index.html')

#POST /store data : {name:}
@app.route('/store', methods=['POST'])
def create_store():
    request_data = request.get_json()
    new_store = {
        'name' : request_data['name'],
        'items' : []
    }
    stores.append(new_store)
    return jsonify(new_store)

#GET /store/<string: name>
@app.route('/store/<string:name>')
def get_store(name):
    for store in stores:
        if store['name'] == name:
            return jsonify(store)
    return jsonify({'message' : "Store Not Found..."})

#GET /store
@app.route('/store')
def get_stores():
    # JSON is basically a dictionary but here the variable stores isn't a dictionary
    # since it's a list and we want to get all the stores, each store being a dictionary,
    # we cannot directly use the jsonify on this data variable.
    # It returns basically a string which is dictionary (pythonic name).
    return jsonify({'stores': stores})

#POST /store/<string:name>/item {name:, price:}
@app.route('/store/<string:name>/item', methods=['POST'])
def create_item_in_store(name):
    request_data = request.get_json()
    for store in stores:
        if(store['name'] == name):
            new_item = {
                'name' : request_data['name'],
                'price' : request_data['price']
            }
            store['items'].append(new_item)
            return jsonify(new_item)
    return jsonify({'message': "Store Not Found..."})

#GET /store/<string:name>/item
@app.route('/store/<string:name>/item')
def get_item_in_store(name):
    for store in stores:
        if store['name'] == name:
            return jsonify({'items': store['items']})
    return jsonify({'message' : "Store Not Found..."})

app.run(port=5000)

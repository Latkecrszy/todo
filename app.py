from flask import Flask, make_response, jsonify, request
import json, os, werkzeug
import dotenv
from flask_cors import CORS
from flask_pymongo import PyMongo
from pymongo import ReturnDocument
app = Flask(__name__)
app.config['MONGO_URI'] = os.environ.get('MONGO_URI', None)
cors = CORS(app, resources={r'/todo/*': {"origins": ["https://cdpn.io"]}})


@app.route('/todo/<int:id>', methods=["GET", "PUT"])
@app.route('/todo/', methods=["POST"])
def todo(id=None):
    mongo = PyMongo(app)
    if request.method == "GET":
        data = mongo.db.todo.find_one({"todoId": id})
        data = {key: value for key, value in data.items() if key != "_id"}
        res = make_response(jsonify(data))
        res.mimetype = 'application/json'
        return res, 200
    elif request.method == "POST":
        payload = request.get_json()
        if mongo.db.counters.find_one({"_id": "todo"}) is None:
            mongo.db.counters.insert_one({"_id": "todo", "num": 0})
        id = mongo.db.counters.find_one_and_update({"_id": "todo"}, {"$inc": {"num": 1}}, return_document=ReturnDocument.AFTER)['num']
        data = {"title": payload.get("title", None), "userId": payload.get("userId", None),
                "completed": payload.get("completed", None), "todoId": id}
        mongo.db.todo.insert_one(data)
        data = {key: value for key, value in data.items() if key != "_id"}
        res = make_response(jsonify(data))
        res.mimetype = 'application/json'
        return res, 200
    elif request.method == "PUT":
        payload = request.get_json()
        mongo.db.todo.find_one_and_replace({"todoId": id}, {"title": payload.get("title", None), "userId": payload.get("userId", None),
                "completed": payload.get("completed", None), "todoId": id})
        data = {"title": payload.get("title", None), "userId": payload.get("userId", None),
                "completed": payload.get("completed", None), "todoId": id}
        res = make_response(jsonify(data))
        res.mimetype = 'application/json'
        return res, 200



app.register_error_handler(405, lambda e: 'Error: Method Not Allowed')
app.register_error_handler(404, lambda e: 'Error: Not Found')
app.register_error_handler(403, lambda e: 'Error: Forbidden')
app.register_error_handler(400, lambda e: 'Error: Bad Request')




if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, use_reloader=True)

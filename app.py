from flask import Flask, make_response, jsonify, request
import json
import os

from flask_cors import CORS


app = Flask(__name__)

cors = CORS(app, resources={r'/todo/*': {"origins": ["https://cdpn.io"]}})


@app.route('/todo/<int:id>', methods=["GET", "PUT"])
@app.route('/todo/', methods=["POST"])
def todo(id=None):
    with open("todos.json") as f:
        todos = json.load(f)
    if request.method == "GET":
        data = [todos[str(todo)] for todo in todos.keys() if int(todo) == id]
        data = data[0]
        res = make_response(jsonify(data))
        res.mimetype = 'application/json'

        return res, 200
    elif request.method == "POST":
        payload = request.get_json()
        intKeys = [int(key) for key in todos]
        maxKey = max(intKeys)
        newKey = maxKey + 1
        todos[str(newKey)] = {"title": payload.get("title", None), "userId": payload.get("userId", None), "completed": payload.get("completed", None)}
        data = {"title": payload.get("title", None), "userId": payload.get("userId", None),
                "completed": payload.get("completed", None), "todoId": newKey}
        with open("todos.json", "w") as f:
            json.dump(todos, f, indent=4)
        return jsonify(data), 200

    elif request.method == "PUT":
        payload = request.get_json()
        todos[str(id)] = {"title": payload.get("title", None), "userId": payload.get("userId", None),
                          "completed": payload.get("completed", None)}

        with open("todos.json", "w") as f:
            json.dump(todos, f, indent=4)

        return jsonify({"title": payload.get("title", None), "userId": payload.get("userId", None),
                        "completed": payload.get("completed", None)}), 200





if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5001))
    app.run(host='0.0.0.0', port=port, debug=True, use_reloader=True)

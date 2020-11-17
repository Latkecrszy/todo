from flask import Flask, make_response, jsonify, request
import json

app = Flask(__name__)


@app.route('/todo/<id>', methods=["GET"])
@app.route('/todo/', methods=["POST"])
def todo(id=None):
    with open("todos.json") as f:
        todos = json.load(f)
    if request.method == "GET":
        if len(todos) <= int(id)-1:
            id = len(todos)
        data = todos[id]
        res = make_response(jsonify(data))
        res.mimetype = 'application/json'
        return res
    elif request.method == "POST":
        payload = request.get_json()
        todos.append({"title": payload.get("title", None), "userId": payload.get("userId", None), "completed": payload.get("completed", None)})
    with open("todos.json", "w") as f:
        json.dump(todos, f, indent=4)


if __name__ == '__main__':
    app.run()
